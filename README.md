# PFX to CRT and Private Key Converter

This Python application converts a PFX file to CRT and Private Key files using OpenSSL. It provides a graphical interface built with Tkinter for ease of use.

## Requirements
- Python: Ensure Python is installed on your system. This application is written in Python.
- Tkinter: Tkinter module is required for the graphical user interface. It comes pre-installed with Python, but make sure it's available in your Python installation.
- OpenSSL: This application relies on OpenSSL for the conversion process. Ensure OpenSSL is installed on your system before using this converter.

## Compatibility
This application has been tested on Linux Fedora. While it should work on other Linux distributions, it may require adjustments for Windows or macOS environments.

## Instructions
1. Launch the application.
2. Provide the path to the PFX file.
3. Enter the password for the PFX file.
4. Optionally, check the "Export Public Key" box if you want to export the public key.
5. Click the "Convert" button to start the conversion process.
6. Once completed, the CRT and Private Key files will be generated in the same directory as the PFX file.
7. Optionally, clear the result text by clicking the "Clear Result" button.

## Usage Notes
- Ensure the provided PFX file path is correct.
- Make sure to enter the correct password for the PFX file.
- If OpenSSL is not installed, you will receive an error message prompting you to install it before proceeding with the conversion.

## License
This application is open-source under the [MIT License](LICENSE).

For any issues or suggestions, feel free to open an [issue](https://github.com/guilherme-reis/tk_1_convert_pfx_to_crt_and_key/issues).