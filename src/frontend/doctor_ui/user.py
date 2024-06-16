"""Users auth API."""
import pandas as pd
from enum import Enum

import streamlit as st
from pydantic import BaseModel, parse_obj_as

from doctor_ui.settings import settings


class UserRoles(Enum):
    """User roles."""

    ROOT = "root"  # noqa: WPS115
    MANAGER = 'manager'  # noqa: WPS115
    HR = 'hr'  # noqa: WPS115
    DOCTOR = 'doctor'  # noqa: WPS115

class User(BaseModel):
    """User model."""
    role: str
    name: str


class AuthAPI:
    """Authentication API."""
    engine = settings.get_engine

    @classmethod
    def get_auth_header(cls, login: str, password: str) -> dict[str, str] | None:
        """Get authentication header for the given login and password.

        Args:
            login (str): user login.
            password (str): user password.

        Returns:
            dict[str, str] | None: auth header or None if login or password is incorrect.
        """
        
        df = pd.read_parquet('../data/df_users.parquet')
        if login in df['login'].values:
            pswrd = df.loc[df['login'] == login, 'password'].item()
            if pswrd == password:
                return {"Authorization": "Approved"}
        return None

    @classmethod
    def get_user(cls, user_name) -> User | None:
        """Get authenticated user info.

        Args:
            auth_header (dict[str, str]): auth header.

        Returns:
            User | None: user info or None if auth header is incorrect.
        """
        df = pd.read_parquet('../data/df_users.parquet')
        if user_name in df['login'].values:
            user_info = df.loc[df['login'] == user_name]
        else:
            return None
        return User(name=user_info['login'].item(), role=user_info['role'].item())
