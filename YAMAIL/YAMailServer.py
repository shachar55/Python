# Shachar Oz

import socket
import datetime
import threading

DEBUG = True
CHUNK_SIZE = 2048
USERS = []
ALL_MAILS = {}

def loggin(data,sent):
    if DEBUG:
        if sent == 'h':
            print(f"{datetime.datetime.now().strftime('%H:%M:%S')}  TO: {data}")
        else:
            print(f"{datetime.datetime.now().strftime('%H:%M:%S')}  FROM: {data}")

def recv_data(sock):
    """
    receives data until hits "###" with logging option
    :param sock: socket
    :return:
    """
    data = ""
    while True:
        if data.find(b"###") >= 0:
            break
        data += sock.recv(CHUNK_SIZE)
    loggin(data[:20],'c')
    return data

def send_data(data,sock):
    """
    sends data with the option of logging
    :param data: data in bytes to send
    :param sock: socket
    :return:
    """
    loggin(data[:20],'h')
    sock.send(data)



def handle_response(sock,user):
    data = recv_data(sock)
    mail = MailInfo(data,user)
    return mail.Decide()

def update_user(sock,user):
    """
    updating the user if he got mail
    :param sock: socket
    :param user: current user connected
    :return:
    """
    if user not in ALL_MAILS.keys():
        send_data(b"NOPND###",sock)
    else:
        to_send = b"TKALL#NUM:" + len(ALL_MAILS.items(user)).encode() + b"#"
        for i in range(0,len(ALL_MAILS.items(user))):
            data = ALL_MAILS[user][i]
            to_send+=b"FROM:"+data[0]+b"#"+data[1]+b"#"+data[2]+b"#"+data[3]+b"#"
        to_send+=b"##"
        send_data(to_send, sock)
        ALL_MAILS.pop(user)


def login(login_data):
    for user in USERS:
        if user[0] == login_data.split('#')[1] and user[1] == login_data.split('#')[2][:-3]:
            return True
    return False


def handle_client(sock,id,addr):
    send_data(b"HELLO###",sock)
    login_data = recv_data(sock)
    login_attempt = login(login_data)
    current_user=login_data.split('#')[1]
    if login_attempt:
        update_user(sock,current_user)
        while True:
            done = handle_response(sock,current_user)
            if done:
                break
    sock.close()

def main():
    srv_sock = socket.socket()
    srv_sock.bind(("0.0.0.0",587))
    srv_sock.listen(20)

    threads = []
    i = 0
    while True:
        cli_sock, addr = srv_sock.accept()
        t = threading.Thread(target=handle_client,args=(cli_sock,str(i),addr))
        t.start()
        threads.append(t)
        i+=1

def load_users():
    with open('YAMail_users.txt','r') as file:
        while True:
            data =file.readline()
            if data == "":
                break
            USERS.append([data[5:data.find('-')],data[data.find('-')+1:-1]])



if __name__ == '__main__':
    load_users()
    main()

class MailInfo():
    def __init__(self,data,current_user,sock):
        self.data = data
        self.current_user = current_user
        self.sock =sock

    def malto(self):
        users = self.data.split('#')[2][2:].split(':')
        date = self.data.split('#')[1]
        subject = self.data.split('#')[3]
        body = self.data.split('#')[4]
        for user in users:
            mail = [self.curret_user, date, subject, body]  # [from,date,subject,body]
            if user in ALL_MAILS.keys():
                ALL_MAILS[user].append(mail)
            else:
                ALL_MAILS.update({user: mail})

    def Decide(self):
        if self.data.split('#')[0] == b"MALTO":
            self.malto(self.data, self.sock, self.user)
            send_data(b"GOTIT###")
            return False
        elif self.data.split('#')[0] == b"B_Y_E###":
            return True