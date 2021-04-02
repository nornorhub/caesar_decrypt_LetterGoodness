#
# Connect over TCP to the following server 'localhost', 10000
# Initiate communication with GET to retrieve the encrypted messages.
# Then return the messages decrypted to the server,
# taking care to ensure each message is split on to a newline
#
 

import socket
import itertools

clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
clientsocket.connect(('127.0.0.1', 10000))
clientsocket.send(b'GET')
sentences = str(clientsocket.recv(1024)).split('\\n')[1:-1]

letterGoodness = [.0817,.0149,.0278,.0425,.1270,.0223,.0202, 
                  .0609,.0697,.0015,.0077,.0402,.0241,.0675,
									.0751,.0193,.0009,.0599,.0633,.0906,.0276,
                 	.0098,.0236,.0015,.0197,.0007]

def shift(S, n):
   word = ''
   for i in S:
      if ord(i) == 32:
         word += ' '
      elif ord(i)+n > 90:
         a = n-(90-ord(i))+64
         word += chr(a)
      else:
         word +=chr(ord(i)+n)
   return word
def TGS(x): # Total goodness of string
   TGC = 0 # Total goodness of character
   for i in x:
      if ord(i) == 32:
         continue
      TGC += letterGoodness[ord(i)-65]
   return TGC
A = sentences[0]
LOSS = [shift(A,n) for n in range (1,27)] # List of shifted strings
LOTG = [TGS(x) for x in LOSS]
a = LOTG.index(max(LOTG))
dc = LOSS[a]

B = sentences[1]
LOSS = [shift(B,n) for n in range (1,27)] # List of shifted strings
LOTG = [TGS(x) for x in LOSS]
b = LOTG.index(max(LOTG))
dc2 = LOSS[b]

C = sentences[2]
LOSS = [shift(C,n) for n in range (1,27)] # List of shifted strings
LOTG = [TGS(x) for x in LOSS]
c = LOTG.index(max(LOTG))
dc3 = LOSS[c]

clientsocket.send((dc + "\n" + dc2 + "\n" + dc3).encode())
print(clientsocket.recv(1024))
