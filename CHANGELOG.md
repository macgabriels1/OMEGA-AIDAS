# Changelog

All notable changes to this project will be documented in this file.

## v1.0.3 (2025-04-28)
- Fixed CI configuration to prevent Python CI from running on tag pushes.
- Added Bandit security scan job with suppression of false positives.
- Introduced automated release workflow to build and publish to PyPI on new tags.
- Updated package version to 1.0.3 in `setup.py`.

## v1.0.2 (2025-04-27)
- Prevented Python CI from running on tag pushes.
- Added `release.yml` workflow to automate PyPI publication.
- Updated `.flake8` configuration to ignore generated and third-party code.

## v1.0.1 (2025-04-26)
- Added initial CI workflow (`python-ci.yml`) with linting, security scanning, and a test matrix.

## Installation

```bash
pip install omega-aidas==1.0.3