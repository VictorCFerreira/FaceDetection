import socket
import binascii

def MandarUDP():

    ip = "177.101.141.181"
    port = 13604

    msgString = binascii.a2b_hex("3cf169693d3e")


    print('Sending {arr} to {ip}:{port}')
    sock = socket.socket(socket.AF_INET,
                        socket.SOCK_DGRAM)

    dest = (ip, port)
    sock.sendto(msgString, dest)