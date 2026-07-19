# Persona / Prompt Spec Template
![License: MIT](https://img.shields.io/github/license/prashibadkur11-creator/persona-spec-template) ![CI](https://img.shields.io/github/actions/workflow/status/prashibadkur11-creator/persona-spec-template/spec-ci.yml?branch=main&label=CI)

A structured, forkable format for defining **how an AI feature should behave —
before the prompt is written.** Think of it as a PRD for AI behavior: the source
of truth a PM owns, that engineers build the prompt from and QA tests against.

Most AI behavior lives in someone's head or a Slack thread, gets translated into
a prompt, and loses its nuance on the way. This template forces the intent into a
precise, testable spec instead.

## What a spec captures

Each spec is a YAML file conforming to [`schema.yaml`](schema.yaml):

| Section | What it pins down |
|---|---|
| `identity` | Who the persona is and what it's for |
| `tone_and_voice` | Concrete, testable voice rules (not "be friendly") |
| `capabilities` | What it should do |
| `constraints` | Hard must-nots and boundaries |
| `failure_modes` | How it specifically tends to break |
| `eval_criteria` | How you'll measure whether it's behaving |
| `example_interactions` | Good and bad sample exchanges |
| `metadata` | Owner, version, linked prompt |

## How it connects to the rest of the toolkit

This spec is the design doc at the center of a small system:

- **`failure_modes` reference the [AI Failure Mode Taxonomy](https://github.com/prashibadkur11-creator/ai-failure-mode-taxonomy)**
  by `taxonomy_id` (e.g. `persona-drift`, `sycophancy`). The spec names the risks;
  the taxonomy catalogs each one's causes, detection, and mitigation.
- **`eval_criteria` feed the [Prompt Regression Suite](https://github.com/prashibadkur11-creator/prompt-regression-suite).**
  Each criterion is written to become a test case — so the qualities the spec
  promises are the qualities CI actually checks.

Spec defines the behavior → taxonomy catalogs the risks → suite tests the result.

See [`specs/support-reply-drafter.yaml`](specs/support-reply-drafter.yaml) for a
worked example with both cross-references filled in.

## Using it

```bash
pip install -r requirements.txt

# Fork, then copy the template and fill it in
cp TEMPLATE.yaml specs/my-persona.yaml

# Validate against the schema (also what CI runs)
python scripts/validate_spec.py
```

The validator checks every required section is present and non-empty, that
`failure_modes` / `eval_criteria` / `example_interactions` have their sub-fields,
and that you included at least one good and one bad example. It exits non-zero on
any problem, so it can gate a pull request.

## The PR workflow

1. Add or edit a spec on a branch.
2. Open a PR — the **Spec CI** action validates every spec.
3. An incomplete spec fails the check until fixed.

This keeps specs disciplined: a spec in `main` is always complete and schema-valid.

## Repo layout

```
.
├── schema.yaml                     # the spec schema (field definitions)
├── TEMPLATE.yaml                   # blank spec to copy and fill in
├── specs/
│   └── support-reply-drafter.yaml  # worked example with cross-references
├── scripts/
│   └── validate_spec.py            # schema validator (the PR gate)
└── .github/workflows/spec-ci.yml
```

## License

MIT.
