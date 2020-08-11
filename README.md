# Automated Network Equipment Backup

Automated Network Equipment Backup is a small python console application that utilizes SSH to log in to a network device and issue the Show Run command. It then stores that information in a text file named after the hostname from the config file. It appends a number (Default: 1-3) to the end of the file to allow for multiple configurations to be backed up. It rotates between the numbers for example 1, 2, 3, and then back to 1. Meaning 1 could be a newer configuration than 3.

If you would like to only have 1 copy of the config simply set ```backup_count``` to 1.

## Requirements

This application requires a minimum python3.8

## Installation

1. Clone the git repository.
   ```bash
   git clone https://github.com/DavFount/automated_network_equipment_backup
   ```
2. Create a virtual environment
    ```bash
    python -m venv venv
    ```
3. Activate Virtual Environment
    * Windows - ``` .\venv\Scripts\Activate ```
    * Linux/Mac - ```source ./venv/bin/activate ```
4. Install Requirements ```pip install -r requirements.txt```

## Usage

1. Rename ```config_example.json``` to ```config.json```
2. Modify the configuration to meet your needs.
3. Activate Virtual Environment (if its not already)
    * Windows - ``` .\venv\Scripts\Activate ```
    * Linux/Mac - ```source ./venv/bin/activate ```
4. run the script ``` python app.py ```

## Note regarding paths

1. This application uses the pathlib library for Python3 allowing you to set the path using forwards slashes and the library will automatically use the correct slashes for your operating system.

2. If you want to use a network share to save your backups to simply use the following syntax ```\\\\path/to/network/share```

## Netmiko
This application uses [netmiko](https://github.com/ktbyers/netmiko) by ktbyers. For a list of supported devices [click here](https://ktbyers.github.io/netmiko/PLATFORMS.html)

## License
[MIT](https://choosealicense.com/licenses/mit/)