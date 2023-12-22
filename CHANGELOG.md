# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [unreleased]
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
