import os
import re
import setuptools


def readFile(relativePath):
	here = os.path.abspath(os.path.dirname(__file__))
	path = os.path.normpath(os.path.join(here, relativePath))
	with open(path) as f:
		return f.read()


def readVersion(relativePath):
	content = readFile(relativePath)
	match = re.search(r"__version__ = ['\"]([^'\"]*)['\"]", content)
	if match:
		return match.group(1)
	raise RuntimeError("Could not find version string")


setuptools.setup(
	name="htic",
	version=readVersion("htic/__init__.py"),
	description="The Humble Type Instruction Compiler translates plain-text instructions into optimized TrueType hinting programs",
	url="https://gitlab.com/sev/htic",
	author="Severin Meyer",
	author_email="sev.ch@web.de",
	license="MIT",
	packages=["htic"],
	entry_points={"console_scripts": ["htic = htic.__main__:main"]},
	test_suite="test",
)
