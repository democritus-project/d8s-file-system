import os
import shutil
import tempfile
from typing import Any, Dict, Iterable, Tuple, Union, List, Dict

# TODO: test and standardize what happens if these functions are given a directory which does not exist
# TODO: may want to convert some of these functions to use this library: https://pypi.org/project/path.py/
# TODO: Write a function to change the permissions on a file (approx. chmod - https://www.tutorialspoint.com/unix/unix-file-permission.htm)
# TODO: add decorators to these functions (e.g. map_first_arg decorator to file functions)


def is_directory(path: str) -> bool:
    """Determine if the given path is a directory."""
    return os.path.isdir(path) or False


def directory_exists(directory_path: str) -> bool:
    """Check if the directory exists."""
    return os.path.isdir(directory_path) or False


def directory_file_names(directory_path: str, *, recursive: bool = True) -> List[str]:
    """List files at the given directory_path."""
    directory_files = []
    for path, dirs, files in os.walk(directory_path):
        directory_files.extend(files)
        if not recursive:
            break
    return directory_files


def directory_file_paths(directory_path: str, *, recursive: bool = True) -> List[str]:
    """List the file paths at the given directory_path."""
    file_paths = []
    for path, dirs, files in os.walk(directory_path):
        file_paths.extend([os.path.join(path, file) for file in files])
        if not recursive:
            break
    return file_paths


def directory_copy(src_path: str, dst_path: str):
    """Copy the directory from the src_path to the destination path."""
    # TODO: add option to overwrite existing directory
    shutil.copytree(src_path, dst_path)


def directory_delete(directory_path: str):
    """Delete the given directory."""
    shutil.rmtree(directory_path)


def directory_create(directory_path: str, mode=0o777):
    """Create a directory."""
    if not directory_exists(directory_path):
        os.makedirs(directory_path, mode=mode)
    else:
        print(f'Output directory ({directory_path}) already exists')


# TODO: add return types for some of the functions below
def directory_disk_usage(directory_path: str):
    """Return the disk usage for the given directory."""
    return shutil.disk_usage(directory_path)


def directory_disk_free_space(directory_path: str):
    """Return the free space in the given directory."""
    return directory_disk_usage(directory_path).free


def directory_disk_used_space(directory_path: str):
    """Return the used space in the given directory."""
    return directory_disk_usage(directory_path).used


def directory_disk_total_space(directory_path: str):
    """Return the total space in the given directory."""
    return directory_disk_usage(directory_path).total


def home_directory() -> str:
    return os.path.expanduser("~")


def home_directory_join(path: str) -> str:
    """Join the given path with the home directory."""
    return os.path.join(home_directory(), path)


def directory_move(src_path: str, dst_path: str):
    """Move the directory from the src_path to the dst_path."""
    shutil.move(src_path, dst_path)


def directory_files_details(directory_path: str, *, recursive: bool = True) -> Dict[str, Dict[str, Union[str, int]]]:
    """Return the file details for each file in the directory at the given path."""
    from .files import file_details, file_name

    file_paths = directory_file_paths(directory_path, recursive=recursive)
    file_details_dict = {path: file_details(path) for path in file_paths}
    return file_details_dict


def directory_files_read(directory_path: str, *, recursive: bool = True) -> Iterable[Tuple[str, str]]:
    """Read all files in the directory_path."""
    from .files import file_read, file_name

    file_paths = directory_file_paths(directory_path, recursive=recursive)
    for path in file_paths:
        yield path, file_read(path)


def directory_subdirectory_names(directory_path: str, *, recursive: bool = True) -> List[str]:
    """List the names of all subdirectories in the given directory."""
    # TODO: I think there is a better way to return this data. Rather than ['foo', 'subfoo'], I'd like to see something like:
    # {
    #   'foo': {
    #     'subfoo': {}
    #   }
    # }
    subdir_names = []
    for path, dirs, files in os.walk(directory_path):
        if any(dirs):
            subdir_names.extend(dirs)
        if not recursive:
            break
    return subdir_names


def directory_files_containing(
    directory_path: str, pattern: str, *, pattern_is_regex: bool = False, recursive: bool = True
) -> Dict[str, List[str]]:
    """Search for the given pattern in all files in the given directory_path."""
    from .files import file_name, file_search

    matching_files = {}
    file_paths = directory_file_paths(directory_path, recursive=recursive)

    for file_path in file_paths:
        search_results = file_search(file_path, pattern, pattern_is_regex=pattern_is_regex)
        if any(search_results):
            matching_files[file_path] = search_results
    return matching_files


def directory_file_paths_matching(directory_path: str, pattern: str, *, recursive: bool = True) -> List[str]:
    """Return the paths of all of the files in the given directory which match the pattern."""
    from .files import file_name_matches, file_name

    # TODO: consider consolidating this function into the directory_file_names_matching function and providing a flag to specify whether or not the user wants a file name or file path

    matching_file_paths = [
        file_path
        for file_path in directory_file_paths(directory_path, recursive=recursive)
        if file_name_matches(file_path, pattern) or pattern in file_path
    ]
    return matching_file_paths


def directory_file_names_matching(directory_path: str, pattern: str, *, recursive: bool = True) -> List[str]:
    """Return the names of all of the files in the given directory which match the pattern."""
    from .files import file_name_matches, file_name

    matching_file_names = [
        name
        for name in directory_file_names(directory_path, recursive=recursive)
        if file_name_matches(name, pattern) or pattern in name
    ]
    return matching_file_names


def directory_read_files_with_path_matching(
    directory_path: str, pattern: str, *, recursive: bool = True
) -> Iterable[Tuple[str, str]]:
    """Read all of the files in the given directory whose paths match the given pattern."""
    from .files import file_read

    matching_file_paths = directory_file_paths_matching(directory_path, pattern, recursive=recursive)

    for file_path in matching_file_paths:
        yield file_path, file_read(file_path)


def temp_dir_create(**kwargs) -> str:
    """Create a temporary directory."""
    return tempfile.TemporaryDirectory(**kwargs)
