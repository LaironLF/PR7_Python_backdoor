import os
import socket

list_command: list[str] = ["cd", "remove", "listdir"]

def do_remove_file():
    pass

def do_help_command():
    print("help - описание команд \n"
          "cd папка\\папка1\\папка2 - перемещение в папку по адресу абсолютному или относительному\n"
          "listdir - вывод названий файлов и папок в текущей папке\n" 
          "send названиефайла.расширение - загрузка файла в текущую папку\n"
          "recv названиефайла.расширение - закачка файла с клиента на сервер из текущей папки клиента\n"
          "set_save_dir путь\\к\\папке - назначение папки сохранения на сервере\n"
          "")

def do_cd(command :str):
    # cd /home/user/test
    list_command = command.split(' ')
    os.chdir(list_command[1]) 
    
def do_listdir(sock: socket.socket):
    # file_list = os.listdir(os.path.dirname(os.path.realpath(__file__)))
    file_list = os.listdir(os.getcwd())
    string_send: str = ""
    for file in file_list:
        string_send += file + "\n"
    sock.send(string_send.encode())      
    
def do_say_hello(sock: socket.socket):
    # say_hello
    print("Hellow")
    sock.send(f'Client said hello'.encode())

def do_send_file(sock: socket.socket, command :str):
    file_name: str = command.split(" ")[1]
    file_size: int = os.stat(file_name).st_size
    
    sock.send(f"{file_size}".encode())
    
    with open(file_name, "rb") as file:
        while True:
            data: bytes = file.read(1024)
            if not data:
                break
            sock.send(data)
    pass

def do_recieve_file(sock: socket.socket, command :str, save_dir: str):
    file_name: str = command.split(" ")[1]
    file_name = file_name.split("\\")[-1]
    file_size: int = int(sock.recv(1024).decode())
    recieved_data: int = 0
    
    with open(save_dir + "\\" +file_name, "wb") as file:
        while file_size > recieved_data:
            data: bytes = sock.recv(1024)
            if data:
                file.write(data)
                recieved_data += len(data)
  
