import json
from pathlib import Path

import pytest

from tools.parse_bods_document import (
    _format_errors,
    build_validator,
    default_schema_dir,
    load_json_document,
    validate_document,
)


def test_load_json_document_roundtrip(tmp_path: Path):
    payload = {"example": True, "items": [1, 2, 3]}
    doc_path = tmp_path / "statement.json"
    doc_path.write_text(json.dumps(payload))

    loaded = load_json_document(doc_path)

    assert loaded == payload


def test_load_json_document_invalid(tmp_path: Path):
    doc_path = tmp_path / "bad.json"
    doc_path.write_text("{ invalid json")

    with pytest.raises(ValueError):
        load_json_document(doc_path)


def test_validate_example_document():
    validator = build_validator(default_schema_dir())
    doc_path = Path(__file__).resolve().parents[1] / "examples" / "fermcat.json"

    errors = validate_document(load_json_document(doc_path), validator)

    assert errors == []


def test_validate_document_reports_errors():
    validator = build_validator(default_schema_dir())
    invalid_document = [{}]

    errors = validate_document(invalid_document, validator)
    formatted = _format_errors(errors)

    assert errors
    assert "- /0:" in formatted


def test_build_validator_missing_schema_dir(tmp_path: Path):
    missing_dir = tmp_path / "no-schema"

    with pytest.raises(FileNotFoundError):
        build_validator(missing_dir)
