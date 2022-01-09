# Shachar Oz

import socket
import datetime
import sys

DEBUG = True
CHUNK_SIZE = 2048
STOP_COMMS = False

def loggin(data,sent):
    if DEBUG:
        if sent == 'c':
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
    loggin(data[:20],'h')
    return data

def send_data(data,sock):
    """
    sends data with the option of logging
    :param data: data in bytes to send
    :param sock: socket
    :return:
    """
    loggin(data[:20],'c')
    sock.send(data)

def send_mail(sock):
    """
    Builds and sends the mail
    :param sock: socket
    :return:
    """
    users = []
    all_users = False
    while not all_users:
        data=input("Enter Username of the person you want to send an email to (Leave empty to stop): ")
        if data != "":
            users.append(data)
        if len(users) != 0 and data == "":
            all_users = True

    mail_subject = input("Enter the subject of the email (# will be replaced with !): ")
    mail_body = input("Enter the subject of the email (# will be replaced with !): ")
    mail_subject = mail_subject.replace('#','!')
    mail_body = mail_body.replace('#','!')

    to_message = b"TO:"
    for user in users:
        to_message+= user.encode()
        to_message+= b":"
    to_message = to_message.rstrip(':')

    to_sent = b"MALTO#" + datetime.datetime.now().strftime('%Y%m%d %H:%M').encode() + b"#" + to_message + b"#" + mail_subject.encode()+b"#"+mail_body.encode()+b"###"
    send_data(to_sent,sock)


def handle_request(option,sock):
    """
    handles the client request to the server
    :param option: (bool) does the user want to send an email or not
    :param sock: socket
    :return:
    """
    if option:
        send_mail(sock)
    else:
        send_data(b"B_Y_E",sock)
        STOP_COMMS = True


def tkmall(data):
    mail_amount = data.split('#')[0]
    emails_raw = data[data.find('#')+1:]
    emails= []
    for i in range(0,mail_amount):
        #[From,date,subject,body]
        emails.append([emails_raw.split('#')[i],emails_raw.split('#')[i+1],emails_raw.split('#')[i+2],emails_raw.split('#')[i+3]])
        i += 3
    with open('client_mails.txt','w') as file:
        for i in range(0,len(emails)):
            print("=================")
            print(f"Date: {emails[i][1].decode()}    From: {emails[i][0].decode()}")
            print(f"Subject: {emails[i][2].decode()}")
            print(f"body: {emails[i][3].decode()}")
            print("=================")
            file.write("=================")
            file.write(f"Date: {emails[i][1].decode()}    From: {emails[i][0].decode()}")
            file.write(f"Subject: {emails[i][2].decode()}")
            file.write(f"body: {emails[i][3].decode()}")
            file.write("=================")

def nopnd():
    print("No Mail waiting for you")

def gotit():
    print("Mail sent")

def handle_response(sock):
    """
    handles the response got from the host
    :param sock: socket
    :return:
    """
    rec = recv_data(sock)
    message_code = rec.split('#')[0]
    data = rec[rec.find('#')+1:]
    if message_code == b"TKMALL":
        tkmall(data)
    elif message_code == b"NOPND":
        nopnd()
    elif message_code == b"GOTIT":
        gotit()


def handle_host(sock):
    """
    handles all host related stuff
    :param sock: socket
    :return:
    """
    while not STOP_COMMS:
        handle_response(sock)
        handle_request(want_send(),sock)


def want_send():
    pass

def main(ip):
    sock = socket.socket()
    sock.connect((ip,587))
    rec_info = sock.recv(1024)
    if  rec_info[:rec_info.find(b'###')+2] == b"HELLO###":
        sock.send(b"OLLEH#"+bytes(sys.argv[2])+b"#"+bytes(sys.argv[2])+b"###")
        handle_host(sock)
    sock.close()

if __name__ == '__main__':
    if len(sys.argv) < 1:
        print("Remember to run with parameters in to following format: IP Username Password")
    else:
        main(sys.argv[1])