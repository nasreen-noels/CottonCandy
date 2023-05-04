#!/usr/bin/python3
# Analyze output from robot line following algorithm.


import socket
import time

sensor_address = '98:da:e0:01:1f:2c'


def connect():
    """
    Return a bluetooth socket connection to the robot
    This function is responsible for connecting to the robot via bluetooth.
    """
    print("Connecting...", end='', flush=True)
    s = socket.socket(socket.AF_BLUETOOTH, socket.SOCK_STREAM, socket.BTPROTO_RFCOMM)
    s.connect((sensor_address, 1))
    print("Success")
    return s

"""
This function does the following:
1. Opens the file that contains commands
2. Iterates through the file 
"""
def reverse_commands(command_file):
    command_log = []
    with open(command_file) as file:
        for line in file:
            command = line.split()
            logs = {'timestamp': command[0], 'action': command[1]}
            command_log.append(logs)
            if command[1] == 'START':
                logs['action'] = 's'
            if command[1] == 'STOPPED':
                logs['action'] = '0'
            if command[1] == 'FORWARD':
                logs['action'] = 'b'
            if command[1] == 'REVERSE':
                logs['action'] = 'g'
            if command[1] == 'LEFT':
                logs['action'] = 'r'
            if command[1] == 'RIGHT':
                logs['action'] = 'l'
    command_log.reverse()

    timestamps = []
    # Creating a list of timestamps
    for log in command_log:
        timestamps.append(int(log['timestamp']))

    # Update the timestamps for the reversed list
    for index, log in enumerate(command_log):
        if index == 0 or index == 1:
            log['timestamp'] = 0
        else:
            log['timestamp'] = (timestamps[index - 2] - timestamps[index - 1]) + command_log[index - 1]['timestamp']
    print(command_log)
    return command_log

def processing_status(current_command, total_commands):
    if current_command == 0:
        print('just starting...')
    elif current_command == int(total_commands/2):
        print('almost there!')


def process_commands(command_log):
    print(command_log)
    s = connect()
    ln = len(command_log)
    for index, logs in enumerate(command_log):
        print(logs)
        s.sendall(logs['action'].encode('utf-8'))
        next_item = 0
        if index < (ln - 1):
            next_item = command_log[index + 1]
            processing_status(index, len(command_log))
            time.sleep((next_item['timestamp'] - logs['timestamp']) / 1000)
        else:
            time.sleep(0)
    s.close()
def process_previous_commands(command_log):
    prev = 0
    for logs in command_log:
        ((time.sleep(logs['timestamp'] - prev) / 1000))
        prev = logs['timestamp']

def main():
    reversed_commands = reverse_commands('commands_new.txt')
    process_commands(reversed_commands)


if __name__ == "__main__":
    main()



