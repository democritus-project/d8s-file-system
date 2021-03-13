import os
import tempfile

import pytest

from d8s_file_system import directory_create, directory_delete, directory_file_names
from d8s_file_system import (
    is_file,
    file_read,
    file_read_bytes,
    file_write,
    file_append,
    file_move,
    file_copy,
    file_delete,
    file_owner_name,
    file_change_owner,
    file_ssdeep,
    file_md5,
    file_sha1,
    file_sha256,
    file_sha512,
    file_name_escape,
    file_name,
    file_name_windows,
    file_name_unix,
    file_size,
    file_directory,
    file_details,
    file_exists,
    file_is_readable,
    file_is_writable,
    file_is_executable,
    file_contains,
    file_search,
    file_name_matches,
    temp_file_create,
)
from d8s_file_system.files import _file_active_action, _file_action

NON_EXISTENT_FILE_PATH = './foo'
TEST_DIRECTORY_PATH = './test_files'
TEST_FILE_CONTENTS = 'a'
TEST_FILE_NAME = 'a'
EXISTING_FILE_PATH = os.path.join(TEST_DIRECTORY_PATH, TEST_FILE_NAME)


@pytest.fixture(autouse=True)
def clear_testing_directory():
    """This function is run after every test."""
    directory_delete(TEST_DIRECTORY_PATH)
    directory_create(TEST_DIRECTORY_PATH)
    file_write(EXISTING_FILE_PATH, TEST_FILE_CONTENTS)


def setup_module():
    """This function is run before all of the tests in this file are run."""
    directory_create(TEST_DIRECTORY_PATH)


def teardown_module():
    """This function is run after all of the tests in this file are run."""
    directory_delete(TEST_DIRECTORY_PATH)


def test_file_append_1():
    contents = file_read(EXISTING_FILE_PATH)
    assert contents == TEST_FILE_CONTENTS
    file_append(EXISTING_FILE_PATH, 'bc')
    contents = file_read(EXISTING_FILE_PATH)
    assert contents == 'abc'


def test_file_copy_1():
    result = file_copy(EXISTING_FILE_PATH, os.path.join(TEST_DIRECTORY_PATH, 'b'))
    assert directory_file_names(TEST_DIRECTORY_PATH) == ['a', 'b']

    # TODO: test the preserve_metadata kwarg (this requires a function to get file metadata)


def test_file_delete_1():
    assert directory_file_names(TEST_DIRECTORY_PATH) == ['a']
    result = file_delete(EXISTING_FILE_PATH)
    assert directory_file_names(TEST_DIRECTORY_PATH) == []


def test_file_write_1():
    contents = file_read(EXISTING_FILE_PATH)
    assert contents == TEST_FILE_CONTENTS

    file_write(EXISTING_FILE_PATH, 'foo bar')
    contents = file_read(EXISTING_FILE_PATH)
    assert contents == 'foo bar'

    file_write(EXISTING_FILE_PATH, b'abc')
    contents = file_read(EXISTING_FILE_PATH)
    assert contents == 'abc'

    file_write(EXISTING_FILE_PATH, [1, 2, 3])
    contents = file_read(EXISTING_FILE_PATH)
    assert contents == '[1, 2, 3]'


def test_file_move_1():
    assert directory_file_names(TEST_DIRECTORY_PATH) == ['a']
    file_move(EXISTING_FILE_PATH, os.path.join(TEST_DIRECTORY_PATH, 'b'))
    assert directory_file_names(TEST_DIRECTORY_PATH) == ['b']


def test_file_contains_docs_1():
    assert file_contains(EXISTING_FILE_PATH, 'a') == True
    assert file_contains(EXISTING_FILE_PATH, 'b') == False
    assert file_contains(EXISTING_FILE_PATH, '[abc]', pattern_is_regex=True) == True
    # assert file_contains(NON_EXISTENT_FILE_PATH, 'a') == 'fill'  # [Errno 2] No such file or directory


def test_file_details_docs_1():
    assert file_details(EXISTING_FILE_PATH) == {
        'md5': '0cc175b9c0f1b6a831c399e269772661',
        'sha1': '86f7e437faa5a7fce15d1ddcb9eaeaea377667b8',
        'sha256': 'ca978112ca1bbdcafac231b39a23dc4da786eff8147c4e72b9807785afee48bb',
        'size': 1,
        'ssdeep': '3:E:E',
    }
    with pytest.raises(FileNotFoundError):
        file_details(NON_EXISTENT_FILE_PATH)


def test_file_exists_docs_1():
    assert file_exists(EXISTING_FILE_PATH) == True
    assert file_exists(NON_EXISTENT_FILE_PATH) == False


