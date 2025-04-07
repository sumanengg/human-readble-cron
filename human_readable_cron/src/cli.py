from .converter import CronConverter

"""
  This is the utility file , which convert every human readable cron expression to the standard cron expression.
  The cron expression is a string representing a schedule for running a command or script at specific times.
"""

def convert_command(args):
    "Handle the convert subcommand."
    converter = CronConverter(args.expression)
    print(converter.cron_expression)

def validate_command(args):
    "Handle the validate subcommand."
    converter = CronConverter(args.expression)
    if converter.is_valid():
        print(f"The cron expression '{args.expression}' is valid.")
    else:
        print(f"The cron expression '{args.expression}' is invalid.")




def main():
    import argparse
    import sys

    parser = argparse.ArgumentParser(description="Convert human-readable cron expressions to standard cron format.")
    subparsers = parser.add_subparsers(dest="command")
    # Add 'convert' subcommand
    convert_parser = subparsers.add_parser("convert", help="Convert human-readable cron to standard cron format")
    convert_parser.add_argument("expression", type=str, help="The human-readable cron expression to convert")
    convert_parser.set_defaults(func=convert_command)

    # Add 'validate' subcommand (example for extensibility)
    validate_parser = subparsers.add_parser("validate", help="Validate a standard cron expression")
    validate_parser.add_argument("expression", type=str, help="The standard cron expression to validate")
    validate_parser.set_defaults(func=validate_command)

    # Parse the arguments
    args = parser.parse_args()

    # Call the appropriate function based on the subcommand
    if hasattr(args, "func"):
        args.func(args)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()