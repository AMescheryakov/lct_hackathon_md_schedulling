import logging
import time

import streamlit as st
from streamlit_option_menu import option_menu

from doctor_ui.user import UserRoles
from doctor_ui.state import clean_cached_state, init_session_state
from doctor_ui.style import load_css
from doctor_ui.views.login import login_form
from doctor_ui.views.registry import AppView, AppViewsRegistry


def app() -> None:
    """Entry point for the game frontend."""
    init_session_state()
    user_views: dict[str, AppView] | None = st.session_state.views
    if user_views is None:
        login_form()
    else:
        with st.sidebar:
            menu_option = option_menu(
                "Меню",
                options=list(user_views.keys()),
                icons=[view.icon for view in user_views.values()],
                menu_icon="cast",
                default_index=0,
                key="option_menu",
            )
            # under_menu_block()
        # render current app view
        user_views[menu_option].render()



if __name__ == "__main__":
    st.set_page_config(page_title="Центр диагностики", layout="wide", page_icon="🏥")
    load_css()
    app()
