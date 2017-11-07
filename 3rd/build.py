# encoding: UTF-8

import subprocess
import os
import sys

# DA-RNN/3rd
third = os.path.dirname(os.path.abspath(__file__))

# libraries to build
libraries = ['eigen', 'nanoflann', 'Pangolin', 'Sophus', 'SuiteSparse']

def resolve(relpath):
    return os.path.join(third, relpath)

def ensure_directories(relpath):
    fullpath = resolve(relpath)
    if not os.path.isdir(fullpath):
        os.makedirs(fullpath)

def prepare_directories():
    for relpath in [os.path.join('build', lib) for lib in libraries]:
        ensure_directories(relpath)
    ensure_directories('artifact')

def this_is_a_command(fn):
    command = fn.__name__
    def __command__(*args, **kwargs):
        args, cwd = fn(*args, *kwargs)
        args.insert(0, command)
        print('>>>', *args)
        process = subprocess.Popen(args, cwd=cwd)
        process.wait()
        if process.returncode != 0:
            print(command, *args, file=sys.stderr)
            exit(process.returncode)
    return __command__

@this_is_a_command
def cmake(source_dir, build_dir, install_dir, **kwargs):
    xs = []
    for key, value in kwargs.items():
        if isinstance(value, bool):
            value = 'YES' if value else 'NO'
        xs.append('-D{}={}'.format(key, value))
    xs.append('-DCMAKE_INSTALL_PREFIX={}'.format(install_dir))
    xs.append(source_dir)
    return xs, build_dir

@this_is_a_command
def make(build_dir):
    xs = ['install', '-j{}'.format(os.cpu_count())]
    return xs, build_dir

def build_library(library, **kwargs):
    source_dir = resolve(library)
    build_dir = resolve(os.path.join('build', library))
    install_dir = resolve('artifact')
    cmake(source_dir, build_dir, install_dir, **kwargs)
    make(build_dir)

def build():
    for lib in libraries:
        build_library(lib)

if __name__ == '__main__':
    prepare_directories()
    build()