def test_file_is_executable_docs_1():
    assert file_is_executable(EXISTING_FILE_PATH) == False
    assert file_is_executable(NON_EXISTENT_FILE_PATH) == False


def test_file_is_readable_docs_1():
    assert file_is_readable(EXISTING_FILE_PATH) == True
    assert file_is_readable(NON_EXISTENT_FILE_PATH) == False


def test_file_is_writable_docs_1():
    assert file_is_writable(EXISTING_FILE_PATH) == True
    assert file_is_writable(NON_EXISTENT_FILE_PATH) == False


def test_file_md5_docs_1():
    assert file_md5(EXISTING_FILE_PATH) == '0cc175b9c0f1b6a831c399e269772661'
    with pytest.raises(FileNotFoundError):
        file_md5(NON_EXISTENT_FILE_PATH)


def test_file_name_docs_1():
    assert file_name(EXISTING_FILE_PATH) == 'a'
    assert file_name(NON_EXISTENT_FILE_PATH) == 'foo'


def test_file_name_escape_docs_1():
    assert file_name_escape('a') == 'a'


def test_file_name_matches_docs_1():
    assert file_name_matches('a', 'a')
    assert file_name_matches('a', '?')
    assert file_name_matches('a', 'a*')
    assert not file_name_matches('a', 'a?')
    assert not file_name_matches('a', 'b')
    assert file_name_matches('a', '[abc]')
    assert not file_name_matches('a', '[bc]')

    path = '/Users/me/code/democritus/foo/democritus_sample_docs.json'
    assert file_name_matches(path, 'democritus_*_docs.json')


def test_file_name_unix_docs_1():
    assert file_name_unix('/Users/bob/documents/Summer2018.pdf') == 'Summer2018.pdf'


def test_file_name_windows_docs_1():
    assert file_name_windows('C:\\Documents\\Newsletters\\Summer2018.pdf') == 'Summer2018.pdf'

    # def test_file_owner_name_docs_1():
    with pytest.raises(FileNotFoundError):
        file_owner_name(NON_EXISTENT_FILE_PATH)


def test_file_read_docs_1():
    assert file_read(EXISTING_FILE_PATH) == 'a'
    with pytest.raises(FileNotFoundError):
        file_read(NON_EXISTENT_FILE_PATH)


def test_file_read_bytes_docs_1():
    assert file_read_bytes(EXISTING_FILE_PATH) == b'a'
    with pytest.raises(FileNotFoundError):
        file_read_bytes(NON_EXISTENT_FILE_PATH)


def test_file_search_docs_1():
    assert file_search(EXISTING_FILE_PATH, 'a') == ['a']
    assert file_search(EXISTING_FILE_PATH, 'b') == []
    assert file_search(EXISTING_FILE_PATH, '[abc]', pattern_is_regex=True) == ['a']
    with pytest.raises(FileNotFoundError):
        file_search(NON_EXISTENT_FILE_PATH, 'a')


def test_file_sha1_docs_1():
    assert file_sha1(EXISTING_FILE_PATH) == '86f7e437faa5a7fce15d1ddcb9eaeaea377667b8'
    with pytest.raises(FileNotFoundError):
        file_sha1(NON_EXISTENT_FILE_PATH)


def test_file_sha256_docs_1():
    assert file_sha256(EXISTING_FILE_PATH) == 'ca978112ca1bbdcafac231b39a23dc4da786eff8147c4e72b9807785afee48bb'
    with pytest.raises(FileNotFoundError):
        file_sha256(NON_EXISTENT_FILE_PATH)


def test_file_sha512_docs_1():
    assert (
        file_sha512(EXISTING_FILE_PATH)
        == '1f40fc92da241694750979ee6cf582f2d5d7d28e18335de05abc54d0560e0f5302860c652bf08d560252aa5e74210546f369fbbbce8c12cfc7957b2652fe9a75'
    )
    with pytest.raises(FileNotFoundError):
        file_sha512(NON_EXISTENT_FILE_PATH)


def test_file_size_docs_1():
    assert file_size(EXISTING_FILE_PATH) == 1
    with pytest.raises(FileNotFoundError):
        file_size(NON_EXISTENT_FILE_PATH)


def test_file_ssdeep_docs_1():
    assert file_ssdeep(EXISTING_FILE_PATH) == '3:E:E'
    with pytest.raises(FileNotFoundError):
        file_ssdeep(NON_EXISTENT_FILE_PATH)


def test_is_file_docs_1():
    assert is_file(EXISTING_FILE_PATH) == True
    assert is_file(NON_EXISTENT_FILE_PATH) == False


def test_temp_file_create_docs_1():
    temp_file = temp_file_create()
    assert temp_file
    temp_file.close()
