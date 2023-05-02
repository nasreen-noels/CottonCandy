#!/usr/bin/python3
# Analyze output from robot line following algorithm.

# 1. read commands from text file
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
    with open(command_file) as f:
        for line in f:
            x = line.split()
            logs = {'timestamp': x[0], 'action': x[1]}
            command_log.append(logs)
            if x[1] == 'START':
                logs['action'] = 'STOPPED'
            if x[1] == 'FORWARD':
                logs['action'] = 'REVERSE'
            if x[1] == 'LEFT':
                logs['action'] = 'RIGHT'
            if x[1] == 'RIGHT':
                logs['action'] = 'LEFT'
    command_log.reverse()
    for logs in command_log:
        vals = float(x[0])
        logs['timestamp'] = float(vals) - float(logs['timestamp'])
    return command_log


# for index, item in enumerate
# elif
# int
# index
def command_check(current_command, total_commands):
    if current_command == 0:
        print('just starting...')
    elif current_command == int(total_commands/2):
        print('almost there!')
# s = connect()
# loop over all the commands
# for each command in the list sleep for difference in time and send command
# s.sendall(data.encode('utf-8'))

def process_commands(command_log):
    # s = connect()
    for index, logs in enumerate(command_log):
        # s.sendall(logs['action'].encode('utf-8'))
        ln = len(command_log)
        next_item = 0
        if index < (ln - 1):
            next_item = command_log[index + 1]
            command_check(index, len(command_log))
            time.sleep((next_item['timestamp'] - logs['timestamp']) / 1000)
            print(next_item)
        else:
            time.sleep(0)
    # s.close()

def main():
    reversed_commands = reverse_commands('robotcommands.txt')
    process_commands(reversed_commands)


if __name__ == "__main__":
    main()
