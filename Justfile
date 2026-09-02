# List the available justfile recipes
[group('general')]
@default:
  just --list --unsorted

# List the lines of code in the project
[group('general')]
loc:
  scc --remap-unknown "-*- Justfile -*-":"justfile"

# Search pydoc for given term
[group('general')]
doc term:
  uv run python -m pydoc {{term}}

# Lint and format code using ruff, applying any fixes
[group('test')]
fix:
  uv run ruff check --fix
  uv run ruff format

# Check lint, formatting, types, and workflows without modifying any files
[group('test')]
lint:
  uv run ruff check
  uv run ruff format --check
  uv run pyright
  uv run zizmor .github/workflows

# Test code using pytest
[group('test')]
test *args:
  uv run pytest {{args}}

# Test code and report coverage
[group('test')]
cov *args:
  uv run pytest --cov --cov-report=term --cov-report=html {{args}}

# Add dependency
[group('dependencies')]
add dep:
  uv add {{dep}}

# Add dependency to the development group
[group('dependencies')]
dev dep:
  uv add --dev {{dep}}

# Update dep to the newest ver allowed by pyproject.toml
[group('dependencies')]
up dep:
  uv lock --upgrade-package {{dep}}
  uv sync

# Update all dependencies
[group('dependencies')]
up-all:
  uv lock --upgrade
  uv sync

# List the outdated dependencies
[group('dependencies')]
out:
  uv pip list --outdated

# Lock/freeze dependencies
[group('dependencies')]
lock:
  uv lock

# Check, test, and build the distributions that CI will publish
#
# Depends on cov rather than on test because CI runs pytest under coverage and
# fails below the fail_under floor in pyproject.toml. Running the bare suite
# here left the gate that gets a push rejected as one this recipe never applied.
[group('deploy')]
build: lint cov
  #!/usr/bin/env bash
  set -euo pipefail
  uv build --clear
  # The same check the release workflow runs before it uploads, so that a
  # packaging mistake surfaces here rather than on a tag that cannot be undone.
  #
  # --isolated is what makes the environment the wheel lands in a clean one.
  # Without it uv layers the --with packages over the project's own .venv,
  # where every dependency is already installed, and a distribution that
  # failed to declare one would still import here. A runner has no .venv, so
  # only the local run needs it.
  uv run --isolated --no-project --with dist/*.whl \
    python scripts/smoke_test_wheel.py "$(uv version --short)"

# Confirm a release can be cut from the tree as it stands
[group('deploy')]
release-check:
  #!/usr/bin/env bash
  set -euo pipefail
  if [ -n "$(git status --porcelain)" ]; then
    echo "Working tree is dirty; commit or stash these first:" >&2
    git status --short >&2
    exit 1
  fi
  if [ "$(git branch --show-current)" != master ]; then
    echo "Releases are cut from master" >&2; exit 1
  fi
  behind="$(git rev-list --count HEAD..@{upstream} 2>/dev/null || echo 0)"
  if [ "$behind" != 0 ]; then
    echo "master is ${behind} commit(s) behind its upstream; pull first" >&2; exit 1
  fi
  if [ -z "$({{just_executable()}} unreleased)" ]; then
    echo "CHANGELOG.md has no entries under Unreleased" >&2; exit 1
  fi
  echo "Ready to release from $(uv version --short)."

# Cut a release
#
# Depends on cov rather than on test for the same reason build does: a tag is
# pushed on the strength of what these recipes checked, and coverage is one of
# the gates CI applies before it will publish that tag.
[group('deploy')]
release: release-check lint cov
  #!/usr/bin/env bash
  set -euo pipefail
  # release-check runs first, as a dependency, so that a dirty tree or an
  # empty Unreleased section is turned away immediately rather than after a
  # full lint and test run.
  unreleased="$({{just_executable()}} unreleased)"
  current="$(uv version --short)"
  echo
  echo "Releasing from ${current}, with these entries under Unreleased:"
  echo
  sed 's/^./    &/' <<<"$unreleased"
  echo
  echo "    1) patch   ${current} -> $(uv version --short --bump patch --dry-run)"
  echo "    2) minor   ${current} -> $(uv version --short --bump minor --dry-run)"
  echo "    3) major   ${current} -> $(uv version --short --bump major --dry-run)"
  echo "    q) cancel"
  echo
  read -r -p "Which release? [1] " choice
  case "${choice:-1}" in
    1|p|patch) bump=patch ;;
    2|m|minor) bump=minor ;;
    3|M|major) bump=major ;;
    q|Q) echo "Cancelled."; exit 0 ;;
    *) echo "Unrecognized choice: ${choice}" >&2; exit 1 ;;
  esac
  version="$(uv version --short --bump "$bump" --dry-run)"
  tag="v${version}"
  if git rev-parse -q --verify "refs/tags/${tag}" >/dev/null; then
    echo "Tag ${tag} already exists" >&2; exit 1
  fi
  uv version --bump "$bump" --no-sync
  uv lock --quiet
  VERSION="$version" python3 - <<'PY'
  import datetime, os, pathlib
  heading = f"## v{os.environ['VERSION']} - {datetime.date.today().isoformat()}"
  p = pathlib.Path("CHANGELOG.md")
  s = p.read_text()
  p.write_text(s.replace("## Unreleased\n", f"## Unreleased\n\n{heading}\n", 1))
  PY
  git commit -qam "Release ${tag}"
  git tag -a "${tag}" -m "${tag}"
  echo
  echo "Tagged ${tag}. Publish it with:"
  echo
  echo "    git push --follow-tags"

# Print the CHANGELOG entries sitting under Unreleased. Both release-check and
# release read this, one to refuse an empty section and the other to show what
# is about to ship, so it is written once here.
[private]
unreleased:
  #!/usr/bin/env python3
  import pathlib, re
  m = re.search(
      r"^## Unreleased\s*\n(.*?)(?=^## v)",
      pathlib.Path("CHANGELOG.md").read_text(),
      re.S | re.M,
  )
  print((m.group(1).strip() if m else ""))
