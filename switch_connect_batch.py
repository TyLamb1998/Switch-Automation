# A Simple Script to SSH into a Cisco SG300 Switch and Run a Command or Multiple Commands from a File or Inline.
# Run This Script with Python 3.x in Your Windows Command Line.

# Requirements:
# - Netmiko library must be installed. Install it using pip: "pip install netmiko"
# - Switch must be reachable and SSH must be enabled

import ipaddress
import argparse
import getpass
import os
from datetime import datetime
import time
from netmiko import ConnectHandler
from netmiko import NetmikoTimeoutException, NetmikoAuthenticationException


def validate_ip(ip_str):
    """Validate the format of an IP address string."""
    try:
        ipaddress.ip_address(ip_str)
        return True
    except ValueError:
        return False


def load_commands(args):
    """
    Load commands from --commands or --file, ensuring they're valid.
    Returns a list of commands or None if there's a problem.
    """
    if args.file:
        try:
            with open(args.file, 'r') as f:
                commands = [line.strip() for line in f if line.strip()]
                if not commands:
                    print("[ERROR] Command file was empty.")
                    
                    return None
        except FileNotFoundError:
            print(f"[ERROR] Command file '{args.file}' not found.")
            return None
    elif args.commands:
        commands = [cmd.strip() for cmd in args.commands.split(',') if cmd.strip()]
    else:
        print("[ERROR] You must provide commands with --commands or a file with --file")
        return None

    return commands


def connect_and_run_commands(host, username, password, commands, log_dir="logs"):
    """
    Establish SSH connection to a Cisco SG300 switch and run specified commands.
    Logs command output to a timestamped file in the specified directory.
    Returns True on success, False on failure.
    """
    device = {
        'device_type': 'cisco_s300',
        'host': host,
        'username': username,
        'password': password,
        'port': 22,
        'fast_cli': False
    }

    try:
        print(f"\nConnecting to {host}...")
        net_connect = ConnectHandler(**device)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        log_file = os.path.join(log_dir, f"{host.replace('.', '_')}_{timestamp}.log")
        os.makedirs(log_dir, exist_ok=True)

        with open(log_file, 'w') as log:
            for cmd in commands:
                print(f"\n[Running] {cmd}")
                output = net_connect.send_command(cmd)
                print(output)
                log.write(f"\n--- {cmd} ---\n{output}\n")

        print(f"\n✅ Output saved to: {log_file}")
        net_connect.disconnect()
        return True

    except NetmikoTimeoutException:
        print(f"[ERROR] Connection to {host} timed out.")
        return False
    except NetmikoAuthenticationException:
        print(f"[ERROR] Authentication failed for {username}@{host}.")
        return False
    except Exception as e:
        print(f"[ERROR] An unexpected error occurred: {e}")
        return False


def main():
    """Parse command-line arguments and initiate SSH command execution."""
    parser = argparse.ArgumentParser(description="Run multiple commands on Cisco SG300.")
    parser.add_argument('--host', required=True, help='IP address of the device')
    parser.add_argument('--username', required=True, help='Username for SSH login')
    parser.add_argument('--commands', help='Comma-separated list of commands to run')
    parser.add_argument('--file', help='Path to a text file with commands (one per line)')
    args = parser.parse_args()

    if not validate_ip(args.host):
        print(f"[ERROR] {args.host} is NOT a valid IP address.")
        return

    commands = load_commands(args)
    if not commands:
        return

    max_password_attempts = 3
    for attempt in range(1, max_password_attempts + 1):
        password = getpass.getpass(prompt=f"Enter SSH password (attempt {attempt}/{max_password_attempts}): ")
        success = connect_and_run_commands(args.host, args.username, password, commands)
        if success:
            break
        elif attempt == max_password_attempts:
            print(f"[ERROR] Maximum password attempts ({max_password_attempts}) reached. Exiting.")


# Entry point
if __name__ == "__main__":
    main()


# Example usage with commands:
# switch_connect_batch.py --host 192.168.1.102 --username cisco --commands "show version,show vlan,show running-config"

# Example usage with a batch file containing commands:
# switch_connect_batch.py --host 192.168.1.102 --username cisco --file commands.txt

