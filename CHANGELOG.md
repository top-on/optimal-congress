# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [unreleased]
### Removed
- Removed tox test setup, relying on `pytest` in CI pipeline instead.

## [1.1.1] - 2024-12-25
### Added
- Increased test coverage
- GitHub Actions for CI/CD

## [1.1.0] - 2024-12-24
### Added
- Ratings filter for choosing language of events to rate (e.g. `optimal-congress rate --language en`)
- CLI option to print software version

## [1.0.2] - 2024-12-12
### Fixed
- Replace 37c3 with 38c3

## [1.0.1] - 2024-12-12
### Fixed
- Update README

## [1.0.0] - 2024-12-12
### Changed
- Adapted to 2024's 38c3 congress
### Fixed
- Update outdated dependencies

## [0.7.4] - 2023-01-20
### Fixed
- update dependencies to patch CVE-2024-22421

## [0.7.3] - 2024-01-18
### Changed
- output ratings and optimization in table format
### Fixed
- bump dependencies with vulnerabilities

## [0.7.2] - 2024-01-03
### Fixed
- list requests as explicit dependency

## [0.7.1] - 2023-12-26
### Fixed
- turn off color if rich dependency is present, and enforce its presence

## [0.7.0] - 2023-12-24
### Added
- command 'next' to list upcoming events, filtered by minimum rating

## [0.6.1] - 2023-12-22
### Fixed
- better vertical alignment of presented optimization results

## [0.6.0] - 2023-12-22
### Added
- with optimization result, also show room name
### Changed
- at fetching, list new/removed based on event's UUID (disregarding changed properties)

## [0.5.1] - 2023-12-21
### Fixed
- make f-string syntax work also with python versions 3.10 and 3.11 (#1)

## [0.5.0] - 2023-12-18
### Added
- export and import ratings to/from to CSV
- -h flag can also be used for --help

## [0.4.0] - 2023-12-17
### Added
- dryrun option for fetch command
- option to require minimum rating for talks to be included in optimization
### Fixed
- update URLs to API endpoints

## [0.3.0] - 2023-12-15
### Changed
- when rating, show more relevant information
### Fixed
- fix optimization when rating has no corresponding event

## [0.2.0] - 2023-12-15
### Added
- report new and removed events when fetching from API
### Changed
- refactoring: make functions take/return set

## [0.1.0] - 2023-12-14
### Added
- implement MVP for fetching events, rating them, and optmizing personal schedule
