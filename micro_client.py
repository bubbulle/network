import pyaudio
import socket
import sys
import wave


FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 44100
CHUNK = 1024
RECORD_SECONDS = 60

audio = pyaudio.PyAudio()
stream = audio.open(format=FORMAT, channels=CHANNELS,
                rate=RATE, input=True,
                frames_per_buffer=CHUNK)
frames = []

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect the socket to the port where the server is listening
server_address = ('172.21.72.109', 10000)
print('connecting to ' + str(sys.stderr) + ' port ' + str(server_address))
sock.connect(server_address)


silence = chr(0)*CHUNK*CHANNELS*2

try:

    print("recording...")
    for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)

        if data == '':
            data = silence
        frames.append(data)
        # print('sending ' + str(data))
        sock.sendall(data)
        data = sock.recv(4096)
    print("finished recording")


finally:

    stream.stop_stream()
    stream.close()
    audio.terminate()
    print('closing socket')
    sock.close()
