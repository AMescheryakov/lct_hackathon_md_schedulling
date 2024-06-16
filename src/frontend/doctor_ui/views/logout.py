import streamlit as st

from doctor_ui.user import UserRoles
from doctor_ui.state import clean_cached_state
from doctor_ui.views.registry import AppView, appview


@appview
class Logout(AppView):
    """Logout option."""

    idx = 99
    name = "Выход"
    icon = "box-arrow-right"
    roles = (
        UserRoles.ROOT.value,
        UserRoles.MANAGER.value,
        UserRoles.HR.value,
        UserRoles.DOCTOR.value,
    )

    def __init__(self) -> None:
        """Empty constructor."""

    def render(self) -> None:
        """Logout user."""
        st.session_state.auth_header = None
        st.session_state.user = None
        st.session_state.views = None
        clean_cached_state()
        st.rerun()
