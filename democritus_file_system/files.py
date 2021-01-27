import fnmatch
import os
import posixpath
import ntpath
import shutil
import sys
import tempfile
from typing import Any, Dict, Union, List

from .atomic_writes import atomic_write


def _file_active_action(file_path: str, base_mode: str, file_contents: Any):
    """Perform an active action (write or append) with the given file contents on the given file."""
    if isinstance(file_contents, str):
        length_of_content = _file_action(file_path, '{}+'.format(base_mode), 'write', file_contents)
    elif isinstance(file_contents, bytes):
        length_of_content = _file_action(file_path, '{}b+'.format(base_mode), 'write', file_contents)
    else:
        print(f'Converting file contents of type {type(file_contents)} to string')
        length_of_content = _file_active_action(file_path, base_mode, str(file_contents))

    if length_of_content >= 0:
        result = True
    else:
        # I'm not sure if there are any cases in which this would occur, but just have it here for safety
        result = False

    return result


def _file_action(file_path, mode='r', command='read', contents=None):
    if 'w' in mode:
        with atomic_write(file_path, mode=mode) as f:
            return eval(f'f.{command}(contents)')
    else:
        with open(file_path, mode) as f:
            if contents:
                return eval(f'f.{command}(contents)')
            else:
                return eval(f'f.{command}()')


def is_file(path: str) -> bool:
    """Determine if the given path is a file."""
    return os.path.isfile(path)


def file_read(file_path: str) -> str:
    file_text = _file_action(file_path, 'r', 'read')
    return file_text


def file_read_bytes(file_path: str) -> bytes:
    file_text = _file_action(file_path, 'rb', 'read')
    return file_text


def file_write(file_path: str, file_contents: Any) -> bool:
    """Write the given content to the file at the given path (including a file name)."""
    result = _file_active_action(file_path, 'w', file_contents)
    return result


def file_append(file_path: str, file_contents: Any) -> bool:
    """Append the given content to the file at the given path (including a file name)."""
    result = _file_active_action(file_path, 'a', file_contents)
    return result


def file_move(starting_path: str, destination_path: str):
    """Move the file from the starting path to the destination path."""
    # TODO: this function could also be called "file_rename" - add a tag so that this function shows up if someone searches for "rename"
    shutil.move(starting_path, destination_path)


def file_copy(starting_path: str, destination_path: str, *, preserve_metadata: bool = False):
    """Copy the file from the starting_path to the destination path."""
    if preserve_metadata:
        shutil.copy2(starting_path, destination_path)
    else:
        shutil.copy(starting_path, destination_path)


def file_delete(file_path: str):
    """Delete the given file."""
    os.remove(file_path)


def file_owner_name(file_path: str) -> str:
    """Find the owner of the file at the given path."""
    # TODO: I believe this function only works for unix systems; update it (or write a corresponding function) to work on windows too
    from pwd import getpwuid

    file_owner_uid = os.stat(file_path).st_uid
    owner_username = getpwuid(file_owner_uid).pw_name
    return owner_username


# TODO: this function could also be called `fileChown` or `directory...`
# TODO: write a test for this function
def file_change_owner(file_path: str):
    """Change the ownership of the given file."""
    shutil.chown(file_path)


def file_ssdeep(file_path: str) -> str:
    """Find the ssdeep fuzzy hash of the file."""
    from democritus_hashes import ssdeep

    return ssdeep(file_read_bytes(file_path))


def file_md5(file_path: str) -> str:
    """Find the md5 hash of the given file."""
    from democritus_hashes import md5

    return md5(file_read_bytes(file_path))


def file_sha1(file_path: str) -> str:
    """Find the sha1 hash of the given file."""
    from democritus_hashes import sha1

    return sha1(file_read_bytes(file_path))


def file_sha256(file_path: str) -> str:
    """Find the sha256 hash of the given file."""
    from democritus_hashes import sha256

    return sha256(file_read_bytes(file_path))


def file_sha512(file_path: str) -> str:
    """Find the sha512 hash of the given file."""
    from democritus_hashes import sha512

    return sha512(file_read_bytes(file_path))


def file_name_escape(file_name: str) -> str:
    """Escape the name of a file so that it can be used as a file name in a file path."""
    import urllib.parse as urlparse

    # TODO: I should probably make an 'unescape' file

    url_encoded_file_name = urlparse.quote_plus(file_name)
    return url_encoded_file_name


def file_name(file_path: str) -> str:
    """Find the file name from the given file path."""
    return os.path.basename(file_path)


def file_name_windows(windows_file_path: str) -> str:
    """Find the file name from the given windows_file_path."""
    return ntpath.basename(windows_file_path)


def file_name_unix(unix_file_path: str) -> str:
    """Find the file name from the given unix_file_path."""
    return posixpath.basename(unix_file_path)


def file_size(file_path: str) -> int:
    """Find the file size."""
    return os.stat(file_path).st_size


def file_directory(file_path: str) -> str:
    """Return the directory in which the given file resides."""
    return file_path.replace(file_name(file_path), '')


def file_details(file_path: str) -> Dict[str, Union[str, int]]:
    """Get file hashes and file size for the given file."""
    file_details = {
        'md5': file_md5(file_path),
        'sha1': file_sha1(file_path),
        'sha256': file_sha256(file_path),
        'ssdeep': file_ssdeep(file_path),
        'size': file_size(file_path),
    }
    return file_details


def file_exists(file_path: str) -> bool:
    """Check if the file exists."""
    return os.access(file_path, os.F_OK)


def file_is_readable(file_path: str) -> bool:
    """Check if the file is readable."""
    return os.access(file_path, os.R_OK)


def file_is_writable(file_path: str) -> bool:
    """Check if the file is writable."""
    return os.access(file_path, os.W_OK)


def file_is_executable(file_path: str) -> bool:
    """Check if the file is executable."""
    return os.access(file_path, os.X_OK)


def file_contains(file_path: str, pattern: str, *, pattern_is_regex: bool = False) -> bool:
    """Return whether or not the file contains the given pattern."""
    result = file_search(file_path, pattern, pattern_is_regex=pattern_is_regex)
    return any(result)


def file_search(file_path: str, pattern: str, *, pattern_is_regex: bool = False) -> List[str]:
    """Search for the given pattern in the file."""
    import re

    file_text = file_read(file_path)
    if pattern_is_regex:
        return re.findall(pattern, file_text)
    else:
        return [pattern] * file_text.count(pattern)


def file_name_matches(file_path: str, pattern: str) -> bool:
    """Return whether or not the file name contains the given pattern."""
    name = file_name(file_path)
    return fnmatch.fnmatch(name, pattern)


def temp_file_create(**kwargs) -> str:
    """Create a temporary file."""
    return tempfile.TemporaryFile(**kwargs)
