# human-readble-cron

A Python utility to convert human-readable cron expressions into standard cron syntax. This tool simplifies the process of creating cron expressions by allowing users to input natural language expressions like "Every Monday at 10 AM" or "Every 5 minutes between 9 AM and 5 PM."

---

## Features
- Convert human-readable cron expressions to standard cron syntax.
- Validate human-readable cron expressions with detailed error messages.
- Support for advanced cron syntax:
  - Ranges: e.g., "Every Monday to Friday at 10 AM."
  - Step values: e.g., "Every 5 minutes between 9 AM and 5 PM."
  - Multiple intervals: e.g., "Every 15 minutes and every hour."
- Support for special keywords like "midnight," "noon," and "weekday."
- CLI support for easy usage.

---

## Installation

### Using `pip`
Install the package from PyPI:
```bash
pip install human-readable-cron
