from dataclasses import dataclass

import pandas as pd
import streamlit as st


from doctor_ui.user import UserRoles
from doctor_ui.views.registry import AppView, appview

import pandas as pd
import numpy as np


@appview
class SpecView(AppView):
    """Stocks AppView."""

    idx = 16
    name = "Специализации Врачей"
    icon = "clipboard2-check"
    roles = (
        UserRoles.ROOT.value,
        UserRoles.MANAGER.value,
    )

    def __init__(self) -> None:
        self.view_data = None

    def render(self) -> None:
        """Render view."""
        st.title("Управление специализациями")
        df = pd.read_parquet('../data/df_modal.parquet')
        edited_df = st.data_editor(df)
        if st.button("Сохранить"):
            edited_df.to_parquet('../data/df_modal.parquet')
        