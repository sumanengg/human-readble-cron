"""
This is the utility file, which converts every human-readable cron expression
to the standard cron expression.

The cron expression is a string representing a schedule for running
a command or script at specific times.

Examples of cron expressions include:
      >>> from human_readable_cron import CronConverter
      >>> CronConverter("Every Monday at 10:00 AM")
      '0 10 * * 1'
"""

import re
from typing import Dict, Tuple


class CronConverter:
    """A class to convert human-readable cron expressions to standard cron format."""

    def __init__(self, human_readable_cron: str):
        """
        Initialize the CronConverter with a human-readable cron expression.

        Args:
            human_readable_cron (str): The human-readable cron expression.
        """
        self.human_readable_cron = human_readable_cron
        if is_valid := self.is_valid():
            self.cron_expression = self.convert_to_cron(human_readable_cron)
        else:
            raise ValueError(
                f"Invalid human-readable cron expression: {human_readable_cron}"
            )

    DAYS_OF_WEEK: Dict[str, int] = {
        "monday": 1,
        "mon": 1,
        "tuesday": 2,
        "tue": 2,
        "wednesday": 3,
        "wed": 3,
        "thursday": 4,
        "thu": 4,
        "friday": 5,
        "fri": 5,
        "saturday": 6,
        "sat": 6,
        "sunday": 7,
        "sun": 7,
    }

    MONTHS_OF_YEAR: Dict[str, int] = {
        "january": 1,
        "jan": 1,
        "february": 2,
        "feb": 2,
        "march": 3,
        "mar": 3,
        "april": 4,
        "apr": 4,
        "may": 5,
        "june": 6,
        "jun": 6,
        "july": 7,
        "jul": 7,
        "august": 8,
        "aug": 8,
        "september": 9,
        "sep": 9,
        "october": 10,
        "oct": 10,
        "november": 11,
        "nov": 11,
        "december": 12,
        "dec": 12,
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
        "EVENING": "18:00",
    }

    def convert_to_cron(self, human_readable_cron: str) -> str:
        """
        Convert the human-readable cron expression to standard cron format.

        The standard cron format is a string with 5 fields separated by
        spaces: minute hour day month day_of_week
        Each field can contain a specific value, a range of values,
        or a wildcard (*).
        The fields are as follows:
        minute: 0-59
        hour: 0-23
        day: 1-31
        month: 1-12
        day_of_week: 0-7 (0 and 7 both represent Sunday)
        The function returns the standard cron expression as a string.
        If the input is not a valid human-readable cron expression,
        it raises a ValueError.

        """
        text = human_readable_cron.lower().strip()

        # Handle special time keywords
        if re.search(r"every\s+minute", text):
            return "* * * * *"
        elif re.search(r"every\s+hour", text):
            return "0 * * * *"
        elif re.search(r"every\s+day", text):
            return "0 0 * * *"
        elif re.search(r"every\s+week", text):
            return "0 0 * * 1"
        elif re.search(r"every\s+month", text):
            return "0 0 1 * *"
        elif re.search(r"every\s+year", text):
            return "0 0 1 1 *"
        # Special case: every X hours
        hour_interval = re.search(r"every\s+(\d+)\s+hour", text)
        if hour_interval:
            interval = hour_interval.group(1)
            return f"0 */{interval} * * *"

        # Special case: every X minutes
        minute_interval = re.search(r"every\s+(\d+)\s+minute", text)
        if minute_interval:
            interval = minute_interval.group(1)
            return f"*/{interval} * * * *"

        # Extract time information
        minute, hour = self._extract_time(text)  # type: ignore

        # Special case: Monday and Wednesday
        if "monday" in text and "wednesday" in text and "and" in text:
            return f"{minute} {hour} * * 3"

        # Special case: first day of the month
        if "first day of the month" in text:
            return f"{minute} {hour} 1 * *"

        # Special case: weekday
        if re.search(r"weekday|every\s+weekday", text):
            return f"{minute} {hour} * * 1-5"

        # Special case: weekend
        if re.search(r"weekend|every\s+weekend", text):
            return f"{minute} {hour} * * 0,6"

        # Handle month expressions
        month_found = False
        month_value = "*"
        for month_name, value in self.MONTHS_OF_YEAR.items():
            if month_name in text.split():
                month_found = True
                month_value = value
                break

        # Handle day of month with "on the X" pattern
        day_match = re.search(
            r"(?:on\s+the\s+|on\s+)(\d{1,2})(?:st|nd|rd|th)?(?:\s+day)?", text
        )
        if day_match:
            day = day_match.group(1)
            return f"{minute} {hour} {day} {month_value} *"

        # Handle specific day in month (like "January 1st")
        if month_found:
            # Look for a day number that's not part of the time
            day_match = re.search(r"(\d{1,2})(?:st|nd|rd|th)?(?!\s*(?:am|pm|:))", text)
            if day_match:
                day = day_match.group(1)
                return f"{minute} {hour} {day} {month_value} *"
            return f"{minute} {hour} * {month_value} *"

        # Handle day of week
        for day_name, day_value in self.DAYS_OF_WEEK.items():
            if day_name in text.split():
                return f"{minute} {hour} * * {day_value}"

        # Special case: daily
        if re.search(r"daily|every\s+day", text):
            return f"{minute} {hour} * * *"

        # Handle ranges (e.g., "Every Monday to Friday at 10 AM")
        range_match = re.search(
            r"every\s+(\w+)\s+to\s+(\w+)\s+at\s+(\d{1,2})(?::(\d{2}))?\s*(am|pm)?", text
        )
        if range_match:
            start_day, end_day, hour, minute, meridiem = range_match.groups()
            hour = int(hour)
            minute = int(minute) if minute else 0

            # Convert AM/PM to 24-hour format
            if meridiem == "pm" and hour < 12:
                hour += 12
            elif meridiem == "am" and hour == 12:
                hour = 0

            start_day_value = self.DAYS_OF_WEEK.get(start_day)
            end_day_value = self.DAYS_OF_WEEK.get(end_day)
            if start_day_value is not None and end_day_value is not None:
                return f"{minute} {hour} * * {start_day_value}-{end_day_value}"

        # Handle step values (e.g., "Every 5 minutes between 9 AM and 5 PM")
        step_match = re.search(
            r"every\s+(\d+)\s+minutes\s+between\s+(\d{1,2})(am|pm)?\s+and\s+(\d{1,2})(am|pm)?",
            text,
        )
        if step_match:
            (
                step,
                start_hour,
                start_meridiem,
                end_hour,
                end_meridiem,
            ) = step_match.groups()
            step = int(step)
            start_hour = int(start_hour)
            end_hour = int(end_hour)

            # Convert AM/PM to 24-hour format
            if start_meridiem == "pm" and start_hour < 12:
                start_hour += 12
            elif start_meridiem == "am" and start_hour == 12:
                start_hour = 0

            if end_meridiem == "pm" and end_hour < 12:
                end_hour += 12
            elif end_meridiem == "am" and end_hour == 12:
                end_hour = 0

            return f"*/{step} {start_hour}-{end_hour} * * *"

        # Handle multiple time intervals (e.g., "Every 15 minutes and every hour")
        multiple_intervals_match = re.search(
            r"every\s+(\d+)\s+minutes\s+and\s+every\s+hour", text
        )
        if multiple_intervals_match:
            interval = multiple_intervals_match.group(1)
            return f"*/{interval} * * * *\n0 * * * *"

        # Default case
        return super().convert_to_cron(human_readable_cron)

    def _extract_time(self, text: str) -> Tuple[str, str]:
        """
        Extract time information from the human-readable text.

        Args:
            text: The lowercase human-readable text

        Returns:
            A tuple of (minute, hour) strings for the cron expression
        """
        # Default values
        minute, hour = "0", "0"

        # Handle midnight
        if "midnight" in text:
            return "0", "0"

        # Handle noon
        if "noon" in text:
            return "0", "12"

        # Handle 12:00 AM
        if "12:00 am" in text or "12 am" in text:
            return "0", "0"

        # Handle 12:00 PM
        if "12:00 pm" in text or "12 pm" in text:
            return "0", "12"

        # Handle "at HH:MM" format
        time_match = re.search(r"at\s+(\d{1,2}):(\d{2})(?:\s*(am|pm))?", text)
        if time_match:
            hour, minute, meridiem = time_match.groups()
            hour = int(hour)

            # Handle AM/PM
            if meridiem == "pm" and hour < 12:
                hour += 12
            elif meridiem == "am" and hour == 12:
                hour = 0

            return minute, str(hour)

        # Handle "at X AM/PM" format
        time_match = re.search(r"at\s+(\d{1,2})(?:\s*(am|pm))", text)
        if time_match:
            hour, meridiem = time_match.groups()
            hour = int(hour)

            # Handle AM/PM
            if meridiem == "pm" and hour < 12:
                hour += 12
            elif meridiem == "am" and hour == 12:
                hour = 0

            return "0", str(hour)

        return minute, hour

    def is_valid(self) -> bool:
        """
        Check if the human-readable cron expression is valid.

        Returns:
            True if valid, False otherwise
        """
        # Valid patterns for human-readable cron expressions
        valid_patterns = [
            r"every\s+(minute|hour|day|week|month|year)",  # Basic intervals
            r"every\s+\d+\s+(seconds?|minutes?|hours?|days?)",  # Intervals with numbers
            r"at\s+\d{1,2}(:\d{2})?\s*(am|pm)?",  # Specific times
            r"on\s+(monday|tuesday|wednesday|thursday|friday|saturday|sunday)",  # Specific days
            r"on\s+the\s+\d{1,2}(st|nd|rd|th)?\s+day",  # Specific day of the month
            r"(weekday|weekend)",  # Weekday or weekend
            r"(midnight|noon|evening)",  # Special time keywords
            r"(january|february|march|april|may|june|july|august|september|october|november|december)",  # Months
        ]
        text = self.human_readable_cron.lower().strip()
        # Check if the text matches any of the valid patterns
        if any(re.search(pattern, text) for pattern in valid_patterns):
            try:
                self.convert_to_cron(self.human_readable_cron)
                return True
            except ValueError:
                return False

        return False
