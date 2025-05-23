# File Loader

A Python tool for managing and copying files using `.gitignore`-style pattern matching.

## Features

- List files while respecting ignore patterns (similar to `.gitignore`)
- Copy filtered files to a target directory
- Support for multiple ignore pattern files
- Dry-run mode for copy operations

## Installation

```bash
# Using pip
pip install ignorely

# Using Poetry
poetry install
```

## Usage

### List Files

List files while excluding patterns from ignore files:

```bash
ignorely ls-files -f ./path/to/output.txt
```

Options:
- `-f, --file`: Output file path to save the file list
- `-i, --ignore`: Additional ignore pattern files (can be used multiple times)

### Copy Files

Copy files while respecting ignore patterns:

```bash
ignorely copy-files ./target/directory
```

Options:
- `-i, --ignore`: Additional ignore pattern files (can be used multiple times)
- `--dry-run`: Preview which files would be copied without actually copying
- `-f, --file`: Input file containing the list of files to copy

## Example

```bash
# List files and save to files.txt
ignorely ls-files -f ./dev/files.txt

# Copy files based on the generated list
ignorely copy-files ./dev/copied
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
