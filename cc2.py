#!/usr/bin/python3
# Analyze output from robot line following algorithm.

# 1. read commands from text file
import socket
import time



sensor_address = '98:da:e0:01:1f:2c'

def connect():
  print("Connecting...",end='',flush=True)
  s = socket.socket(socket.AF_BLUETOOTH, socket.SOCK_STREAM, socket.BTPROTO_RFCOMM)
  s.connect((sensor_address, 1))
  print("Success")
  return s

def recv_data(s):
  print("Receiving...")
  while True:
    data = str(s.recv(1024),encoding='ASCII')
    print(data,end='')

def send_data(s):
  while True:
      print("send> ",end='')
      data = input()
      if not data:
          break
      s.sendall(data.encode('utf-8'))
  s.close()
  print("Done")
command_log = []
with open('robotcommands.txt') as f:
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
s = connect()
# loop over all the commands
# for each command in the list sleep for difference in time and send command
# s.sendall(data.encode('utf-8'))
prev = 0
for logs in command_log:
    s.sendall(logs['action'].encode('utf-8'))
    time.sleep((logs['timestamp'] - prev) / 1000)
    prev = logs['timestamp']
    print(logs)
s.close()
