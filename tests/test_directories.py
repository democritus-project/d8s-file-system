import os
import tempfile

import pytest

from d8s_file_system import (
    is_directory,
    directory_exists,
    directory_file_names,
    directory_file_paths,
    directory_copy,
    directory_delete,
    directory_create,
    directory_disk_usage,
    directory_disk_free_space,
    directory_disk_used_space,
    directory_disk_total_space,
    home_directory,
    home_directory_join,
    directory_move,
    directory_files_details,
    directory_files_read,
    directory_subdirectory_names,
    directory_files_containing,
    directory_file_paths_matching,
    directory_file_names_matching,
    directory_read_files_with_path_matching,
    temp_dir_create,
)
from d8s_file_system import file_write

NON_EXISTENT_DIRECTORY_PATH = './foo'
EXISTING_DIRECTORY_PATH = './test_directories'


@pytest.fixture(autouse=True)
def clear_testing_directory():
    """This function is run after every test."""
    if directory_exists(EXISTING_DIRECTORY_PATH):
        directory_delete(EXISTING_DIRECTORY_PATH)
    if directory_exists(NON_EXISTENT_DIRECTORY_PATH):
        directory_delete(NON_EXISTENT_DIRECTORY_PATH)
    directory_create(EXISTING_DIRECTORY_PATH)
    file_write(os.path.join(EXISTING_DIRECTORY_PATH, 'a'), 'a')
    file_write(os.path.join(EXISTING_DIRECTORY_PATH, 'b'), 'b')
    file_write(os.path.join(EXISTING_DIRECTORY_PATH, 'c'), 'c')


def setup_module():
    """This function is run before all of the tests in this file are run."""
    directory_create(EXISTING_DIRECTORY_PATH)


def teardown_module():
    """This function is run after all of the tests in this file are run."""
    directory_delete(EXISTING_DIRECTORY_PATH)


def test_directory_create_docs_1():
    directory_create(os.path.join(EXISTING_DIRECTORY_PATH, 'foo'))
    assert directory_subdirectory_names(EXISTING_DIRECTORY_PATH, recursive=False) == ['foo']

    # creating the same directory again works (it does not raise an error)
    directory_create(os.path.join(EXISTING_DIRECTORY_PATH, 'foo'))
    assert directory_subdirectory_names(EXISTING_DIRECTORY_PATH, recursive=False) == ['foo']

    # creating multiple layers of directories works too
    directory_create(os.path.join(EXISTING_DIRECTORY_PATH, 'foo', 'subfoo'))
    assert directory_subdirectory_names(EXISTING_DIRECTORY_PATH, recursive=False) == ['foo']
    assert directory_subdirectory_names(EXISTING_DIRECTORY_PATH) == ['foo', 'subfoo']


def test_directory_copy_docs_1():
    assert directory_subdirectory_names(EXISTING_DIRECTORY_PATH, recursive=False) == []
    new_directory_path = os.path.join(EXISTING_DIRECTORY_PATH, 'foo')
    directory_create(new_directory_path)
    assert directory_subdirectory_names(EXISTING_DIRECTORY_PATH, recursive=False) == ['foo']
    file_write(os.path.join(new_directory_path, 'a'), 'a')

    copy_directory_path = os.path.join(EXISTING_DIRECTORY_PATH, 'bar')
    directory_copy(new_directory_path, copy_directory_path)
    assert directory_subdirectory_names(EXISTING_DIRECTORY_PATH, recursive=False) == ['foo', 'bar']
    assert directory_file_names(new_directory_path) == ['a']
    assert directory_file_names(copy_directory_path) == ['a']

    # copying into a directory which already exists raises an error
    with pytest.raises(FileExistsError):
        directory_copy(new_directory_path, copy_directory_path)


def test_directory_copy_docs_recursive_copy():
    assert directory_subdirectory_names(EXISTING_DIRECTORY_PATH, recursive=False) == []
    new_directory_path = os.path.join(EXISTING_DIRECTORY_PATH, 'foo', 'subfoo')
    directory_create(new_directory_path)
    assert directory_subdirectory_names(EXISTING_DIRECTORY_PATH) == ['foo', 'subfoo']
    file_write(os.path.join(new_directory_path, 'a'), 'a')

    # copying a directory copies everything inside that directory
    src_path = os.path.join(EXISTING_DIRECTORY_PATH, 'foo')
    dst_path = os.path.join(EXISTING_DIRECTORY_PATH, 'bar')
    deep_dst_path = os.path.join(dst_path, 'subfoo')
    directory_copy(src_path, dst_path)
    assert directory_subdirectory_names(EXISTING_DIRECTORY_PATH) == ['foo', 'bar', 'subfoo', 'subfoo']
    assert directory_file_names(deep_dst_path) == ['a']


