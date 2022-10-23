Blobo
=====

Python class and instructions for reading the Blobo game controller.

This branch is a complete rewrite for Python3 and Bluez5. Tested on Arch Linux in 2022.

## Usage

- `pip install pybluez` (or actually `pip install git+https://github.com/pybluez/pybluez.git` at the time of writing).
- Shake Blobo to wake it up.
- `python Example.py` - connect to any Blobo.
- `python Example.py 00:11:22:33:44:55` - connect to a specific Blobo.

## License

Licensed under the MIT License.
