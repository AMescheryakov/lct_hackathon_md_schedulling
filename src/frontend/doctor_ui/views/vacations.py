from dataclasses import dataclass

import pandas as pd
import streamlit as st


from doctor_ui.user import UserRoles
from doctor_ui.views.registry import AppView, appview

import pandas as pd
import numpy as np


@appview
class VacationsView(AppView):
    """Stocks AppView."""

    idx = 15
    name = "График"
    icon = "bar-chart"
    roles = (
        UserRoles.ROOT.value,
        UserRoles.MANAGER.value,
        UserRoles.DOCTOR.value,
    )

    def __init__(self) -> None:
        self.view_data = None

    def render(self) -> None:
        """Render view."""
        st.title("Управление доступностью")
        df = pd.read_parquet('../data/df_vac.parquet')
        df_orig = df.copy()
        if st.session_state.user.role == UserRoles.DOCTOR.value:
            df = df[df['Doctor'] == st.session_state.user.name].copy()
        edited_df = st.data_editor(df)
        if st.button("Сохранить"):
            df_orig.loc[edited_df.index] = edited_df
            df_orig.to_parquet('../data/df_vac.parquet')
