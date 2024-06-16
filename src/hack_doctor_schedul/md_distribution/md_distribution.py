import pandas as pd
from pathlib import Path
import numpy as np


def preprocess_predictions(
    predictions_path: Path,
    medical_tests_list: list,
    datetime_column: str,
):
    df = pd.read_csv(
        predictions_path,
        usecols=medical_tests_list + [datetime_column],
        parse_dates=[datetime_column]
    )
    df[medical_tests_list] = df[medical_tests_list].apply(np.ceil).astype("int64")
    return df


def greedy_workload_distribution(
    df_md: pd.DataFrame,
    df_pred: pd.DataFrame,
    df_norm: pd.DataFrame,
    current_date: pd.Timestamp,
    date_column: str,
):
    df_md.sort_values(["md_type", "total_workload"], ascending=True, inplace=True)
    df_norm_current = df_norm.copy().set_index("name")
    df_norm_current["prediction"] = df_pred
    schedule_list = df_norm_current.apply(
        lambda row: greedy_distribution_by_medical_test(
            row,
            df_md,
        ),
        axis=1,
    ).tolist()
    df_schedule = pd.concat(schedule_list, ignore_index=True)
    df_schedule[date_column] = current_date
    return df_schedule[["md_id", "md_type", "modality", "count", "ds"]]


def greedy_distribution_by_medical_test(current_norm, df_md):

    md_type_mask = df_md["md_type"] == current_norm["md_type"]
    df_md_counter = df_md[["md_id", "md_type"]].copy()
    df_md_counter["count"] = 0
    df_md_counter["modality"] = current_norm.name

    maximum_test_count = df_md.loc[:, "current_workload"] / current_norm["cost"]
    maximum_test_count = maximum_test_count.apply(np.floor)
    maximum_test_count[~md_type_mask] = 0
    distribution_mask = (maximum_test_count.cumsum() <= current_norm["prediction"])
    mask_to_minimize = distribution_mask & md_type_mask

    # Adding equal counts for maximum values
    df_md.loc[mask_to_minimize, "current_workload"] -= maximum_test_count[distribution_mask] * current_norm["cost"]
    df_md.loc[mask_to_minimize, "total_workload"] += maximum_test_count[distribution_mask] * current_norm["cost"]
    df_md_counter.loc[mask_to_minimize, "count"] += maximum_test_count[distribution_mask]
    # Removing number of tests left 
    count_of_tests_left = current_norm["prediction"] - maximum_test_count[distribution_mask].sum()
    index_left = df_md_counter.loc[md_type_mask, "count"].idxmin()
    df_md.loc[index_left, "current_workload"] -= count_of_tests_left * current_norm["cost"]
    df_md.loc[index_left, "total_workload"] += count_of_tests_left * current_norm["cost"]
    df_md_counter.loc[index_left, "count"] += count_of_tests_left

    return df_md_counter[df_md_counter["count"] > 0]


class MDLoader():
    def __init__(
            self,
    ):
        pass

    def load_mds(self):
        pass

    def get_mds(self):
        pass


class MockMDLoader(MDLoader):
    def __init__(
            self,
            predictions: pd.DataFrame,
            norm: list,
            cost_per_md: int,
            load_fraction: float,
            dt_column: str,
    ):
        self.df_pred_ = predictions
        self.norm_ = norm
        self.cost_per_md_ = cost_per_md
        self.load_fraction_ = load_fraction
        self.dt_column_ = dt_column

    def load_mds(self):
        df_norm = pd.DataFrame(self.norm_)
        columns_list = df_norm["name"].tolist()

        # Prepare predictions
        df_pred_long = pd.melt(
            self.df_pred_,
            id_vars=self.dt_column_,
            value_vars=columns_list,
            var_name="medical_test",
            value_name="count",
        )
        df_norm_pred = df_pred_long.merge(
            df_norm,
            how="left",
            left_on="medical_test",
            right_on="name",
        )
        df_norm_pred["units_per_time"] = df_norm_pred["cost"] * df_norm_pred["count"]
        df_norm_pred = df_norm_pred.groupby([self.dt_column_, "md_type"])["units_per_time"].sum()
        # Count mds needed for each md_type
        df_max_md_types = df_norm_pred.groupby(["md_type"]).max()
        df_max_md_types /= (self.cost_per_md_ * self.load_fraction_)
        df_max_md_types = df_max_md_types.apply(np.ceil).astype(int).rename("md_count")

        md_list = df_max_md_types.reset_index().apply(self.generate_doctors, axis=1).tolist()
        self._df_md_ = pd.concat(md_list, ignore_index=True)

    def generate_doctors(self, md_count: pd.Series):
        doctors_list = [
            {
                "md_id": f"{md_count['md_type']}_{i}",
                "md_type": md_count["md_type"]
            } for i in range(md_count["md_count"])
        ]
        return pd.DataFrame(doctors_list)

    def get_mds(self):
        return self._df_md_.copy()


class MDPool():
    def __init__(
        self,
        md_loader: MDLoader,
        norm: list,
        df_pred: pd.DataFrame,
        cost_per_md: int,
        load_fraction: float,
        dt_column: str,
        distribution_strategy=greedy_workload_distribution,
    ):
        self.md_loader_ = md_loader
        self.md_loader_.load_mds()
        self.df_norm_ = pd.DataFrame(norm)
        self.df_pred_ = df_pred
        self.cost_per_md_ = cost_per_md
        self.load_fraction_ = load_fraction
        self.dt_column_ = dt_column
        self.distribution_strategy_ = distribution_strategy

    def distribute_workload(self):
        df_md = self.md_loader_.get_mds()
        # Initialize dataframe before itearions
        df_md["total_workload"] = 0

        schedule_list = self.df_pred_.apply(
            lambda current_pred: self.distribute_workload_at_iter(
                current_pred,
                df_md,
            ),
            axis=1
        ).tolist()
        self.df_schedule_ = pd.concat(schedule_list, ignore_index=True)

    def distribute_workload_at_iter(self, df_current_predictions, df_md):
        df_md["current_workload"] = self.cost_per_md_ * self.load_fraction_
        return self.distribution_strategy_(
            df_md,
            df_current_predictions.drop(self.dt_column_),
            self.df_norm_,
            df_current_predictions[self.dt_column_],
            self.dt_column_,
        )

    def create_md_scedule(self):
        self.distribute_workload()
        return self.df_schedule_.copy()
