import hashlib
import os
import shutil
try:
    import tkinter as tk
except ImportError:
    import Tkinter as tk

from binilla.util import *
from traceback import format_exc


def get_is_executable(filepath):
    if not os.path.isfile(filepath):
        return False

    try:
        with open(filepath, "rb") as f:
            if f.read(2) != b"MZ":
                return False
            f.seek(296)
            if f.read(6) != b"PE\x00\x00\x4c\x01":
                return False
    except Exception:
        return False

    return True


def do_executable_patch(file_path, region_bounds=(), orig_hashes=(),
                        patched_hashes=(), patches=(), backup=True):
    '''Returns True if patch failed.
    Returns False if patch succeeded.
    Returns None if patch is already applied.
    '''
    if not get_is_executable(file_path):
        return True

    assert len(region_bounds) == len(orig_hashes)
    # already_patched will start out True if we have enough hashes
    # to compare, and will only be False if one or more don't match
    already_patched = len(region_bounds) == len(patched_hashes)
    patched_hashes = tuple(patched_hashes) + (
        (None, ) * (len(orig_hashes) - len(patched_hashes)))

    try:
        with open(file_path, "rb") as f:
            for bounds, orig, patched in zip(region_bounds, orig_hashes,
                                             patched_hashes):
                f.seek(bounds[0])
                hasher = hashlib.md5()
                hasher.update(f.read(bounds[1] - bounds[0]))
                area_hash = hasher.hexdigest()
                if area_hash == patched and patched is not None:
                    continue
                elif area_hash != orig:
                    return True
                already_patched = False

        if already_patched:
            return None

        if backup:
            try:
                if not os.path.exists(file_path + ".ORIG"):
                    with open(file_path, "rb") as in_file,\
                         open(file_path + ".ORIG", "wb") as out_file:
                        shutil.copyfileobj(in_file, out_file)
            except Exception:
                pass

        with open(file_path, "rb+") as f:
            for offset, patch in patches:
                f.seek(offset)
                f.write(patch)

    except Exception:
        print(format_exc())
        return True

    return False
