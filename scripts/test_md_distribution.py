from hack_doctor_schedul.md_distribution import md_distribution as mdd
import pandas as pd
from pathlib import Path

# Test 1
mock_predictions_path = Path("./data/processed/test/mock_predictions.csv")
test_columns = [
    "Денситометр",
    "КТ",
    "КТ с КУ 1 зона",
    "КТ с КУ 2 и более зон",
    "ММГ",
    "МРТ",
    "МРТ с КУ 1 зона",
    "МРТ с КУ 2 и более зон",
    "РГ",
    "Флюорограф",
]
dt_column = "ds"
df_mock_processed_true = mdd.preprocess_predictions(
    mock_predictions_path,
    test_columns,
    dt_column,
)
df_mock_processed_test = pd.read_csv("./data/processed/test/mock_processed.csv", parse_dates=[dt_column])


if df_mock_processed_test.equals(df_mock_processed_true):
    print("Test 1. Passed")
else:
    print("Test 1. failed")
    print("Test df")
    print(df_mock_processed_test)
    print("True df")
    print(df_mock_processed_true)

# Test 2

if df_mock_processed_test.dtypes.equals(df_mock_processed_true.dtypes):
    print("Test 2. Passed")
else:
    print("Test 2. failed")
    print("Test df")
    print(df_mock_processed_test.dtypes)
    print("True df")
    print(df_mock_processed_true.dtypes)

# Test 3

df_simple_processed_test = pd.read_csv("./data/processed/test/mock_processed_simple.csv", parse_dates=[dt_column])
test_norm = [
    {
        "name": "Денситометр",
        "cost": 2.2,
        "md_type": "xray",
    },
    {
        "name": "КТ",
        "cost": 11.6,
        "md_type": "ct",
    },
    {
        "name": "КТ с КУ 1 зона",
        "cost": 18.8,
        "md_type": "ct",
    },
]
cost_per_md = 2367
defensive_percent = 0.8
df_md = pd.DataFrame(
    [
        {
            "md_id": "ct_0",
            "md_type": "ct",
        },
        {
            "md_id": "xray_0",
            "md_type": "xray",
        },
        {
            "md_id": "xray_1",
            "md_type": "xray",
        },
        {
            "md_id": "xray_2",
            "md_type": "xray",
        },
        {
            "md_id": "xray_3",
            "md_type": "xray",
        },
        {
            "md_id": "xray_4",
            "md_type": "xray",
        },
    ]
)

mock_loader = mdd.MockMDLoader(
    df_simple_processed_test,
    test_norm,
    cost_per_md=cost_per_md,
    load_fraction=defensive_percent,
    dt_column=dt_column,
)
mock_loader.load_mds()
if df_md.equals(mock_loader.get_mds()):
    print("Test 3. Passed")
else:
    print("Test 3. failed")
    print("Test df")
    print(df_md)
    print("True df")
    print(mock_loader.get_mds())

# Test 4
df_mock_schedule = pd.read_csv("./data/processed/test/mock_schedule.csv", parse_dates=[dt_column])
md_pool = mdd.MDPool(
    md_loader=mock_loader,
    norm=test_norm,
    df_pred=df_simple_processed_test,
    cost_per_md=cost_per_md,
    load_fraction=defensive_percent,
    dt_column=dt_column,
    distribution_strategy=mdd.greedy_workload_distribution,
)
md_pool.distribute_workload()
df_schedule_true = md_pool.create_md_scedule()
if df_mock_schedule.sort_values(["ds"]).reset_index(drop=True).equals(df_schedule_true.sort_values(["ds"]).reset_index(drop=True)):
    print("Test 4. Passed")
else:
    print("Test 4. failed")
    print("Test df")
    print(df_mock_schedule.sort_values(["ds"]).reset_index(drop=True))
    print("True df")
    print(df_schedule_true.sort_values(["ds"]).reset_index(drop=True))

# Test 5
df_md_strat_test = mock_loader.get_mds().copy()
df_md_strat_test["current_workload"] = cost_per_md * defensive_percent
df_md_strat_test["total_workload"] = 1000
df_md_strat_test.loc[1, "total_workload"] = 1043
df_md_strat_test.loc[2, "total_workload"] = 1430
current_predictions = df_simple_processed_test.loc[3, :].drop(dt_column)
current_schedule = df_mock_schedule[df_mock_schedule[dt_column] == "2024-01-22"].reset_index(drop=True)
current_greedy_dist = mdd.greedy_workload_distribution(
    df_md_strat_test,
    current_predictions,
    pd.DataFrame(test_norm),
    pd.Timestamp("2024-01-22"),
    "ds",
)
if current_schedule.equals(
    current_greedy_dist
):
    print("Test 5. Passed")
else:
    print("Test 5. failed")
    print("Test df")
    print(current_schedule)
    print("True df")
    print(
        current_greedy_dist
    )
