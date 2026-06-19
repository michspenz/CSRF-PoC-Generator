# CSRF PoC Generator

A CLI utility for generating CSRF proof-of-concept payloads for web security testing.

[![Python 3.9+](https://img.shields.io/badge/python-3.9%2B-blue)](https://www.python.org/)
[![MIT License](https://img.shields.io/badge/license-MIT-green)](LICENSE)


## 1. Project title + description

CSRF PoC Generator is a compact command-line tool for pentesters and DFIR analysts who need to rapidly build and validate cross-site request forgery proof-of-concept pages.

## 2. What is CSRF?

Cross-Site Request Forgery (CSRF) is a web application vulnerability where an attacker tricks a victim into submitting an authenticated request without their intent. The attacker leverages the victim's active session to perform actions on behalf of the user.

## 3. Features

- Generate valid HTML PoC payloads for both `POST` and `GET` form submission methods
- Convert field strings like `amount=1000&to=attacker` into hidden form inputs
- Auto-submit PoC pages on load with a fallback manual submit button
- Optional browser auto-open for quick validation
- Verbose output for field injection visibility
- Robust CLI error handling for invalid input and file write issues

## 4. Installation

```bash
git clone https://github.com/michspenz/csrf-poc-generator.git
cd csrf-poc-generator
pip install -r requirements.txt
```

## 5. CLI usage examples

### Basic POST PoC

```bash
python csrf_generator.py --url https://example.com/transfer --method POST --fields "amount=1000&to=attacker"
```

### GET request PoC

```bash
python csrf_generator.py --url https://example.com/search --method GET --fields "query=admin&debug=true"
```

### Custom output filename

```bash
python csrf_generator.py --url https://example.com/transfer --method POST --fields "amount=1000&to=attacker" --output my_csrf_poc.html
```

### Auto-open in browser

```bash
python csrf_generator.py --url https://example.com/transfer --method POST --fields "amount=1000&to=attacker" --open
```

This tool is designed for pentesters, DFIR analysts, and security consultants who need a fast, repeatable way to generate CSRF payloads for validation, reporting, and incident response.

Released under the MIT License. See the `LICENSE` file for full terms.
