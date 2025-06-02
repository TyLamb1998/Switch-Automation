
# Cisco SG300 SSH Automation Script

## Overview

This Python script automates SSH connections to Cisco SG300 switches to run single or multiple commands either from an inline list or a command file. It simplifies device management tasks by enabling batch execution of commands with output logging for troubleshooting and audit purposes.

The project demonstrates practical skills in network automation, secure SSH handling, and Python scripting—highlighting my ability to deliver reliable, maintainable solutions for network operations.

## Features

- Validate IP address input to ensure correctness.
- Load commands from a comma-separated string or an external command file.
- Connect to Cisco SG300 switches securely using SSH.
- Execute commands sequentially with live terminal output.
- Save command outputs to timestamped log files for audit and debugging.
- Robust error handling for connection, authentication, and unexpected issues.
- User-friendly CLI interface with argument parsing and password prompt retries.

## Requirements

- Python 3.x
- [Netmiko](https://github.com/ktbyers/netmiko) library (`pip install netmiko`)
- Network connectivity to Cisco SG300 switch with SSH enabled.

## Usage

### Inline commands example:
```bash
python switch_connect_batch.py --host 192.168.1.102 --username cisco --commands "show version,show vlan,show running-config"
```

### Commands from a file example:
```bash
python switch_connect_batch.py --host 192.168.1.102 --username cisco --file commands.txt
```

- `commands.txt` should contain one command per line, without extra blank lines.

## How It Works

1. Validates the provided IP address format.
2. Loads commands from the specified source.
3. Prompts the user up to 3 times for the SSH password.
4. Establishes an SSH session to the Cisco SG300.
5. Runs each command sequentially and prints output in real-time.
6. Logs outputs to a uniquely timestamped file in a `logs/` directory.
7. Handles and reports common errors like timeouts or authentication failures.

## Why This Project?

This script is a practical example of my network automation expertise, showcasing:

- Strong Python programming and scripting skills.
- Familiarity with industry-standard libraries (Netmiko).
- Ability to create robust, user-friendly CLI tools.
- Attention to detail with error handling and logging.
- Commitment to writing clean, maintainable, and documented code.

## Next Steps / Future Enhancements

- Support for parallel command execution across multiple devices.
- Enhanced logging format with JSON or CSV for easier parsing.
- Integration with Ansible or other automation frameworks.
- Support for different Cisco device types.
- Unit tests and CI/CD pipeline integration.

---

Feel free to reach out if you'd like to collaborate or have questions about the code!

---

