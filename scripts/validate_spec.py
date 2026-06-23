#!/usr/bin/env python3
"""
Validate persona specs in specs/ against the schema.

Checks that every required section is present and non-empty, and that
failure_modes / eval_criteria / example_interactions have their expected
sub-fields. Exits non-zero if any spec is invalid (so it can gate a PR).

Usage:
    python scripts/validate_spec.py            # validate all specs
    python scripts/validate_spec.py specs/x.yaml   # validate one

Requires: pyyaml
"""

import glob
import os
import sys

try:
    import yaml
except ImportError:
    sys.exit("Missing dependency: pyyaml. Install with `pip install pyyaml`.")

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

REQUIRED_TOP = [
    "identity",
    "tone_and_voice",
    "capabilities",
    "constraints",
    "failure_modes",
    "eval_criteria",
    "example_interactions",
]

IDENTITY_FIELDS = ["name", "role", "description"]
FAILURE_FIELDS = ["taxonomy_id", "why_it_applies", "watch_for"]
EVAL_FIELDS = ["name", "criteria", "how_measured"]
EXAMPLE_FIELDS = ["label", "user", "assistant"]


def _nonempty(v):
    if v is None:
        return False
    if isinstance(v, str):
        return v.strip() != ""
    if isinstance(v, (list, dict)):
        return len(v) > 0
    return True


def validate(path):
    errors = []
    with open(path, encoding="utf-8") as f:
        spec = yaml.safe_load(f)

    if not isinstance(spec, dict):
        return [f"{path}: file is not a valid spec mapping"]

    for section in REQUIRED_TOP:
        if section not in spec or not _nonempty(spec[section]):
            errors.append(f"missing or empty required section: {section}")

    ident = spec.get("identity") or {}
    for fld in IDENTITY_FIELDS:
        if not _nonempty(ident.get(fld)):
            errors.append(f"identity.{fld} is empty")

    for i, fm in enumerate(spec.get("failure_modes") or []):
        for fld in FAILURE_FIELDS:
            if not _nonempty(fm.get(fld)):
                errors.append(f"failure_modes[{i}].{fld} is empty")

    for i, ev in enumerate(spec.get("eval_criteria") or []):
        for fld in EVAL_FIELDS:
            if not _nonempty(ev.get(fld)):
                errors.append(f"eval_criteria[{i}].{fld} is empty")

    labels = set()
    for i, ex in enumerate(spec.get("example_interactions") or []):
        for fld in EXAMPLE_FIELDS:
            if not _nonempty(ex.get(fld)):
                errors.append(f"example_interactions[{i}].{fld} is empty")
        labels.add((ex.get("label") or "").lower())
    if spec.get("example_interactions") and not ({"good", "bad"} <= labels):
        errors.append("example_interactions should include at least one 'good' and one 'bad'")

    return [f"{os.path.basename(path)}: {e}" for e in errors]


def main():
    targets = sys.argv[1:] or glob.glob(os.path.join(ROOT, "specs", "*.yaml"))
    if not targets:
        print("No specs found in specs/.")
        return

    all_errors = []
    for path in sorted(targets):
        errs = validate(path)
        if errs:
            all_errors.extend(errs)
            print(f"INVALID  {os.path.basename(path)}  ({len(errs)} issue(s))")
            for e in errs:
                print(f"    - {e.split(': ', 1)[1]}")
        else:
            print(f"OK       {os.path.basename(path)}")

    if all_errors:
        print(f"\n{len(all_errors)} validation error(s).")
        sys.exit(1)
    print("\nAll specs valid.")


if __name__ == "__main__":
    main()
