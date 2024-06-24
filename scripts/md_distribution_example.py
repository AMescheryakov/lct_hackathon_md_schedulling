from hack_doctor_schedul.md_distribution import md_distribution as mdd
from pathlib import Path

# Global variables
mock_predictions_path = Path("./data/processed/test/real_predictions.csv")
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
    {
        "name": "КТ с КУ 2 и более зон",
        "cost": 26.6,
        "md_type": "ct",
    },
    {
        "name": "ММГ",
        "cost": 3.7,
        "md_type": "mmg",
    },
    {
        "name": "МРТ",
        "cost": 15.1,
        "md_type": "mri",
    },
    {
        "name": "МРТ с КУ 1 зона",
        "cost": 19.7,
        "md_type": "mri",
    },
    {
        "name": "МРТ с КУ 2 и более зон",
        "cost": 30.1,
        "md_type": "mri",
    },
    {
        "name": "РГ",
        "cost": 3.7,
        "md_type": "xray",
    },
    {
        "name": "Флюорограф",
        "cost": 1,
        "md_type": "xray",
    },
]

cost_per_md = 2367
defensive_percent = 0.8

# Preprocessing predictions
df_mock_processed = mdd.preprocess_predictions(
    mock_predictions_path,
    test_columns,
    dt_column,
)

# Creating MockMDLoader examplar for md generation
mock_loader = mdd.MockMDLoader(
    df_mock_processed,
    test_norm,
    cost_per_md=cost_per_md,
    load_fraction=defensive_percent,
    dt_column=dt_column,
)

# Object for md schedule optimization
md_pool = mdd.MDPool(
    md_loader=mock_loader,
    norm=test_norm,
    df_pred=df_mock_processed,
    cost_per_md=cost_per_md,
    load_fraction=defensive_percent,
    dt_column=dt_column,
    distribution_strategy=mdd.greedy_workload_distribution,
)
df_schedule_true = md_pool.create_md_scedule()
print(df_schedule_true)