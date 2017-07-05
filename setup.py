from setuptools import setup, find_packages
from basesetup import write_version_py

VERSION = "0.1alpha"
ISRELEASED = False

write_version_py(VERSION, ISRELEASED, 'gui/version.py')

setup(
    name="deepchem-gui",
    version=VERSION,
    packages=find_packages(),
    include_package_data=True,
    package_data={'deepchem-gui': ['static/deepchem-gui/*', 'static/ngl/*']},
    entry_points={
        'console_scripts': [
            'deepchem-gui = gui.cli.main:main',
        ],
    },
    platforms=["Linux", "Unix"],
    author="Prasad Kawthekar",
    author_email="pkawthek@stanford.edu",
    description="DeepChem GUI",
    license="GPL-3.0",)
