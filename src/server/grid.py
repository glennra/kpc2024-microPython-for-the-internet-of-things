import tkinter as tk
from http.server import BaseHTTPRequestHandler, HTTPServer
import threading
import json
import socket
import paho.mqtt.client as mqtt

IP_LO = 101
IP_HI = 155

class RectangleGrid(tk.Tk):
    def __init__(self, rows=11, columns=5):
        super().__init__()

        self.rows = rows
        self.columns = columns

        # Main Frame
        self.main_frame = tk.Frame(self)
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        # Canvas for the grid
        self.canvas = tk.Canvas(self.main_frame)
        self.canvas.pack(fill=tk.BOTH, expand=True)

        # Text display at the bottom
        self.text_display = tk.Text(self.main_frame, height=4, state=tk.DISABLED)
        self.text_display.pack(fill=tk.X)

        self.rectangles = {}
        self.create_grid()

        self.bind("<Configure>", self.on_resize)

    def create_grid(self):
        for row in range(self.rows):
            for column in range(self.columns):
                rect_id = self.canvas.create_rectangle(0, 0, 1, 1, fill="white")
                text_id = self.canvas.create_text(0, 0, text="", fill="black", font=("Helvetica", 24))

                self.rectangles[(row, column)] = (rect_id, text_id)

        self.on_resize(None)

    def on_resize(self, event):
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()

        rect_width = canvas_width / self.columns
        rect_height = canvas_height / self.rows

        for row in range(self.rows):
            for column in range(self.columns):
                x1 = column * rect_width
                y1 = row * rect_height
                x2 = x1 + rect_width
                y2 = y1 + rect_height

                rect_id, text_id = self.rectangles[(row, column)]
                self.canvas.coords(rect_id, x1, y1, x2, y2)
                self.canvas.coords(text_id, (x1 + x2) / 2, (y1 + y2) / 2)

                # Calculate the font size to be a fraction of the rectangle's height
                font_size = int(rect_height * 0.3)
                self.canvas.itemconfig(text_id, font=("Helvetica", font_size))

    def set_rectangle(self, row, column, color="white", text=""):
        if (row, column) in self.rectangles:
            rect_id, text_id = self.rectangles[(row, column)]
            self.canvas.itemconfig(rect_id, fill=color)
            self.canvas.itemconfig(text_id, text=text)
            #self.add_text_to_display(f"Rectangle ({row}, {column}) updated with color {color} and text '{text}'.")

    def add_text_to_display(self, message):
            self.text_display.config(state=tk.NORMAL)
            self.text_display.insert(tk.END, message + '\n')
            self.text_display.see(tk.END)  # Scroll to the bottom
            self.text_display.config(state=tk.DISABLED)


class RequestHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        client_ip = ''
        try:
            # Get the client's IP address
            client_ip = self.client_address[0]
            last_octet = int(client_ip.split('.')[-1])

            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data)

            color = data.get('color', 'white')
            text = data.get('text', '')
            if text == '':
                raise RuntimeError("No 'text' field in JSON data")

            response_msg = b'Success'
            
            if IP_LO <= last_octet <= IP_HI:
                index = last_octet - IP_LO
                
                row = index // self.server.app.columns
                column = index % self.server.app.columns
                self.server.app.set_rectangle(row, column, color, text)
                self.send_response(200)
                self.end_headers()
                self.wfile.write(response_msg)
            else:
                self.send_response(400)
                self.end_headers()
                msg = f'Invalid index from IP address {last_octet}'
                self.wfile.write(msg.encode('utf-8'))
                #self.add_text_to_display(f"Rectangle ({row}, {column}) updated with color {color} and text '{text}'.")
                self.server.app.add_text_to_display(msg)
        except Exception as e:
            self.server.app.add_text_to_display(f"{client_ip} {str(e)}")
            

def run_http_server(app, server_class=HTTPServer, handler_class=RequestHandler, port=8000):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    httpd.app = app
    print(f'Starting HTTP server on port {port}...')
    httpd.serve_forever()

