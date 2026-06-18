import argparse
import html
import os
import sys
import webbrowser
from urllib.parse import urlparse

from colorama import Fore, Style, init as colorama_init


TEMPLATE_NAME = "templates/poc_template.html"
VERSION = "csrf-poc-generator 1.0.0"


def print_error(message):
    print(f"{Fore.RED}[ERROR]{Style.RESET_ALL} {message}", file=sys.stderr)


def print_warning(message):
    print(f"{Fore.YELLOW}[WARNING]{Style.RESET_ALL} {message}", file=sys.stderr)


def print_success(message):
    print(f"{Fore.GREEN}{message}{Style.RESET_ALL}")


def validate_url(url):
    parsed = urlparse(url)
    if parsed.scheme.lower() not in {"http", "https"} or not parsed.netloc:
        raise ValueError(
            "Invalid URL format. Please provide a full URL like https://example.com/target"
        )


def parse_fields(fields_string):
    if not fields_string:
        raise ValueError(
            "Empty fields string. Use --fields \"key=value&key2=value2\".")

    fields = {}
    for pair in fields_string.split("&"):
        pair = pair.strip()
        if not pair:
            continue
        if "=" not in pair:
            raise ValueError(f"Invalid field format: '{pair}'. Expected key=value")
        key, value = pair.split("=", 1)
        if not key:
            raise ValueError(
                f"Invalid field format: '{pair}'. Field name cannot be empty"
            )
        fields[key] = value

    if not fields:
        raise ValueError(
            "No valid fields found. Ensure --fields contains at least one key=value pair."
        )

    return fields


def load_template():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    template_path = os.path.join(script_dir, TEMPLATE_NAME)
    try:
        with open(template_path, "r", encoding="utf-8") as template_file:
            return template_file.read()
    except OSError as exc:
        raise RuntimeError(f"Unable to load template file: {template_path}") from exc


def generate_html(url, method, fields, template):
    method = method.upper()
    if method not in {"GET", "POST"}:
        raise ValueError("Method must be GET or POST")

    escaped_url = html.escape(url, quote=True)
    escaped_method = html.escape(method, quote=True)
    input_fields = []
    for key, value in fields.items():
        escaped_key = html.escape(key, quote=True)
        escaped_value = html.escape(value, quote=True)
        input_fields.append(
            f'<input type="hidden" name="{escaped_key}" value="{escaped_value}" />'
        )

    inputs_html = "\n        ".join(input_fields)
    return template.format(action_url=escaped_url, method=escaped_method, inputs=inputs_html)


def main(argv=None):
    colorama_init(autoreset=True)

    parser = argparse.ArgumentParser(description="CSRF PoC Generator")
    parser.add_argument("--url", required=True, help="Target URL")
    parser.add_argument(
        "--method",
        default="POST",
        choices=["GET", "POST", "get", "post"],
        help="HTTP method to use for the form",
    )
    parser.add_argument(
        "--fields",
        required=True,
        help="Form fields as key=value&key2=value2",
    )
    parser.add_argument(
        "--output",
        default="csrf_poc.html",
        help="Output filename for the generated PoC",
    )
    parser.add_argument(
        "--open",
        action="store_true",
        help="Open the generated PoC in the default browser",
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Print verbose information while generating the PoC",
    )
    parser.add_argument(
        "--version",
        action="version",
        version=VERSION,
        help="Print version information and exit",
    )

    args = parser.parse_args(argv)

    try:
        validate_url(args.url)
        fields = parse_fields(args.fields)

        if args.verbose:
            for key, value in fields.items():
                print(f"{Fore.YELLOW}Injecting field:{Style.RESET_ALL} {key}={value}")

        template = load_template()
        html_output = generate_html(args.url, args.method, fields, template)

        output_path = os.path.abspath(args.output)
        try:
            with open(output_path, "w", encoding="utf-8") as output_file:
                output_file.write(html_output)
        except OSError as exc:
            print_error(
                f"Unable to write output file: {output_path}. {exc.strerror or exc}"
            )
            sys.exit(1)

        print_success(f"CSRF PoC generated: {output_path}")

        if args.open:
            webbrowser.open(output_path)
    except ValueError as exc:
        print_error(str(exc))
        sys.exit(1)
    except RuntimeError as exc:
        print_error(str(exc))
        sys.exit(1)


if __name__ == "__main__":
    main()
