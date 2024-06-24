from dataclasses import dataclass
from types import MappingProxyType

import pandas as pd
import streamlit as st

from pathlib import Path
import json


import datetime
import calendar
from streamlit_calendar import calendar as st_calendar

from doctor_ui.user import UserRoles
from doctor_ui.views.registry import AppView, appview



@dataclass
class _ViewData:
    player_stocks: pd.DataFrame
    npc_stocks: pd.DataFrame


@st.cache_data
def convert_df(df):
    return df.to_csv().encode("utf-8")


@appview
class CalendarView(AppView):
    """Stocks AppView."""

    idx = 14
    name = "Календарь Исследований"
    icon = "calendar-range-fill"
    roles = (
        UserRoles.ROOT.value,
        UserRoles.MANAGER.value,
        UserRoles.HR.value,
        UserRoles.DOCTOR.value,
    )

    def __init__(self) -> None:
        self.view_data: _ViewData | None = None

    def render(self) -> None:
        st.title("Календарь исследований")
        modal_color: dict = json.loads(Path('../data/modal_color.json').read_text())
        """Render view."""
        df = pd.read_parquet('../data/df_cal.parquet')
        editable = "true"
        if st.session_state.user.role == UserRoles.DOCTOR.value:
            df = df[df['Doctor'] == st.session_state.user.name]
            editable = False
        resources = df[['Doctor', 'title']].reset_index().to_dict(orient='records')
        current_year = datetime.datetime.now().year
        current_month = datetime.datetime.now().month
        month_segments_dict = split_month_into_segments(current_year, current_month)
        # Generate calendar events with counts in the title
        calendar_events_with_counts = []
        for index, row in df.iterrows():
            for week in range(1, 5):
                start_date, end_date = month_segments_dict[week]
                event = {
                    "allDay": True,
                    "title": f"{row['title']} | {row[f'week_{week}']}",
                    "start": start_date,
                    "end": end_date,
                    "color": modal_color[row['title']],
                    "resourceId": str(index),
                }
                calendar_events_with_counts.append(event)
        calendar_options = {
            "editable": editable,
            "selectable": "true",
            "headerToolbar": {
                "left": "today prev,next",
                "center": "title",
            },
            "slotMinTime": "06:00:00",
            "slotMaxTime": "22:00:00",
            "initialView": "resourceTimelineMonth",
            "resourceGroupField": "Doctor",
            "resources": resources,
        }

        custom_css="""
            .fc-event-past {
                opacity: 0.8;
            }
            .fc-event-time {
                font-style: italic;
            }
            .fc-event-title {
                font-weight: 700;
            }
            .fc-toolbar-title {
                font-size: 2rem;
            }
        """
        cal = st_calendar(events=calendar_events_with_counts, options=calendar_options, custom_css=custom_css)
        st.download_button("Выгрузить табель", convert_df(df), file_name="табель.csv", mime="text/csv")
        if st.button("Сохранить"):
            pass


def split_month_into_segments(year, month, segments=4):
    """
    Splits the specified month into a given number of segments.

    Parameters:
    - year: int, the year of the month to split.
    - month: int, the month to split.
    - segments: int, the number of segments to split the month into.

    Returns:
    - Dictionary with segment numbers as keys and [start_date, end_date] as values.
    """
    # Calculate the total number of days in the specified month
    total_days = calendar.monthrange(year, month)[1]

    # Calculate the number of days per segment
    days_per_segment = total_days // segments

    # Generate the start and end dates for each segment
    segments_dict = {}
    start_date = datetime.date(year, month, 1)

    for i in range(segments):
        end_date = start_date + datetime.timedelta(days=days_per_segment - 1) + datetime.timedelta(days=1)
        if i == segments - 1:  # Make sure the last segment covers the remaining days
            end_date = datetime.date(year, month, total_days) + datetime.timedelta(days=1)
        segments_dict[i + 1] = [start_date.strftime('%Y-%m-%d'), end_date.strftime('%Y-%m-%d')]
        start_date = end_date
    
    return segments_dict