def test_directory_move_docs_1():
    assert directory_exists(EXISTING_DIRECTORY_PATH)
    assert not directory_exists(NON_EXISTENT_DIRECTORY_PATH)
    directory_move(EXISTING_DIRECTORY_PATH, NON_EXISTENT_DIRECTORY_PATH)
    assert not directory_exists(EXISTING_DIRECTORY_PATH)
    assert directory_exists(NON_EXISTENT_DIRECTORY_PATH)


def test_directory_delete_docs_1():
    assert directory_subdirectory_names(EXISTING_DIRECTORY_PATH, recursive=False) == []
    new_directory_path = os.path.join(EXISTING_DIRECTORY_PATH, 'foo')
    directory_create(new_directory_path)
    assert directory_subdirectory_names(EXISTING_DIRECTORY_PATH, recursive=False) == ['foo']
    directory_delete(new_directory_path)
    assert directory_subdirectory_names(EXISTING_DIRECTORY_PATH, recursive=False) == []

    with pytest.raises(FileNotFoundError):
        directory_delete(NON_EXISTENT_DIRECTORY_PATH)


def test_home_directory_docs_1():
    result = home_directory()
    assert result.startswith('/Users/')

    result = home_directory_join(EXISTING_DIRECTORY_PATH)
    assert result.startswith('/Users/')
    assert result.endswith('test_directories')


def test_directory_files_containing_docs_1():
    result = directory_files_containing(EXISTING_DIRECTORY_PATH, 'a')
    assert result == {'./test_directories/a': ['a']}

    result = directory_files_containing(EXISTING_DIRECTORY_PATH, 'foo bar')
    assert result == {}

    result = directory_files_containing(EXISTING_DIRECTORY_PATH, '[abc]', pattern_is_regex=True)
    assert result == {'./test_directories/a': ['a'], './test_directories/c': ['c'], './test_directories/b': ['b']}

    result = directory_files_containing(NON_EXISTENT_DIRECTORY_PATH, 'a')
    assert result == {}


def test_directory_read_files_with_path_matching_docs_1():
    result = directory_read_files_with_path_matching(EXISTING_DIRECTORY_PATH, 'a')
    assert list(result) == [('./test_directories/a', 'a')]

    result = directory_read_files_with_path_matching(EXISTING_DIRECTORY_PATH, '*a')
    assert list(result) == [('./test_directories/a', 'a')]

    result = directory_read_files_with_path_matching(EXISTING_DIRECTORY_PATH, 'foo bar')
    assert list(result) == []

    result = directory_read_files_with_path_matching(EXISTING_DIRECTORY_PATH, '*[abc]')
    assert list(result) == [('./test_directories/a', 'a'), ('./test_directories/c', 'c'), ('./test_directories/b', 'b')]

    result = directory_read_files_with_path_matching(NON_EXISTENT_DIRECTORY_PATH, 'a')
    assert list(result) == []


def test_directory_disk_free_space_docs_1():
    assert isinstance(directory_disk_free_space(EXISTING_DIRECTORY_PATH), int)
    with pytest.raises(FileNotFoundError):
        directory_disk_free_space(NON_EXISTENT_DIRECTORY_PATH)


def test_directory_disk_total_space_docs_1():
    assert isinstance(directory_disk_total_space(EXISTING_DIRECTORY_PATH), int)
    with pytest.raises(FileNotFoundError):
        directory_disk_total_space(NON_EXISTENT_DIRECTORY_PATH)


def test_directory_disk_used_space_docs_1():
    assert isinstance(directory_disk_used_space(EXISTING_DIRECTORY_PATH), int)
    with pytest.raises(FileNotFoundError):
        directory_disk_used_space(NON_EXISTENT_DIRECTORY_PATH)


def test_directory_exists_docs_1():
    assert directory_exists(EXISTING_DIRECTORY_PATH) == True
    assert directory_exists(NON_EXISTENT_DIRECTORY_PATH) == False


