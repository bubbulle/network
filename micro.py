import pyaudio
import socket
import sys
# import wave


FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 44100
CHUNK = 1024
RECORD_SECONDS = 5


audio = pyaudio.PyAudio()
stream = audio.open(format=FORMAT, channels=CHANNELS,
                rate=RATE, input=True,
                frames_per_buffer=CHUNK)

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to the port
server_address = ('172.21.72.143', 10000)
print('starting up on ' + str(sys.stderr) + ' port ' + str(server_address))
sock.bind(server_address)

# Listen for incoming connections
sock.listen(1)

while True:
    # Wait for a connection
    print('waiting for a connection')
    connection, client_address = sock.accept()

    try:
        print('connection from' + str(client_address))

        audio = pyaudio.PyAudio()
        stream = audio.open(format=FORMAT, channels=CHANNELS,
                        rate=RATE, output=True,
                        frames_per_buffer=CHUNK)


        # Receive the data in small chunks and retransmit it
        while True:
            try:
                data = connection.recv(4096)
                # print('received ' + str(data))
                if data:
                    stream.write(data)

                    print('sending data back to the client')
                    connection.sendall(data)


                else:
                    print('no more data from' + str(client_address))
                    break

            except:
                i=0

    finally:
        # Clean up the connection
        audio.terminate()
        connection.close()
