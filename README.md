# README.md

# Python Directory Reader

## Overview

The Python Directory Reader is a simple application designed to read data from multiple specified directories. It utilizes a configuration file to determine the paths of the directories from which it will read data.

## Features

- Reads data from four specified directories:
  - BEE_DATA
  - LIMITLESS_DATA
  - FACTS
  - ERRORS
- Configurable directory paths through a JSON configuration file.
- Modular design with separate files for configuration, directory reading, and utility functions.

## Project Structure

```
python-directory-reader
├── src
│   ├── main.py
│   ├── config.py
│   ├── directory_reader.py
│   └── utils
│       ├── __init__.py
│       └── file_handler.py
├── config
│   └── directories.json
├── tests
│   ├── __init__.py
│   ├── test_directory_reader.py
│   └── test_file_handler.py
├── requirements.txt
├── .gitignore
└── README.md
```

## Installation

To install the required dependencies, run:

```
pip install -r requirements.txt
```

## Usage

To run the application, execute the following command:

```
python src/main.py
```

Ensure that the `directories.json` file is properly configured with the correct paths for the directories you wish to read from.

## Contributing

Contributions are welcome! Please feel free to submit a pull request or open an issue for any suggestions or improvements.

## License

This project is licensed under the MIT License.