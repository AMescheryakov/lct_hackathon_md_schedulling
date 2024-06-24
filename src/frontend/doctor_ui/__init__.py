"""doctor_ui package."""
from doctor_ui.views.logout import Logout
from doctor_ui.views.calendar import CalendarView
from doctor_ui.views.vacations import VacationsView
from doctor_ui.views.speciality import SpecView
from doctor_ui.views.access  import AccessView
__all__ = ["Logout", "CalendarView", "VacationsView", "SpecView", "AccessView"]
