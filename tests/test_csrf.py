import os
import tempfile
from csrf_generator import parse_fields, generate_html, load_template


def test_parse_fields_simple():
    fields = parse_fields("amount=1000&to=attacker")
    assert fields == {"amount": "1000", "to": "attacker"}


def test_generate_html_post_method():
    template = "<form action=\"{action_url}\" method=\"{method}\">{inputs}</form>"
    html = generate_html("https://example.com/transfer", "POST", {"amount": "1000", "to": "attacker"}, template)
    assert "action=\"https://example.com/transfer\"" in html
    assert "method=\"POST\"" in html
    assert 'name="amount" value="1000"' in html
    assert 'name="to" value="attacker"' in html


def test_generate_html_get_method():
    template = "<form action=\"{action_url}\" method=\"{method}\">{inputs}</form>"
    html = generate_html("https://example.com/transfer", "GET", {"amount": "1000", "to": "attacker"}, template)
    assert "method=\"GET\"" in html


def test_output_file_generated(tmp_path):
    template = load_template()
    html = generate_html("https://example.com/transfer", "POST", {"amount": "1000"}, template)
    output_path = tmp_path / "test_generated.html"
    output_path.write_text(html, encoding="utf-8")
    assert output_path.exists()
    assert output_path.read_text(encoding="utf-8").startswith("<!DOCTYPE html>")
