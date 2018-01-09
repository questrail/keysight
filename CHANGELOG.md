# CHANGELOG.md
This file contains all notable changes to the [keysight][] project.

## Unreleased

## v1.0.0 - 09-Jan-18

### Changed
- Don't auto deplay using Travis, since that's problematic.

## v0.6.1 - 09-Jan-18

### Changed
- Changed Python versions to 2.7, 3.4, 3.5, and 3.6.

## v0.6.0 - 09-Jan-18

### Fixed
- If the N9340 data file has units on the ref value in the CSV, then
  return just the value and don't throw an exception.

## v0.5.1 - 05-Oct-16

### Fixed
- Ability to handle 1-3 traces on E4411B

## v0.5.0 - 04-Oct-16

### Added
- Ability to handle 1-3 traces instead of just 1 trace

## v0.4.1 - 04-Oct-16

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
