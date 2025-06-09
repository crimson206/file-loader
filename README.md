# Ignorely

A flexible CLI tool for filtering and copying files using include/exclude patterns, similar to Git's ignore functionality.

## Features

- **File Filtering**: List files using include/exclude patterns
- **File Copying**: Copy filtered files with various options
- **Unified Export**: Filter and copy files in one command
- **Pattern Management**: Support for multiple pattern files via table-of-contents files
- **Flexible Output**: Support for flat or hierarchical directory structures
- **Dry Run Mode**: Preview operations before executing

## Installation

```bash
pip install ignorely
```

Or install from source:
```bash
git clone <repository-url>
cd ignorely
pip install .
```

## Quick Start

1. Create pattern files in `.ignorely/` directory:
   ```bash
   mkdir .ignorely
   echo ".gitignore" > .ignorely/exclude_tot
   echo "include_patterns.txt" > .ignorely/include_tot
   ```

2. List filtered files:
   ```bash
   ignorely ls-files
   ```

3. Export filtered files to a directory:
   ```bash
   ignorely export-files output/
   ```

## Commands

### `ls-files` - List filtered files

List files with include/exclude filtering.

```bash
ignorely ls-files [OPTIONS]
```

**Options:**
- `-o, --output FILE`: Save output to file instead of displaying
- `-e, --exclude-tot FILE`: File containing exclude pattern files (default: `.ignorely/exclude_tot`)
- `-i, --include-tot FILE`: File containing include pattern files (default: `.ignorely/include_tot`)

**Examples:**
```bash
# List all filtered files
ignorely ls-files

# Save file list to output.txt
ignorely ls-files -o output.txt

# Use custom pattern files
ignorely ls-files -e custom_exclude.txt -i custom_include.txt
```

### `copy-files` - Copy files from list

Copy files to output directory based on provided file list.

```bash
ignorely copy-files OUTPUT_DIR [OPTIONS]
```

**Options:**
- `-l, --list-file FILE`: Read file list from file
- `-d, --dry-run`: Show what would be copied without actually copying
- `--flatten`: Flatten directory structure using divider in filenames
- `--divider CHAR`: Character to use as path divider when flattening (default: `%`)
- `-c, --clean`: Clean (remove) output directory before copying

**Examples:**
```bash
# Copy files from stdin
ignorely ls-files | ignorely copy-files output/

# Copy files from file list
ignorely copy-files output/ -l files.txt

# Dry run to preview operations
ignorely copy-files output/ -l files.txt --dry-run

# Flatten directory structure
ignorely copy-files output/ -l files.txt --flatten

# Clean output directory before copying
ignorely copy-files output/ -l files.txt --clean
```

### `export-files` - Filter and copy in one step

Combines `ls-files` and `copy-files` functionality.

```bash
ignorely export-files OUTPUT_DIR [OPTIONS]
```

**Options:**
- `-e, --exclude-tot FILE`: File containing exclude pattern files (default: `.ignorely/exclude_tot`)
- `-i, --include-tot FILE`: File containing include pattern files (default: `.ignorely/include_tot`)
- `-d, --dry-run`: Show what would be copied without actually copying
- `--flatten`: Flatten directory structure using divider in filenames
- `--divider CHAR`: Character to use as path divider when flattening (default: `%`)
- `-c, --clean`: Clean (remove) output directory before copying

**Examples:**
```bash
# Export filtered files
ignorely export-files output/

# Export with flattened structure
ignorely export-files output/ --flatten

# Dry run export
ignorely export-files output/ --dry-run

# Clean and export
ignorely export-files output/ --clean
```

## Pattern Files

Ignorely uses "table-of-contents" files to manage multiple pattern files:

### Exclude Table-of-Contents (`.ignorely/exclude_tot`)
Lists pattern files containing exclusion rules:
```
.gitignore
.dockerignore
custom_exclude.txt
```

### Include Table-of-Contents (`.ignorely/include_tot`)
Lists pattern files containing inclusion rules:
```
include_patterns.txt
important_files.txt
```

### Pattern File Format
Pattern files use Git-style wildcard patterns:
```
# This is a comment
*.log
temp/
**/node_modules/
!important.log
```

## Pattern Matching

Ignorely uses the same pattern matching as Git:
- `*`: Matches any number of characters except `/`
- `**`: Matches any number of characters including `/`
- `?`: Matches any single character except `/`
- `!`: Negates a pattern (include instead of exclude)
- `#`: Comments (ignored)

## Examples

### Basic Usage
```bash
# Create basic setup
mkdir .ignorely
echo ".gitignore" > .ignorely/exclude_tot
echo "*.py" > include_python.txt
echo "include_python.txt" > .ignorely/include_tot

# List Python files not in .gitignore
ignorely ls-files

# Export Python files to dist/
ignorely export-files dist/
```

### Advanced Filtering
```bash
# Multiple exclude patterns
cat > .ignorely/exclude_tot << EOF
.gitignore
.dockerignore
build_ignore.txt
EOF

# Multiple include patterns
cat > .ignorely/include_tot << EOF
source_files.txt
docs_files.txt
EOF

# Export with flattened structure
ignorely export-files release/ --flatten --divider=__
```

### Pipeline Usage
```bash
# Filter and process files
ignorely ls-files | grep "\.py$" | ignorely copy-files python_files/

# Export specific patterns
ignorely export-files backup/ -e custom_exclude.txt
```

## Dependencies

- **cleo**: CLI framework
- **pathspec**: Git-style pattern matching

## Requirements

- Python >= 3.10

## License

[Add your license information here]

## Contributing

[Add contributing guidelines here]
