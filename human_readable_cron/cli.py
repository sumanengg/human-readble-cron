from .converter import CronConverter
"""
  This is the utility file , which convert every human readable cron expression to the standard cron expression.
  The cron expression is a string representing a schedule for running a command or script at specific times.
"""

def main():
    import argparse
    import sys

    parser = argparse.ArgumentParser(description="Convert human-readable cron expressions to standard cron format.")
    parser.add_argument("expression", type=str, help="The human-readable cron expression to convert.")
    args = parser.parse_args()

    converter = CronConverter(args.expression)
    print(converter.cron_expression)

if __name__ == "__main__":
    main()