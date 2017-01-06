from sys import executable as py_executable
from PyInstaller.__main__ import run as _build_exe
from os import path, chdir

_here = path.abspath(path.dirname(__file__))
chdir(_here)
_py_executable_path = path.abspath(path.dirname(py_executable))

_build_exe_args = (
    '--clean',
    '--i', "application/ico/MainWindowIcon.ico",
    '--paths', "{}/Lib/site-packages/PyQt5/Qt/bin".format(_py_executable_path),
    '--paths', "package-ddclient/src",
    '-y',
    "application/main.py"
)

_build_package_file_name = 'package-ddclient/setup.py'

_build_package_args = (
    py_executable,
    _build_package_file_name,
    'sdist',
    '--formats=gztar',
    '-d', '../dist/package'
)


def build_package():
    from subprocess import call
    import sys
    try:
        ret_code = call(_build_package_args, shell=True)
        if ret_code < 0:
            print("Build package was terminated by signal", -ret_code, file=sys.stderr)
        else:
            print("Build package returned", ret_code, file=sys.stderr)
    except OSError as e:
        print("Build package execution failed:", e, file=sys.stderr)
    pass


def build_exe():
    _build_exe(pyi_args=_build_exe_args)
    pass


def add_data_file():
    src_path = 'doc/datadictionarysource'
    dist_path = 'dist/datadictionarysource'
    from shutil import copytree, rmtree
    if path.exists(dist_path):
        rmtree(dist_path)
    copytree(src_path, dist_path)
    pass


if __name__ == "__main__":
    try:
        build_exe()
        build_package()
        add_data_file()
    except Exception as exception:
        print('ERROR:', 'Build failed!', exception)
        import traceback
        traceback.print_exc()
        pass
    pass
