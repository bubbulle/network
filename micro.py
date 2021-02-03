import pyaudio
import socket
import sys
from _thread import start_new_thread


FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 44100
CHUNK = 1024
ThreadCount = 0


audio = pyaudio.PyAudio()
stream = audio.open(format=FORMAT, channels=CHANNELS,
                rate=RATE, input=True,
                frames_per_buffer=CHUNK)

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to the port
server_address = ('172.21.72.109', 10000)
print('starting up on ' + str(sys.stderr) + ' port ' + str(server_address))
sock.bind(server_address)

# Listen for incoming connections
sock.listen(1)

def read(connection):
    try:
        #print('connection from' + str(client_address))

        audio = pyaudio.PyAudio()
        stream = audio.open(format=FORMAT, channels=CHANNELS,
                            rate=RATE, output=True,
                            frames_per_buffer=CHUNK)

        # Receive the data in small chunks and retransmit it
        while True:
            data = connection.recv(4096)
            #print('received ' + str(data))
            if data:
                #print(type(data))
                # waveFile.writeframes(data)
                stream.write(data)
                #print('sending data back to the client')
                connection.sendall(data)

            else:
                print('no more data from' + str(client_address))
                break

    finally:
        # Clean up the connection
        audio.terminate()
        connection.close()

while True:
    connection, client_address = sock.accept()
    #print('Connected to: ' + client_address[0] + ':' + str(client_address[1]))
    start_new_thread(read, (connection, ))
    ThreadCount += 1
    #print('Thread Number: ' + str(ThreadCount))
sock.close()
