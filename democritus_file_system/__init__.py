try:
    from importlib.metadata import version, PackageNotFoundError
except ImportError:
    from importlib_metadata import version, PackageNotFoundError

try:
    __version__ = version('democritus_file_system')
except PackageNotFoundError:
    message = 'Unable to find a version number for "democritus_file_system". This likely means the library was not installed properly. Please re-install it and, if the problem persists, raise an issue here: https://github.com/democritus-project/democritus-file-system/issues.'
    print(message)

__author__ = '''Floyd Hightower'''
__email__ = 'floyd.hightower27@gmail.com'

from .atomic_writes import atomic_write
from .files import *
from .directories import *
