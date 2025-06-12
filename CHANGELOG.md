# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [3.0.0] - 2024-06-12

### Breaking Changes
- Changed `.ignorely` directory structure to be more flexible
  - `.ignorely` folder can now be placed anywhere (default: `.ignorely/`)
  - No longer requires nested `.ignorely` folder structure
  - Configuration files (`exclude_tot`, `include_tot`) are now optional

### Added
- New `init` command to create ignorely configuration
- Default ignore patterns in `.excludes`
- Default include patterns in `.includes`
- More graceful handling when configuration files are missing

### Changed
- Default `ignorely-dir` location changed to `.ignorely`
- Unified error handling across all commands
- Improved error messages and user feedback
- Updated command descriptions to reflect new structure

### Migration Guide
If you're upgrading from 2.x:
1. Run `ignorely init` in your project root
2. Move your existing patterns from `.ignorely/.ignorely/*` to `.ignorely/*`
3. Update any scripts that rely on the old directory structure 