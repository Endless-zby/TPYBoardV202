import socket
import tkinter as tk

UDP_IP = "192.168.123.255"
UDP_PORT = 5005
MESSAGE_STOP = "stop"
MESSAGE_FORWARD = "forward"
MESSAGE_BACKWARD = "backward"
MESSAGE_LEFT = "left"
MESSAGE_RIGHT = "right"


def send_udp_message(message):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.sendto(bytes(message, "utf-8"), (UDP_IP, UDP_PORT))
    sock.close()


def on_button_press(message):
    send_udp_message(message)


def on_button_release():
    send_udp_message(MESSAGE_STOP)


root = tk.Tk()

button_forward = tk.Button(root, text="Forward")
button_forward.bind("<ButtonPress>", lambda event: on_button_press(MESSAGE_FORWARD))
button_forward.bind("<ButtonRelease>", lambda event: on_button_release())
button_forward.pack()

button_backward = tk.Button(root, text="Backward")
button_backward.bind("<ButtonPress>", lambda event: on_button_press(MESSAGE_BACKWARD))
button_backward.bind("<ButtonRelease>", lambda event: on_button_release())
button_backward.pack()

button_left = tk.Button(root, text="Left")
button_left.bind("<ButtonPress>", lambda event: on_button_press(MESSAGE_LEFT))
button_left.bind("<ButtonRelease>", lambda event: on_button_release())
button_left.pack()

button_right = tk.Button(root, text="Right")
button_right.bind("<ButtonPress>", lambda event: on_button_press(MESSAGE_RIGHT))
button_right.bind("<ButtonRelease>", lambda event: on_button_release())
button_right.pack()

button_stop = tk.Button(root, text="Stop", command=lambda: on_button_release())
button_stop.pack()

root.mainloop()
