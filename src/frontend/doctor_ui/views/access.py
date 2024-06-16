from dataclasses import dataclass

import pandas as pd
import streamlit as st


from doctor_ui.user import UserRoles
from doctor_ui.views.registry import AppView, appview

import pandas as pd
import numpy as np


@appview
class AccessView(AppView):
    """Stocks AppView."""

    idx = 17
    name = "Управление сотрудниками"
    icon = "file-earmark-person"
    roles = (
        UserRoles.ROOT.value,
        UserRoles.MANAGER.value,
        UserRoles.HR.value,
        # UserRoles.DOCTOR.value,
    )

    def __init__(self) -> None:
        self.view_data = None

    def render(self) -> None:
        """Render view."""
        st.title("Управление данными сотрудников")
        df = pd.read_parquet('../data/df_users.parquet')
        edited_df = st.data_editor(df, num_rows='dynamic', )
        if st.button("Сохранить"):
            edited_df.to_parquet('../data/df_users.parquet')
        