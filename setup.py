import setuptools
import subprocess
import shutil
from setuptools.command.build_ext import build_ext
from distutils.extension import Extension


compile_result = subprocess.call([
    'gcc', '-shared', '-o', 'libmir.dll',
    'mir.c', 'mir-gen.c', 'libmir-ext.c',
    '-Os', '-fPIC'
], cwd='./mir-src')
if compile_result != 0:
    raise Exception("MIR GCC build failed with return code %d." % compile_result)

shutil.copy('./mir-src/libmir.dll', './libmir/libmir.dll')

with open("README.md", "r") as fh:
    long_description = fh.read()


# Dirty fix for https://github.com/pypa/packaging-problems/issues/542
class build_ext_dummy(build_ext):
    def run(self):
        pass


class BinaryDistribution(setuptools.Distribution):
    def has_ext_modules(foo):
        return True

    def is_pure(self):
        return False


setuptools.setup(
    name="libmir", # Replace with your own username
    version="0.1.0a2",
    author="flandre.info",
    author_email="flandre@scarletx.cn",
    description="Python bindings for MIR JIT.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/eliphatfs/libmir",
    packages=['libmir'],
    include_package_data=True,
    ext_modules=[Extension("libmir.native", [])],
    classifiers=[
        "Programming Language :: Python :: 3 :: Only",
        "License :: OSI Approved :: Apache Software License"
    ],
    python_requires='~=3.6',
    package_data={
        'libmir': ['libmir.dll'],
    },
    cmdclass={'build_ext': build_ext_dummy},
    distclass=BinaryDistribution
)
