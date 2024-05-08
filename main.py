import ftplib
import os
import socket
import sys
from datetime import datetime
from dotenv import load_dotenv


load_dotenv()
user = os.getenv("USER")
passwd = os.getenv("PASSWD")

ORANGE = '\033[33m'
RED = "\033[0;31m"
LIGHT_GREEN = "\033[1;32m"
END = "\033[0m"
IP, backup_name = sys.argv[1:]
ftp = ftplib.FTP()


def check_ftp_server(host, port=21):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(5)
        sock.connect((host, port))
        print(f"O servidor em {host} na porta {port} está disponível")
        return True
    except socket.error:
        print(f"Falha ao conectar em {RED}{host}{END} na porta {RED}{port}{END}")
        return False
    finally:
        sock.close()


def copy_files(files, folder):
    if not os.path.exists(folder):
        os.mkdir(folder)
    os.chdir(folder)
    for file in files:
        print(f"{ORANGE}{file}{END} está sendo copiado para {folder}")
        with open(f"{file}", "wb") as fp:
            ftp.retrbinary(f"RETR {file}", fp.write)
    os.chdir("../")


def ftp_connection():
    if check_ftp_server(IP):
        try:
            ftp.connect(IP, timeout=5)
            ftp.login(user=user, passwd=passwd)
            print(f"Login realizado com sucesso em {IP}")
            print(ftp.getwelcome(), "\n")
        except Exception as e:
            print(f"Falha ao realizar login >>> {RED}{e}{END}")
    else:
        print(f"Servidor FTP não está respondendo em {IP}")


def main():
    try:
        ftp_connection()
        directories = ["C", "E"]
        date = f"{datetime.now():%d%m%Y}"
        backup_folder_name = f"{backup_name}_{date}"
        root_directory = f"C:\\Users\\R\\Desktop\\{backup_folder_name}"

        if not os.path.exists(root_directory):
            print(f"Criando {root_directory}")
            os.mkdir(root_directory)
        os.chdir(root_directory)

        for folder in directories:
            ftp.cwd(folder)
            files = ftp.nlst()
            copy_files(files, folder)
            ftp.cwd("../")

        print(f"{LIGHT_GREEN}Transferência finalizada.{END}")
        ftp.quit()
    except Exception as e:
        print(f"{e}")


if __name__ == "__main__":
    main()
