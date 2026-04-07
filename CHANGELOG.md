# Changelog

All notable changes to this project will be documented in this file.
## [Unreleased]

### Bug Fixes

- **nnote**: Version string

### CI

- Replace changelog commit job with release notes update

### Documentation

- Add license section to README
- Add changelog link to README

### Features

- **commands**: Add move command

### Miscellaneous

- Add automated changelog generation with git-cliff
- Configure README as PyPI long description
- Release v0.1.2

### Testing

- **commands**: Add test suite for the command move

## [0.1.1]

### Documentation

- LICENSE

### Miscellaneous

- **config**: Exclude test from the package
- Release v0.1.1

## [0.1.0]

### Documentation

- Enhance readme

### Features

- Init
- Implement notes dir config via init command
- Implement note creation via new command
- Implement command new, edit, drop
- **cli**: The command list
- Search command and algorithm
- **ci**: Add workflow to publish to PyPi on release

### Miscellaneous

- Change default notes dir to ~/nnotes
- **config**: Migrate to pyproject.toml

### Refactoring

- Split cli.py into command packs

### Testing

- Add pytest suite for config, notes, and search modules


