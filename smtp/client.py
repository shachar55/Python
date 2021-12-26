import socket
import base64

"""[Client]
    1. Connect
    2. 
"""
username = b"shacharOz@icgmail.dox"#input("Enter Mail: ").encode() #temp
password = b"11570times6"#input("Enter Password: ").encode() #temp
full =  b"\x00"+username+b"\x00"+password

def sendRecv(sock):
    recv = sock.recv(1024)
    print(recv)
    sock.send(b"EHLO pc4-13\r\n")
    recv = sock.recv(1024)
    print(recv)  
    
    sock.send(b"AUTH LOGIN "+base64.b64encode(full)+ b"\r\n")
    recv = sock.recv(1024)
    print(base64.b64decode(recv[4:-2]))

    sock.send(username + b"\r\n")
    recv = sock.recv(1024)
    sock.send(password + b"\r\n")
    recv = sock.recv(1024)
    print(recv)
    sock.send(b"MAIL FROM: <%s>\r\n"%(username))
    recv = sock.recv(1024)
    print(recv)
    sock.send(b"RCPT TO:resha@bads.com\r\n")
    recv = sock.recv(1024)
    print(recv)
    sock.send(b"DATA\r\n")
    recv = sock.recv(1024)
    print(recv)
    sock.send(b"Subject: Get Ready!\r\n.\r\n")
    recv = sock.recv(1024)
    print(recv)
    sock.send(b"QUIT\r\n")
    recv = sock.recv(1024)
    print(recv)
    
    
def main():
    sock = socket.socket()
    try:
        sock.connect(("192.168.0.109",25))
        print("Connected successfully")
    except:
        print("Failed!")
    sendRecv(sock)
    
    
if __name__ == "__main__":
    main()