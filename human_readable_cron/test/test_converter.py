import unittest

from human_readable_cron.src.converter import CronConverter


class TestConverter(unittest.TestCase):
    """Unit tests for the CronConverter class."""

    def test_days_of_week(self):
        """Test day of week conversions."""
        self.assertEqual(
            CronConverter("every Monday at 10 AM").cron_expression, "0 10 * * 1"
        )
        self.assertEqual(
            CronConverter("every Tuesday at 2 PM").cron_expression, "0 14 * * 2"
        )
        self.assertEqual(
            CronConverter("every Wed at 3:30 PM").cron_expression, "30 15 * * 3"
        )
        self.assertEqual(
            CronConverter("every Thursday at noon").cron_expression, "0 12 * * 4"
        )
        self.assertEqual(
            CronConverter("every Friday at midnight").cron_expression, "0 0 * * 5"
        )
        self.assertEqual(
            CronConverter("every Sat at 9 AM").cron_expression, "0 9 * * 6"
        )
        self.assertEqual(
            CronConverter("every Sun at 11 PM").cron_expression, "0 23 * * 7"
        )

    def test_time_formats(self):
        """Test various time formats."""
        self.assertEqual(
            CronConverter("daily at 10:30 AM").cron_expression, "30 10 * * *"
        )
        self.assertEqual(
            CronConverter("daily at 2:45 PM").cron_expression, "45 14 * * *"
        )
        self.assertEqual(
            CronConverter("daily at 12:00 AM").cron_expression, "0 0 * * *"
        )
        self.assertEqual(
            CronConverter("daily at 12:00 PM").cron_expression, "0 12 * * *"
        )
        self.assertEqual(CronConverter("daily at 9 AM").cron_expression, "0 9 * * *")
        self.assertEqual(CronConverter("daily at 5 PM").cron_expression, "0 17 * * *")

    def test_special_times(self):
        """Test special time keywords."""
        self.assertEqual(
            CronConverter("daily at midnight").cron_expression, "0 0 * * *"
        )
        self.assertEqual(CronConverter("daily at noon").cron_expression, "0 12 * * *")

    def test_intervals(self):
        """Test interval-based schedules."""
        self.assertEqual(CronConverter("every minute").cron_expression, "* * * * *")
        self.assertEqual(
            CronConverter("every 5 minutes").cron_expression, "*/5 * * * *"
        )
        self.assertEqual(CronConverter("every hour").cron_expression, "0 * * * *")
        self.assertEqual(CronConverter("every 2 hours").cron_expression, "0 */2 * * *")

    def test_day_of_month(self):
        """Test day of month expressions."""
        self.assertEqual(
            CronConverter("on the 1st at 10 AM").cron_expression, "0 10 1 * *"
        )
        self.assertEqual(
            CronConverter("on the 15th at 3 PM").cron_expression, "0 15 15 * *"
        )
        self.assertEqual(
            CronConverter("on the 31st day at midnight").cron_expression, "0 0 31 * *"
        )

    def test_months(self):
        """Test month expressions."""
        self.assertEqual(
            CronConverter("every January 1st at noon").cron_expression, "0 12 1 1 *"
        )
        self.assertEqual(
            CronConverter("every Dec 25 at 8 AM").cron_expression, "0 8 25 12 *"
        )
        self.assertEqual(
            CronConverter("every May at 3 PM").cron_expression, "0 15 * 5 *"
        )

    def test_complex_expressions(self):
        """Test more complex expressions."""
        self.assertEqual(
            CronConverter("every Monday and Wednesday at 2:30 PM").cron_expression,
            "30 14 * * 3",
        )  # Takes the last day
        self.assertEqual(
            CronConverter("every first day of the month at 3 AM").cron_expression,
            "0 3 1 * *",
        )

    def test_case_insensitivity(self):
        """Test that the parser is case-insensitive."""
        self.assertEqual(
            CronConverter("EVERY MONDAY AT 10 AM").cron_expression, "0 10 * * 1"
        )
        self.assertEqual(
            CronConverter("every TUESDAY at 2 PM").cron_expression, "0 14 * * 2"
        )
        self.assertEqual(
            CronConverter("Every Wednesday At Noon").cron_expression, "0 12 * * 3"
        )

    def test_whitespace_handling(self):
        """Test that the parser handles extra whitespace."""
        self.assertEqual(
            CronConverter("  every   Monday   at   10   AM  ").cron_expression,
            "0 10 * * 1",
        )

    def test_default_time(self):
        """Test default time handling."""
        self.assertEqual(CronConverter("every day").cron_expression, "0 0 * * *")

    def test_month_without_day(self):
        """Test month without specific day."""
        self.assertEqual(
            CronConverter("every February at 9 AM").cron_expression, "0 9 * 2 *"
        )

    def test_is_valid(self):
        """Test the is_valid method with various inputs."""
        # Valid cases
        self.assertTrue(CronConverter("Every minute").is_valid())
        self.assertTrue(CronConverter("Every Monday at 10 AM").is_valid())
        self.assertTrue(
            CronConverter("Every 5 minutes between 9 AM and 5 PM").is_valid()
        )

        # Invalid cases
        with self.assertRaises(ValueError) as context:
            CronConverter("Every").is_valid()
        self.assertEqual(
            str(context.exception), "Invalid human-readable cron expression: Every"
        )


if __name__ == "__main__":
    unittest.main()
