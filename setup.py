import setuptools
import subprocess
import shutil


compile_result = subprocess.call([
    'gcc', '-shared', '-o', 'libmir.dll',
    'mir.c', 'mir-gen.c',
    '-Wl,--export-all-symbols',
    '-Os'
], cwd='./mir-src')
if compile_result != 0:
    raise Exception("MIR GCC build failed with return code %d." % compile_result)

shutil.copy('./mir-src/libmir.dll', './libmir/libmir.dll')

with open("README.md", "r") as fh:
    long_description = fh.read()


class BinaryDistribution(setuptools.Distribution):
    def has_ext_modules(foo):
        return True


setuptools.setup(
    name="libmir", # Replace with your own username
    version="0.1.0a1",
    author="flandre.info",
    author_email="flandre@scarletx.cn",
    description="Python bindings for MIR JIT.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/eliphatfs/libmir",
    packages=['libmir'],
    classifiers=[
        "Programming Language :: Python :: 3 :: Only",
        "License :: OSI Approved :: Apache Software License"
    ],
    python_requires='~=3.6',
    package_data={
        'libmir': ['libmir.dll'],
    },
    distclass=BinaryDistribution
)