def decode_data(data):
    text_length = data[0]
    if len(data) < 1 + text_length + 5:
        raise RuntimeError("Not enough data: " + str(len(data)) + " < " + str( 1 + text_length + 5))
    text = data[1:1 + text_length].decode('utf-8')
    col_start = 1 + text_length
    r, g, b = data[col_start:col_start + 3]
    color = f'#{r:02x}{g:02x}{b:02x}'
    val_start = col_start + 3
    value = (data[val_start] << 8) + data[val_start+1]
    value = round(value/10, 1)
    text += str(value)

    return color, text

def run_udp_server(app, port=8001):
    udp_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp_sock.bind(('', port))
    print(f'Starting UDP server on port {port}...')
    
    while True:
        client_ip = ''
        try:
            data, addr = udp_sock.recvfrom(1024)
            client_ip = addr[0]
            last_octet = int(client_ip.split('.')[-1])

            if IP_LO <= last_octet <= IP_HI: 
                index = last_octet - IP_LO
            else:
                raise RuntimeError("IP not in range 101..150")
                # index = 0 # for testing from localhost

            row = index // app.columns
            column = index % app.columns

            # Assuming data is a bytearray with the first byte as text length, followed by text and then 3 bytes of RGB
            if len(data) < 8:  # Minimal length check
                continue

            #print("data bytes:", len(data))
                        
            color, text = decode_data(data)
            
            app.set_rectangle(row, column, color, text)
        except Exception as e:
            app.add_text_to_display(f"{client_ip} {str(e)}")


def on_mqtt_message(client, userdata, msg):
    try:
        data = bytearray(msg.payload)
        client_id = msg.topic.split('/')[-1]
        last_octet = int(client_id)

        if IP_LO - 100 <= last_octet <= IP_HI - 100:
            index = last_octet - 1
            row = index // userdata.columns
            column = index % userdata.columns
        else:
            raise RuntimeError("ID not in range 1..50")
            # index = 0 # for testing from localhost

        if len(data) < 6:  # Minimal length check
            raise RuntimeError("Not enough data: num bytes=" + str(len(data)))
            
        text_length = data[0]
        if len(data) < 1 + text_length + 5:
            raise RuntimeError("Not enough data: " + str(len(data)) + " < " + str( 1 + text_length + 5))

        color, text = decode_data(data)
        
        app.set_rectangle(row, column, color, text)

    except Exception as e:
        #print(f"Error processing MQTT message: {e}")
        app.add_text_to_display(f"Error processing MQTT message from client {client_id}: {str(e)}")


def run_mqtt_client(app, broker_address="localhost", port=1883, topic="grid/+"):
    client = mqtt.Client(userdata=app)
    client.on_message = on_mqtt_message

    # If this raises ConnectionRefusedError it is probably because you
    # forgot to start the broker. 
    client.connect(broker_address, port, 60)
    client.subscribe(topic)

    print(f"Connected to MQTT broker at {broker_address}:{port}, subscribed to topic '{topic}'")

    client.loop_forever()
if __name__ == "__main__":
    app = RectangleGrid()

    # Start the HTTP server in a separate thread
    http_server_thread = threading.Thread(target=run_http_server, args=(app,))
    http_server_thread.daemon = True
    http_server_thread.start()

    # Start the UDP server in a separate thread
    udp_server_thread = threading.Thread(target=run_udp_server, args=(app,))
    udp_server_thread.daemon = True
    udp_server_thread.start()

    # For MQTT a broker is also required. On Linux mosquitto can be used.
    # mosquitto.conf:
    #   listener 1883 0.0.0.0
    #   allow_anonymous true
    #
    # mosquitto -c mosquitto.conf

    # Start the MQTT client in a separate thread
    mqtt_client_thread = threading.Thread(target=run_mqtt_client, args=(app,))
    mqtt_client_thread.daemon = True
    mqtt_client_thread.start()

    app.mainloop()
