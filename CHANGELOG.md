# CHANGELOG.md

This file contains all notable changes to the [keysight][] project.

## Unreleased

### Changed

- Build with [uv_build][] rather than hatchling. hatchling arrived in v1.5.0 as
  the replacement for setuptools, months before uv had a build backend of its
  own; uv already manages and locks this project, so the backend is one fewer
  tool in the build. The `[tool.hatch.build.targets.wheel]` stanza it needed is
  gone, since `src/keysight` is what uv_build looks for by default. The wheel is
  file for file what hatchling produced.
- Pin the build backend to a minor range. `[build-system] requires` is not part
  of `uv.lock`, so an unpinned backend was resolved fresh on every build,
  including the release run that produces the attested distributions. It was the
  one input to the published wheel that nothing held still, next to actions
  pinned to commit SHAs and dependencies installed with `uv sync --locked`.
- Ship a minimal source distribution. uv_build includes the module, README,
  LICENSE, and `pyproject.toml`, where hatchling had included everything git
  tracks. The wheel is unchanged; what the sdist no longer carries is the test
  suite, its sample data, and `uv.lock`, so it is no longer enough on its own to
  check that the readers still parse the instrument files.

### Fixed

- Ignore `.DS_Store`. It had only ever been ignored through a global git config
  on the author machine, so nothing stopped a contributor from committing one
  into `src/`, where the build would carry it into both distributions.

## v2.0.0 - 2026-09-02

### Added

- Publish from GitHub Actions using [trusted publishing][]. There is no PyPI
  API token anywhere: the release workflow mints a short lived credential
  from the GitHub OIDC identity of that run, and signs a [PEP 740][]
  attestation for each distribution against the same identity, which PyPI
  serves beside the file it attests. Releases had been uploaded by hand with
  `hatch publish` from a task that also pushed the tag, so nothing stood
  behind who uploaded or what was built.
- Wait on the whole CI workflow before publishing. `release.yml` calls
  `ci.yml` rather than rechecking what it can reach itself, so a tag cannot
  publish what the 3.12, 3.13, and 3.14 matrix and the dependency floor job
  have not checked. It then verifies the tagged commit is on `master`, since
  a tag is only a pointer and one placed anywhere else would otherwise
  publish whatever it points at, and rechecks the tag against the version in
  `pyproject.toml`.
- Smoke test the built wheel from outside the source tree. Every other check
  runs against `src/`, so a packaging mistake that leaves a module or
  `py.typed` out of the distribution passed all of them and shipped anyway.
  `scripts/smoke_test_wheel.py` installs the wheel where `src/` cannot be
  reached and reaches for every module through the package, and both
  `just build` and the release workflow run it.
- Add a `just release` recipe that cuts the release. It refuses a dirty
  working tree, a branch other than `master`, a `master` behind its upstream,
  an empty Unreleased section, and a tag that already exists, all before it
  lints and tests, then shows the entries waiting under Unreleased next to
  the version each kind of bump would produce and asks which to cut. The
  `invoke release` task it replaces took the version as an argument and
  trusted it, and printed a checklist of questions in place of checking
  anything.
- Test the lowest dependency versions `pyproject.toml` allows in a CI job of
  its own. The version floor is a promise to anyone installing keysight
  alongside something else that holds numpy back, and the matrix never tested
  it: it installs whatever `uv.lock` pins, which is the newest numpy rather
  than the oldest allowed one.
- Audit the workflows with [zizmor][] in CI and in `just lint`, so that
  everything the release path depends on is checked by something other than
  reading it.
- Put the actions and the Python dependencies under [Dependabot][], monthly.
  The actions are pinned to commit SHAs, so without this, pinning would
  amount to staying on one commit forever.
- Ship `py.typed` and annotate the public functions, so that the types reach
  anyone type checking against this package.
- Report coverage to [Coveralls][coveralls link] from CI, with the suite
  failing under 100% statement and branch coverage.
- `just release-check`, which runs the refusals `just release` opens with and
  stops there: a dirty working tree, a branch other than `master`, a `master`
  behind its upstream, an empty `Unreleased` section. Asking whether a release
  can be cut no longer means starting one and reading the error.
- `just doc`, which searches pydoc for a given term.
- Ignore `.pypirc`. A copy holding a PyPI username and password predates the
  move to trusted publishing, which mints a short lived credential per
  release and leaves nothing on disk; nothing here needs the file, and
  ignoring it keeps a leftover from being committed by accident.

### Changed

- Require Python 3.12 or newer. The package had claimed 3.9 while the test
  suite ran on whatever was installed and CI ran on nothing at all, since
  Travis had been dead for years.
- Manage the project with [uv][] and drive it with [Just][], replacing pip,
  a hand held virtualenv, `requirements.txt`, and the [Invoke][] tasks. The
  dependencies are resolved into `uv.lock`, which is what CI installs with
  `uv sync --locked`, so a local run and a CI run install the same versions.
- Run the suite with [pytest][] rather than nose2, and reach the sample files
  through `pathlib` rather than [unipath][], which was an undeclared test
  dependency and has not been released since 2013. The three near identical
  N9340 test modules are now one parametrized module, which also covers the
  `TST.CSV` sample that nothing had been reading.
- Lint and format with [ruff][] and type check with [pyright][], both pinned
  in `uv.lock` and reached through `uv run`, replacing black, pylint, and
  mypy. The pyright settings had been copied from another project and pointed
  at a `tektronix` virtualenv and directories that do not exist here.
