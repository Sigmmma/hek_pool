import imp
import os
import platform
import sys
import subprocess
try:
    import tkinter as tk
except ImportError:
    import Tkinter as tk
from io import StringIO

from math import log, ceil
from time import sleep
from supyr_struct.defs.util import *
from traceback import format_exc


def is_main_frozen():
   return (hasattr(sys, "frozen") or hasattr(sys, "importers")
           or imp.is_frozen("__main__"))


def get_cwd(module=None):
   if is_main_frozen():
       return os.path.dirname(sys.executable)
   return os.path.dirname(__file__ if module is None else module)


def float_to_str(f, max_sig_figs=23*log(2, 10)):
    sig_figs = -1
    if abs(f) > 0:
        sig_figs = int(round(max_sig_figs - log(abs(f), 10)))

    if sig_figs < 0:
        return str(f).split(".")[0]
    return (("%" + (".%sf" % sig_figs)) % f).rstrip("0").rstrip(".")


class ProcController():
    kill = False
    abandon = False
    process = None
    returncode = None

    def __init__(self, kill=False, abandon=False,
                 process=None, returncode=None):
        self.kill = kill
        self.abandon = abandon
        self.process = process
        self.returncode = returncode


def do_subprocess(exec_path, cmd_args=(), exec_args=(), **kw):
    result = 1
    proc_controller = kw.pop("proc_controller", ProcController())
    try:

        if platform.system() == "Linux":
            args = (exec_path, ) + exec_args
        else:
            cmd_args  = ''.join((" /%s" % a.lower()) for a in cmd_args)
            cmd_str = '"%s" %s'
            if cmd_args:
                # ALWAYS make sure either /c or /k are explicitely supplied when
                # calling cmd, otherwise default quote handling will be used and
                # putting quotes around everything won't supply parameters right
                if '/k' not in cmd_args:
                    cmd_args += ' /c'
                cmd_str = 'cmd %s "%s"' % (cmd_args, cmd_str)

            exec_args = ''.join(( " %s" % a.lower()) for a in exec_args)
            args = cmd_str % (exec_path, exec_args)

        with subprocess.Popen(args, **kw) as p:
            proc_controller.process = p
            while p.poll() is None:
                if proc_controller.kill:
                    p.kill()
                    p.wait()
                elif proc_controller.abandon:
                    break
                sleep(0.02)

        result = p.returncode
    except Exception:
        print(format_exc())

    proc_controller.returncode = result
    return result