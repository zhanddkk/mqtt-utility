from sys import executable as py_executable
from PyInstaller.__main__ import run as _build_exe
import os as _os
import platform

_here = _os.path.abspath(_os.path.dirname(__file__))
_os.chdir(_here)
_py_executable_path = _os.path.abspath(_os.path.dirname(py_executable))

if platform.system() == 'Windows':
    _build_exe_args = (
        '--clean',
        '--i', "application/ico/MainWindowIcon.ico",
        # '--paths', "{}/Lib/site-packages/PyQt5/Qt/bin".format(_py_executable_path),
        '--paths', "package-ddclient/src",
        '-n', 'application',
        '-y',
        "application/main.py"
    )
else:
    _build_exe_args = (
        '--clean',
        '--i', "application/ico/MainWindowIcon.ico",
        '--paths', "package-ddclient/src",
        '-n', 'application',
        '-y',
        "application/main.py"
    )

_build_package_file_name = 'package-ddclient/setup.py'

_build_package_args = (
    py_executable,
    _build_package_file_name,
    'sdist',
    '--formats=gztar',
    '-d', '../dist'
)


def build_package():
    from subprocess import call
    import sys
    try:
        ret_code = call(_build_package_args)
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
    dist_path = 'dist/dd_source'
    from shutil import copytree, rmtree
    if _os.path.exists(dist_path):
        rmtree(dist_path)
    copytree(src_path, dist_path)
    pass


def __only_py(src, names):
    ret = []
    for sub_name in names:
        if not sub_name.endswith('.py'):
            ret.append(sub_name)
            pass
    return ret
    pass


def add_node_script_file():
    src_path = 'application/nodescript'
    dist_path = 'dist/application/nodescript'
    from shutil import copytree, rmtree
    if _os.path.exists(dist_path):
        rmtree(dist_path)
    copytree(src_path, dist_path, ignore=__only_py)
    pass


def __add_dir_in_zip(_zip_f, dir_name, arc_pre_path=''):
    file_list = []
    if arc_pre_path and not arc_pre_path.endswith('/'):
        arc_pre_path = '{}/'.format(arc_pre_path)
    if _os.path.isfile(dir_name):
        file_list.append(dir_name)
    else:
        for root, dirs, files in _os.walk(dir_name):
            for name in files:
                file_list.append(_os.path.join(root, name))
    for file in file_list:
        arc_name = file[len(dir_name):]
        print(arc_name)
        _zip_f.write(file, arc_pre_path + arc_name)
    pass


def packing_app(app_pkg_name):
    print('Packing application...')
    if _os.path.exists(app_pkg_name):
        _os.remove(app_pkg_name)
        print(app_pkg_name, 'is removed')
    from zipfile import ZipFile
    with ZipFile(app_pkg_name, 'w') as zip_f:
        __add_dir_in_zip(zip_f, 'dist/dd_source', 'dd_source')
        __add_dir_in_zip(zip_f, 'dist/application', 'application')
    pass


def format_app_package_name():
    from application.AppVersion import __doc__ as _app_version
    name_format = 'simulator-{version}-{os_name}_{os_machine}.zip'
    _os_name = platform.system() + platform.release()
    _os_machine = platform.machine()
    return name_format.format(os_name=_os_name,
                              os_machine=_os_machine,
                              version=_app_version).lower()
    pass


if __name__ == "__main__":
    try:
        build_exe()
        build_package()
        add_data_file()
        add_node_script_file()
        packing_app('dist/{}'.format(format_app_package_name()))
        pass
    except Exception as exception:
        print('ERROR:', 'Build failed!', exception)
        import traceback
        traceback.print_exc()
        input()
        pass
    pass
