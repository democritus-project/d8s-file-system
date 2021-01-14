import contextlib
import os

from atomicwrites import atomic_write as atomic_write_, AtomicWriter


class AtomicWriterPerms(AtomicWriter):
    """This class wraps the AtomicWriter from the atomicwrites package to update the file permissions after the file is created.

    This snippet was taken from/inspired by the code here: https://github.com/OCR-D/core/pull/625."""

    def get_fileobject(self, **kwargs):
        f = super().get_fileobject(**kwargs)
        try:
            mode = os.stat(self._path).st_mode
        except FileNotFoundError:
            # Creating a new file, emulate what os.open() does
            mask = os.umask(0)
            os.umask(mask)
            mode = 0o664 & ~mask
        fd = f.fileno()
        os.fchmod(fd, mode)
        return f


@contextlib.contextmanager
def atomic_write(fpath, *, overwrite: bool = True, **cls_kwargs):
    with atomic_write_(fpath, writer_cls=AtomicWriterPerms, overwrite=overwrite, **cls_kwargs) as f:
        yield f