def test_directory_file_names_docs_1():
    assert directory_file_names(EXISTING_DIRECTORY_PATH) == ['a', 'c', 'b']
    assert directory_file_names(NON_EXISTENT_DIRECTORY_PATH) == []


def test_directory_file_paths_matching_docs_1():
    assert directory_file_paths_matching(EXISTING_DIRECTORY_PATH, '*a') == ['./test_directories/a']
    assert directory_file_paths_matching(EXISTING_DIRECTORY_PATH, '*b') == ['./test_directories/b']
    assert directory_file_paths_matching(NON_EXISTENT_DIRECTORY_PATH, '*b') == []


def test_directory_file_names_matching_docs_1():
    assert directory_file_names_matching(EXISTING_DIRECTORY_PATH, 'a') == ['a']
    assert directory_file_names_matching(EXISTING_DIRECTORY_PATH, 'b') == ['b']
    assert directory_file_names_matching(NON_EXISTENT_DIRECTORY_PATH, 'b') == []


def test_directory_file_paths_docs_1():
    assert directory_file_paths(EXISTING_DIRECTORY_PATH) == [
        './test_directories/a',
        './test_directories/c',
        './test_directories/b',
    ]
    assert directory_file_paths(EXISTING_DIRECTORY_PATH, recursive=False) == [
        './test_directories/a',
        './test_directories/c',
        './test_directories/b',
    ]
    assert directory_file_paths(NON_EXISTENT_DIRECTORY_PATH) == []


def test_directory_files_details_docs_1():
    assert directory_files_details(EXISTING_DIRECTORY_PATH) == {
        './test_directories/a': {
            'md5': '0cc175b9c0f1b6a831c399e269772661',
            'sha1': '86f7e437faa5a7fce15d1ddcb9eaeaea377667b8',
            'sha256': 'ca978112ca1bbdcafac231b39a23dc4da786eff8147c4e72b9807785afee48bb',
            'ssdeep': '3:E:E',
            'size': 1,
        },
        './test_directories/c': {
            'md5': '4a8a08f09d37b73795649038408b5f33',
            'sha1': '84a516841ba77a5b4648de2cd0dfcb30ea46dbb4',
            'sha256': '2e7d2c03a9507ae265ecf5b5356885a53393a2029d241394997265a1a25aefc6',
            'ssdeep': '3:G:G',
            'size': 1,
        },
        './test_directories/b': {
            'md5': '92eb5ffee6ae2fec3ad71c777531578f',
            'sha1': 'e9d71f5ee7c92d6dc9e92ffdad17b8bd49418f98',
            'sha256': '3e23e8160039594a33894f6564e1b1348bbd7a0088d42c4acb73eeaed59c009d',
            'ssdeep': '3:H:H',
            'size': 1,
        },
    }
    assert directory_files_details(NON_EXISTENT_DIRECTORY_PATH) == {}


def test_directory_files_read_docs_1():
    assert tuple(directory_files_read(EXISTING_DIRECTORY_PATH)) == (
        ('./test_directories/a', 'a'),
        ('./test_directories/c', 'c'),
        ('./test_directories/b', 'b'),
    )
    assert tuple(directory_files_read(NON_EXISTENT_DIRECTORY_PATH)) == ()


def test_directory_subdirectory_names_docs_1():
    assert directory_subdirectory_names(EXISTING_DIRECTORY_PATH) == []

    new_directory_path = os.path.join(EXISTING_DIRECTORY_PATH, 'foo', 'subfoo')
    directory_create(new_directory_path)
    assert directory_subdirectory_names(EXISTING_DIRECTORY_PATH) == ['foo', 'subfoo']
    assert directory_subdirectory_names(EXISTING_DIRECTORY_PATH, recursive=False) == ['foo']
    assert directory_subdirectory_names(NON_EXISTENT_DIRECTORY_PATH) == []


def test_is_directory_docs_1():
    assert is_directory(EXISTING_DIRECTORY_PATH) == True
    assert is_directory(NON_EXISTENT_DIRECTORY_PATH) == False


def test_temp_dir_create_docs_1():
    temp_dir = temp_dir_create()
    assert isinstance(temp_dir, tempfile.TemporaryDirectory)
    temp_dir.cleanup()
