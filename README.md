# Democritus File System (Files and Directories)

[![PyPI](https://img.shields.io/pypi/v/d8s-file-system.svg)](https://pypi.python.org/pypi/d8s-file-system)
[![CI](https://github.com/democritus-project/d8s-file-system/workflows/CI/badge.svg)](https://github.com/democritus-project/d8s-file-system/actions)
[![Lint](https://github.com/democritus-project/d8s-file-system/workflows/Lint/badge.svg)](https://github.com/democritus-project/d8s-file-system/actions)
[![codecov](https://codecov.io/gh/democritus-project/d8s-file-system/branch/main/graph/badge.svg?token=V0WOIXRGMM)](https://codecov.io/gh/democritus-project/d8s-file-system)
[![The Democritus Project uses semver version 2.0.0](https://img.shields.io/badge/-semver%20v2.0.0-22bfda)](https://semver.org/spec/v2.0.0.html)
[![The Democritus Project uses black to format code](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![License: LGPL v3](https://img.shields.io/badge/License-LGPL%20v3-blue.svg)](https://choosealicense.com/licenses/lgpl-3.0/)

Democritus functions<sup>[1]</sup> for working with files and directories.

[1] Democritus functions are <i>simple, effective, modular, well-tested, and well-documented</i> Python functions.

We use `d8s` as an abbreviation for `democritus` (you can read more about this [here](https://github.com/democritus-project/roadmap#what-is-d8s)).

## Functions

  - ```python
    def is_file(path: str) -> bool:
        """Determine if the given path is a file."""
    ```
  - ```python
    def file_read(file_path: str) -> str:
        """Read the file at the given file_path as a string."""
    ```
  - ```python
    def file_read_bytes(file_path: str) -> bytes:
        """Read the file at the given file_path as bytes."""
    ```
  - ```python
    def file_write(file_path: str, file_contents: Any) -> bool:
        """Write the given content to the file at the given path (including a file name)."""
    ```
  - ```python
    def file_append(file_path: str, file_contents: Any) -> bool:
        """Append the given content to the file at the given path (including a file name)."""
    ```
  - ```python
    def file_move(starting_path: str, destination_path: str):
        """Move the file from the starting path to the destination path."""
    ```
  - ```python
    def file_copy(starting_path: str, destination_path: str, *, preserve_metadata: bool = False):
        """Copy the file from the starting_path to the destination path."""
    ```
  - ```python
    def file_delete(file_path: str):
        """Delete the given file."""
    ```
  - ```python
    def file_owner_name(file_path: str) -> str:
        """Find the owner of the file at the given path."""
    ```
  - ```python
    def file_change_owner(file_path: str):
        """Change the ownership of the given file."""
    ```
  - ```python
    def file_ssdeep(file_path: str) -> str:
        """Find the ssdeep fuzzy hash of the file."""
    ```
  - ```python
    def file_md5(file_path: str) -> str:
        """Find the md5 hash of the given file."""
    ```
  - ```python
    def file_sha1(file_path: str) -> str:
        """Find the sha1 hash of the given file."""
    ```
  - ```python
    def file_sha256(file_path: str) -> str:
        """Find the sha256 hash of the given file."""
    ```
  - ```python
    def file_sha512(file_path: str) -> str:
        """Find the sha512 hash of the given file."""
    ```
  - ```python
    def file_name_escape(file_name_arg: str) -> str:
        """Escape the name of a file so that it can be used as a file name in a file path."""
    ```
  - ```python
    def file_name(file_path: str) -> str:
        """Find the file name from the given file path."""
    ```
  - ```python
    def file_name_windows(windows_file_path: str) -> str:
        """Find the file name from the given windows_file_path."""
    ```
  - ```python
    def file_name_unix(unix_file_path: str) -> str:
        """Find the file name from the given unix_file_path."""
    ```
  - ```python
    def file_size(file_path: str) -> int:
        """Find the file size."""
    ```
  - ```python
    def file_directory(file_path: str) -> str:
        """Return the directory in which the given file resides."""
    ```
  - ```python
    def file_details(file_path: str) -> Dict[str, Union[str, int]]:
        """Get file hashes and file size for the given file."""
    ```
  - ```python
    def file_exists(file_path: str) -> bool:
        """Check if the file exists."""
    ```
  - ```python
    def file_is_readable(file_path: str) -> bool:
        """Check if the file is readable."""
    ```
  - ```python
    def file_is_writable(file_path: str) -> bool:
        """Check if the file is writable."""
    ```
  - ```python
    def file_is_executable(file_path: str) -> bool:
        """Check if the file is executable."""
    ```
  - ```python
    def file_contains(file_path: str, pattern: str, *, pattern_is_regex: bool = False) -> bool:
        """Return whether or not the file contains the given pattern."""
    ```
  - ```python
    def file_search(file_path: str, pattern: str, *, pattern_is_regex: bool = False) -> List[str]:
        """Search for the given pattern in the file."""
    ```
  - ```python
    def file_name_matches(file_path: str, pattern: str) -> bool:
        """Return whether or not the file name contains the given pattern."""
    ```
  - ```python
    def is_directory(path: str) -> bool:
        """Determine if the given path is a directory."""
    ```
  - ```python
    def directory_exists(directory_path: str) -> bool:
        """Check if the directory exists."""
    ```
  - ```python
    def directory_file_names(directory_path: str, *, recursive: bool = False) -> List[str]:
        """List files at the given directory_path."""
    ```
  - ```python
    def directory_file_paths(directory_path: str, *, recursive: bool = False) -> List[str]:
        """List the file paths at the given directory_path."""
    ```
  - ```python
    def directory_copy(src_path: str, dst_path: str):
        """Copy the directory from the src_path to the destination path."""
    ```
  - ```python
    def directory_delete(directory_path: str):
        """Delete the given directory."""
    ```
  - ```python
    def directory_create(directory_path: str, mode=0o777):
        """Create a directory."""
    ```
  - ```python
    def directory_disk_usage(directory_path: str):
        """Return the disk usage for the given directory."""
    ```
  - ```python
    def directory_disk_free_space(directory_path: str):
        """Return the free space in the given directory."""
    ```
  - ```python
    def directory_disk_used_space(directory_path: str):
        """Return the used space in the given directory."""
    ```
  - ```python
    def directory_disk_total_space(directory_path: str):
        """Return the total space in the given directory."""
    ```
  - ```python
    def home_directory() -> str:
        """Return the home directory."""
    ```
  - ```python
    def home_directory_join(path: str) -> str:
        """Join the given path with the home directory."""
    ```
  - ```python
    def directory_move(src_path: str, dst_path: str):
        """Move the directory from the src_path to the dst_path."""
    ```
  - ```python
    def directory_files_details(directory_path: str, *, recursive: bool = False) -> Dict[str, Dict[str, Union[str, int]]]:
        """Return the file details for each file in the directory at the given path."""
    ```
  - ```python
    def directory_files_read(directory_path: str, *, recursive: bool = False) -> Iterable[Tuple[str, str]]:
        """Read all files in the directory_path."""
    ```
  - ```python
    def directory_subdirectory_names(directory_path: str, *, recursive: bool = False) -> List[str]:
        """List the names of all subdirectories in the given directory."""
    ```
  - ```python
    def directory_files_containing(
        directory_path: str, pattern: str, *, pattern_is_regex: bool = False, recursive: bool = False
    ) -> Dict[str, List[str]]:
        """Search for the given pattern in all files in the given directory_path."""
    ```
  - ```python
    def directory_file_paths_matching(directory_path: str, pattern: str, *, recursive: bool = False) -> List[str]:
        """Return the paths of all of the files in the given directory which match the pattern."""
    ```
  - ```python
    def directory_file_names_matching(directory_path: str, pattern: str, *, recursive: bool = False) -> List[str]:
        """Return the names of all of the files in the given directory which match the pattern."""
    ```
  - ```python
    def directory_read_files_with_path_matching(
        directory_path: str, pattern: str, *, recursive: bool = False
    ) -> Iterable[Tuple[str, str]]:
        """Read all of the files in the given directory whose paths match the given pattern."""
    ```
  - ```python
    def atomic_write(fpath, *, overwrite: bool = True, **cls_kwargs):
        """Create a context manager to write atomically using the AtomicWriterPerms class to update file permissions."""
    ```

## Development

👋 &nbsp;If you want to get involved in this project, we have some short, helpful guides below:

- [contribute to this project 🥇][contributing]
- [test it 🧪][local-dev]
- [lint it 🧹][local-dev]
- [explore it 🔭][local-dev]

If you have any questions or there is anything we did not cover, please raise an issue and we'll be happy to help.

## Credits

This package was created with [Cookiecutter](https://github.com/audreyr/cookiecutter) and Floyd Hightower's [Python project template](https://github.com/fhightower-templates/python-project-template).

[contributing]: https://github.com/democritus-project/.github/blob/main/CONTRIBUTING.md#contributing-a-pr-
[local-dev]: https://github.com/democritus-project/.github/blob/main/CONTRIBUTING.md#local-development-
