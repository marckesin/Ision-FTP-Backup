import ftplib
import os
import socket
import sys
from datetime import datetime
import progressbar
from dotenv import load_dotenv

load_dotenv()
user = os.getenv("USER")
passwd = os.getenv("PASSWD")

ORANGE = "\033[33m"
RED = "\033[0;31m"
LIGHT_GREEN = "\033[1;32m"
END = "\033[0m"
IP, backup_name = sys.argv[1:]
ftp = ftplib.FTP()


def clear():
    """Function that clear the screen"""
    os.system("cls" if os.name == "nt" else "clear")


def check_ftp_server(host, port=21):
    """Checks if a server is responding on default FTP port"""
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
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
    """Function that copy files from the FTP server"""
    if not os.path.exists(folder):
        os.mkdir(folder)
    os.chdir(folder)
    for file in progressbar.progressbar(files, redirect_stdout=True):
        try:
            print(f"{ORANGE}{file}{END} está sendo copiado para {folder}")
            with open(f"{file}", "wb") as fp:
                ftp.retrbinary(f"RETR {file}", fp.write)
        except ftplib.all_errors:
            continue
    os.chdir("../")


def ftp_connection():
    """Starts a connection between host and server"""
    if check_ftp_server(IP):
        try:
            ftp.connect(IP, timeout=5)
            ftp.login(user=user, passwd=passwd)
            print(f"Login realizado com sucesso em {IP}")
            print(ftp.getwelcome(), "\n")
        except ftplib.error_perm as e:
            print(f"Falha ao realizar login >>> {RED}{e}{END}")
    else:
        print(f"Servidor FTP não está respondendo em {IP}")


def main():
    """Main function """
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
    except AttributeError as e:
        print(f"{e}")


if __name__ == "__main__":
    clear()
    main()
