import os

import pytest

from d8s_file_system import atomic_write, directory_create, file_read, directory_delete

TEST_DIRECTORY_PATH = './test_files'
NON_EXISTENT_FILE_PATH = './foo'
TEST_FILE_NAME = 'a'
EXISTING_FILE_PATH = os.path.join(TEST_DIRECTORY_PATH, TEST_FILE_NAME)


def test_atomic_write_docs_1():
    directory_create(TEST_DIRECTORY_PATH)
    FILE_CONTENTS = 'foo'

    with atomic_write(EXISTING_FILE_PATH) as f:
        f.write(FILE_CONTENTS)
    assert file_read(EXISTING_FILE_PATH) == FILE_CONTENTS

    with atomic_write(EXISTING_FILE_PATH) as f:
        f.write(FILE_CONTENTS)
    assert file_read(EXISTING_FILE_PATH) == FILE_CONTENTS

    # if we try to write to an existing file with `overwrite=False`, we will get an error
    with pytest.raises(FileExistsError):
        with atomic_write(EXISTING_FILE_PATH, overwrite=False) as f:
            f.write(FILE_CONTENTS)

    directory_delete(TEST_DIRECTORY_PATH)
