"""
This is the utility file , which convert every human readable cron expression to the standard cron expression.
The cron expression is a string representing a schedule for running a command or script at specific times. 

Examples of cron expressions include:
      >>> from human_readable cron import CronConverter
      >>> CronConverter("Every Monday at 10:00 AM")
        '0 10 * * 1'

"""

import re
from typing import List, Tuple, Union, Dict, Optional
from datetime import datetime, timedelta

class CronConverter:
    def __init__(self, human_readable_cron: str):
        self.human_readable_cron = human_readable_cron
        self.cron_expression = self.convert_to_cron(human_readable_cron)

    DAYS_OF_WEEK: Dict[str, int] = {
        "monday": 1, "mon": 1,
        "tuesday": 2, "tue": 2,
        "wednesday": 3, "wed": 3,   
        "thursday": 4, "thu": 4,
        "friday": 5, "fri": 5,
        "saturday": 6, "sat": 6,
        "sunday": 7, "sun": 7,
    }

    MONTHS_OF_YEAR: Dict[str, int] = {
        "january": 1, "jan": 1,
        "february": 2, "feb": 2,    
        "march": 3, "mar": 3,
        "april": 4, "apr": 4,
        "may": 5,
        "june": 6, "jun": 6,
        "july": 7, "jul": 7,
        "august": 8, "aug": 8,
        "september": 9, "sep": 9,
        "october": 10, "oct": 10,  
        "november": 11, "nov": 11,
        "december": 12, "dec": 12,
    }

    TIME_UNITS = {
        "seconds": 1,
        "minutes": 60,
        "hours": 3600,
        "days": 86400,
    }

    TIME_KEYWORDS: Dict[str, str] = {
        "MIDNIGHT": "00:00",
        "NOON": "12:00",
        "EVENING": "18:00"
    }

    def convert_to_cron(self, human_readable_cron: str) -> str:
        """
            Convert the human-readable cron expression to standard cron format.
            The standard cron format is a string with 5 fields separated by spaces:
            minute hour day month day_of_week
            Each field can contain a specific value, a range of values, or a wildcard (*).
            The fields are as follows:
            minute: 0-59
            hour: 0-23
            day: 1-31
            month: 1-12 
            day_of_week: 0-7 (0 and 7 both represent Sunday)
            The function returns the standard cron expression as a string.
            If the input is not a valid human-readable cron expression, it raises a ValueError.

        """

        human_readable_cron = human_readable_cron.lower().strip()

        # Handle special time keywords
        if re.search(r"every\s+minute", human_readable_cron):
            return "0 0 * * *"
        elif re.search(r"every\s+hour", human_readable_cron):
            return "0 * * * *"
        elif re.search(r"every\s+day", human_readable_cron):
            return "0 0 * * *"
        elif re.search(r"every\s+week", human_readable_cron):
            return "0 0 * * 1"
        elif re.search(r"every\s+month", human_readable_cron):
            return "0 0 1 * *"
        elif re.search(r"every\s+year", human_readable_cron):
            return "0 0 1 1 *"