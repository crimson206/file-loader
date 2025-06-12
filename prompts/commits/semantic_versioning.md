# Semantic Versioning Rules

Version format: **MAJOR.MINOR.PATCH** (e.g., 1.0.0)

## Version Update Rules

1. **MAJOR version** (Breaking Change)
   - Incompatible API changes
   - Major modifications or removals
   - Changes to core interfaces or primary functions
   - Changes that affect public API contracts
   - Examples: 
     - Modifying main function signatures
     - Changing core interface structures
     - Removing or renaming primary APIs
   - Example: 1.0.0 → 2.0.0

2. **MINOR version** (Feature)
   - Backwards-compatible functionality additions
   - Improvements to existing features
   - Changes to helper functions or utilities
   - Examples:
     - Adding new utility functions
     - Modifying internal helper methods
     - Extending existing utility interfaces
   - Example: 1.0.0 → 1.1.0

3. **PATCH version** (Fix)
   - Backwards-compatible bug fixes
   - Performance improvements
   - Example: 1.0.0 → 1.0.1

## Relationship with Conventional Commits

- `BREAKING CHANGE` → **MAJOR** version up
- `feat:` → **MINOR** version up
- `fix:` → **PATCH** version up