- Read any number of traces in the `e4411b` and `n9038` modules. `e4411b`
  handled 1, 2, or 3 traces and `n9038` handled 1 or 6, each spelled out as a
  branch per count.
- Replace the N9038 header parse with a table of fields in file order. It had
  been 60 lines of `mynext()` calls whose alignment with the file was
  impossible to check by eye.
- `just build` and `just release` depend on `cov` rather than `test`. CI runs
  pytest under coverage and fails below the `fail_under` floor in
  `pyproject.toml`, so the bare suite these recipes ran left that gate as one
  they never applied: a tree that passed locally could still be rejected on
  push, and `just release` could tag a version CI would then refuse to publish.
- The CHANGELOG parser that reads the `Unreleased` section moved out of
  `release` and into a private `unreleased` recipe. `release-check` and
  `release` both read it, one to refuse an empty section and the other to show
  what is about to ship, so it is written once rather than inlined in each.
- Bring the `LICENSE.txt` copyright range up to 2026. It had stopped at
  2022, years behind the work in the file.
- Promote "Releasing to PyPI" in the README from a fourth level heading to a
  third. It had been nested under "Development Setup on macOS", which made
  releasing look like a macOS specific topic.

### Fixed

- A file naming a trace count that the reader had no branch for returned the
  spent CSV reader in place of an array, so the failure surfaced wherever the
  caller first indexed the result. Such a file now raises `ValueError` while
  reading it.
- The N9340 reader no longer opens files through a Python 2 compatibility
  branch. Python 2 support was dropped in v1.5.0, and `sys.version_info`
  checks were left behind guarding a `csv.reader` call that could never run.

### Removed

- The unused, undocumented `_get_ref()` copy in the `n9038` module, which was
  a duplicate of the `n9340` one and was never called.
- `AUTHORS.md`, and the "(see AUTHORS.md file)" clause in `LICENSE.txt` that
  pointed at it. It listed one author with "None at this time" under both
  Maintainers and Contributors, which `pyproject.toml` already records in
  its `authors` field.

## v1.5.0 - 2024-12-05

### Changed

- Build and publish with hatch instead of setuptools.
- Update the dependencies and the lint task.

### Removed

- Python 2.x support.

## v1.4.3 - 2022-05-23

- v1.4.2 wasn't released to pypi.
- Added twine to dependencies.

## v1.4.2 - 2022-05-23

- v1.4.1 wasn't released to pypi.
- Added build to dependencies.
- Switched to pip-chill vs pip freeze.

## v1.4.1 - 2022-05-23

- Add N9038A.
- Change from Nose to Nose2.

## v1.3.0 - 2022-05-23

- Not released.

## v1.2.2 - 2021-12-16

- Installed build and twine. Froze requirements.

## v1.2.1 - 2021-12-16

- Change description-file to description_file in setup.cfg.

## v1.2.0 - 2021-12-16

- Update build and PyPI distribution process.
- Update copyright for 2022.
- Update dependencies in requirements.txt.

## v1.1.0 - 2018-01-11

### Fixed

- Handle case where N9340 file has a marker.

## v1.0.1 - 2018-01-09

### Fixed

- Return the proper ref if it has units of dBm or dBuV.

## v1.0.0 - 2018-01-09

### Changed

- Don't auto deplay using Travis, since that's problematic.

## v0.6.1 - 2018-01-09

### Changed

- Changed Python versions to 2.7, 3.4, 3.5, and 3.6.

## v0.6.0 - 2018-01-09

### Fixed

- If the N9340 data file has units on the ref value in the CSV, then
  return just the value and don't throw an exception.

## v0.5.1 - 2016-10-05

### Fixed

- Ability to handle 1-3 traces on E4411B

## v0.5.0 - 2016-10-04

### Added

- Ability to handle 1-3 traces instead of just 1 trace

## v0.4.1 - 2016-10-04

### Added

- Ability to run on Python 3.3+ in addition to Python 2.6+

## v0.3.0 - 2015-09-01

### Added

- Ability to parse CSV files from E4411B Spectrum Analyzer

## v0.2.1 - 2015-08-20

### Added

- Added coverage to `inv test` task

### Changed

- Updated pip requirements including numpy
- Migrated from Travis legacy to container-based infrastructure
- Remove pypi deploy from `inv release` task and use Travis instead

## v0.1.2 - 2014-08-15

### Fixed

- Removed Python 3.3/3.4 from Travis-CI since those builds are currently
  failing.

## v0.1.1 - 2014-08-15

### Added

- Add Travis-CI, gitignore, and Coveralls

## v0.1 - 2014-08-15

### Added

- Initial release passes with unit tests for a sample produced by a
  N9340B spectrum analyzer CSV

[coveralls link]: https://coveralls.io/github/questrail/keysight?branch=master
[Dependabot]: https://docs.github.com/en/code-security/dependabot
[Invoke]: https://www.pyinvoke.org/
[just]: https://just.systems/
[keysight]: https://github.com/questrail/keysight
[PEP 740]: https://peps.python.org/pep-0740/
[pyright]: https://microsoft.github.io/pyright/
[pytest]: https://docs.pytest.org/
[ruff]: https://docs.astral.sh/ruff/
[trusted publishing]: https://docs.pypi.org/trusted-publishers/
[unipath]: https://github.com/mikeorr/Unipath
[uv_build]: https://docs.astral.sh/uv/concepts/build-backend/
[uv]: https://docs.astral.sh/uv/
[zizmor]: https://docs.zizmor.sh/
