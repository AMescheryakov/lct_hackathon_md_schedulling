import streamlit as st

from doctor_ui.user import AuthAPI
from doctor_ui.views.registry import AppViewsRegistry


def login_callback() -> None:
    """Login callback, using backend for auth."""
    auth_header = AuthAPI.get_auth_header(st.session_state.login, st.session_state.password)
    if auth_header is not None:
        user = AuthAPI.get_user(st.session_state.login)
        if user is not None:
            st.session_state.auth_header = auth_header
            st.session_state.user = user
            st.session_state.views = AppViewsRegistry.role_views(user.role)
            


def login_form() -> None:
    """Streamlit login form."""
    st.markdown(
        "<center><h2>Авторизация</h2></center>",
        unsafe_allow_html=True,
    )
    st.markdown("---")
    _, col, _ = st.columns([1.5, 1, 1.5])
    with col:
        with st.form(key="login_form"):
            st.text("Система управления Московского референс-центра")
            st.text_input("Логин:", key="login")
            st.text_input("Пароль:", type="password", key="password")
            if st.form_submit_button("Войти", on_click=login_callback):
                if st.session_state.user is None:
                    st.error("Неверный логин или пароль", icon="🚨")
    st.markdown(
        "<center>В случае проблем с авторизацией, обратитесь к вашему корпоративному администратору.</center>",
        unsafe_allow_html=True,
    )
