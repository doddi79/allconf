# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).


## [4.0.1] - 2026-11-13

### Added

- A task-oriented public API index in `docs/api-index.md`, linked from the README

### Changed

- Rewrote the README to document the main features, replacing the "I'll document this later" placeholder
- CI now tests on Python 3.10-3.13 (as required by `batutils` 2.x) instead of 3.8-3.12

### Removed

- The `integration-tests` CI job, which ran a `tests/withfidelius` directory that was removed in 4.0.0
- Python 3.8 and 3.9 from the package classifiers


## [4.0.0] - 2024-11-15

## Added

- Forked project and renamed module
