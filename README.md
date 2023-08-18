# SQL Explorer - Readme

SQL Explorer is a tool designed to simplify the process of generating Python classes and functions for interacting with a specific database. It achieves this by reading the 'information_schema' table of a target database and generating corresponding Python classes for each table, along with CRUD (Create, Read, Update, Delete) functions.

## Table of Contents

- [Features](#features)
- [Installation](#installation)
  - [Using install.py](#using-installpy)
  - [Using requirements.txt](#using-requirementstxt)
- [Usage](#usage)
  - [Configuration](#configuration)
  - [Generating Python Classes and Functions](#generating-python-classes-and-functions)
  - [Running SQL_Explorer](#running-sql_explorerpy)
- [Example](#example)
- [Contributing](#contributing)
- [License](#license)

## Features

- Automatically generates Python classes for each table in the specified database.
- Creates CRUD functions (SELECT/WHERE, INSERT, UPDATE, DELETE) for easy database interaction.
- Simplifies the setup through a configuration file and a provided example.
- Supports both installation methods: using `install.py` or `requirements.txt`.

## Installation

### Using install.py

1. Clone the repository: `git clone https://github.com/yourusername/sql-explorer.git`
2. Navigate to the project directory: `cd sql-explorer`
3. Run the installation script: `python install.py`

### Using requirements.txt

1. Clone the repository: `git clone https://github.com/yourusername/sql-explorer.git`
2. Navigate to the project directory: `cd sql-explorer`
3. Install the required dependencies: `pip install -r requirements.txt`

## Usage

### Configuration

1. Copy the provided `.env.example` file and rename it to `.env`.
2. Fill in the necessary information:
   - `HOST`: Database host address.
   - `USER`: Database username.
   - `PASSWORD`: Database password.
   - `PORT`: Database port.
   - `DATABASE`: Target database name (default: 'information_schema').

### Generating Python Classes and Functions

1. Ensure that you have configured the `.env` file with the correct database information.
2. Run the SQL Explorer script: `python SQL_Explorer.py`
3. The script will read the 'information_schema' table and generate Python classes and functions for each table in the database.

### Running SQL_Explorer.py

1. After configuring the `.env` file, you can run `SQL_Explorer.py` directly: `python SQL_Explorer.py`.
2. The script will read the configuration from the `.env` file and generate the necessary files.

## Example

Here's an example of how to use SQL Explorer:

1. Install SQL Explorer using the preferred method.
2. Configure the `.env` file with your database information.
3. Run the SQL Explorer script: `python SQL_Explorer.py`.
4. The script will generate Python classes and functions for the specified database tables.

## Contributing

Contributions are welcome! If you find any issues or have suggestions for improvements, please feel free to open an issue or submit a pull request on the GitHub repository.

## License

This project is licensed under the [MIT License](LICENSE).
