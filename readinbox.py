import imaplib
import socket
import data

# Forzar el uso de IPv4
imaplib._MAXLINE = 10000000
imaplib.IMAP4_SSL.address = (socket.getaddrinfo('imap.gmail.com', 993, socket.AF_INET)[0][4])

SERVER = 'imap.gmail.com'
USER = data.USER
PASS = data.PASS

# Conectar al servidor Gmail
server = imaplib.IMAP4_SSL(SERVER)

# Login
server.login(USER, PASS)

# Seleccionar la Bandeja Inbox
status, count = server.select('Inbox')
status, data = server.fetch(count[0], '(UID BODY[TEXT])')

flag = str((data[0][1]))
print(flag)

server.close()
server.logout()
