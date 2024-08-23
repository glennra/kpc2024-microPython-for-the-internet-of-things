import socket

udp_ip = "192.168.2.2"
udp_port = 8001

text = "Hello1234567890"
text_length = len(text)
color_rgb = (255, 0, 255)  # Magenta color
value = 12345
v = ((value >> 8) & 0xFF, value & 0xFF)
message = bytearray([text_length]) + text.encode('utf-8') + bytearray(color_rgb) + bytearray(v)

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
n = sock.sendto(message, (udp_ip, udp_port))
print("sent", n)

