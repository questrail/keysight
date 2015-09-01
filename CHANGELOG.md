# CHANGELOG.md
This file contains all notable changes to the [keysight][] project.

## Unreleased

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

### Bugs
- Removed Python 3.3/3.4 from Travis-CI since those builds are currently
  failing.

## v0.1.1 - 2014-08-15

### Enhancments
- Add Travis-CI, gitignore, and Coveralls

## v0.1 - 2014-08-15

### Enhancements
- Initial release passes with unit tests for a sample produced by a
  N9340B spectrum analyzer CSV

[keysight]: https://github.com/questrail/keysight
