"""Parse and validate Beneficial Ownership Data Standard JSON documents."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Iterable, List

from jsonschema import Draft202012Validator, FormatChecker
from referencing import Registry, Resource
from referencing.jsonschema import DRAFT202012


def default_schema_dir() -> Path:
    """Return the default location of the schema directory within the repo."""

    return Path(__file__).resolve().parents[1] / "schema"


def load_json_document(path: Path):
    """
    Load JSON from a file and return the parsed object.

    Raises a :class:`ValueError` if the file contains invalid JSON, to ensure
    calling code can distinguish between parse failures and validation errors.
    """

    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:  # pragma: no cover - defensive branch
        raise ValueError(f"Invalid JSON in {path}: {exc}") from exc


def _schema_registry(schema_dir: Path) -> Registry:
    """Create a registry containing all JSON schemas in ``schema_dir``."""

    if not schema_dir.exists():
        raise FileNotFoundError(f"Schema directory not found: {schema_dir}")

    resources = []
    for schema_path in sorted(schema_dir.glob("*.json")):
        try:
            schema = json.loads(schema_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:  # pragma: no cover - defensive branch
            raise ValueError(f"Invalid JSON schema: {schema_path}") from exc
        schema_id = schema.get("$id")
        if not schema_id:
            continue
        resources.append((schema_id, Resource(contents=schema, specification=DRAFT202012)))

    if not resources:
        raise ValueError(f"No JSON schemas with $id found in {schema_dir}")

    return Registry().with_resources(resources)


def build_validator(schema_dir: Path | None = None) -> Draft202012Validator:
    """Build a JSON Schema validator for BODS statements."""

    schema_dir = schema_dir or default_schema_dir()
    registry = _schema_registry(schema_dir)
    try:
        statement_schema = registry.contents("urn:statement")
    except KeyError as exc:  # pragma: no cover - defensive branch
        raise ValueError(f"Statement schema not found in {schema_dir}") from exc
    return Draft202012Validator(statement_schema, registry=registry, format_checker=FormatChecker())


def validate_document(document, validator: Draft202012Validator) -> List:
    """Return a sorted list of validation errors for ``document``."""

    errors = validator.iter_errors(document)
    return sorted(errors, key=lambda error: [str(part) for part in error.path])


def _format_errors(errors: Iterable) -> str:
    formatted = []
    for error in errors:
        json_path = "/" + "/".join(str(part) for part in error.path)
        formatted.append(f"- {json_path or '/'}: {error.message}")
    return "\n".join(formatted)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("document", type=Path, help="Path to a BODS JSON document")
    parser.add_argument(
        "--validate",
        action="store_true",
        help="Validate the document against the local BODS statement schema.",
    )
    parser.add_argument(
        "--schema-dir",
        type=Path,
        default=default_schema_dir(),
        help="Path to the directory containing the JSON schema files.",
    )

    args = parser.parse_args(argv)

    try:
        document = load_json_document(args.document)
    except Exception as exc:  # pragma: no cover - defensive branch
        print(f"Failed to load {args.document}: {exc}", file=sys.stderr)
        return 1

    print(f"Loaded {args.document} successfully (type={type(document).__name__}).")

    if args.validate:
        try:
            validator = build_validator(args.schema_dir)
        except Exception as exc:  # pragma: no cover - defensive branch
            print(f"Failed to build validator: {exc}", file=sys.stderr)
            return 1
        errors = validate_document(document, validator)
        if errors:
            print("Validation errors detected:")
            print(_format_errors(errors))
            return 1
        print("Document is valid BODS.")

    return 0


if __name__ == "__main__":  # pragma: no cover - CLI entry point
    raise SystemExit(main())
