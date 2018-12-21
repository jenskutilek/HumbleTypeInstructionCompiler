"""Prints a plain-text version of compiled Humble Type Instructions for testing purposes"""

import argparse

from . import __version__
from . import toConsole


def main():
	# Arguments
	parser = argparse.ArgumentParser(description=__doc__)
	parser.add_argument("--version", action="version", version=__version__)
	parser.add_argument("SOURCE", help="instruction source file")
	args = parser.parse_args()

	# Functionality
	toConsole(args.SOURCE)


if __name__ == '__main__':
	main()
