from setuptools import setup, find_packages

with open("requirements.txt") as f:
	install_requires = f.read().strip().split("\n")

# get version from __version__ variable in ksa_taekwondo/__init__.py
from ksa_taekwondo import __version__ as version

setup(
	name="ksa_taekwondo",
	version=version,
	description="taekwondo App ",
	author="Trigger Solutions",
	author_email="trigger.solutions.eg@gmail.com",
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires
)
