import socket
import tkinter as tk

UDP_IP = "172.16.192.43"
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


def on_set_ip_address():
    global UDP_IP
    UDP_IP = entry_ip_address.get()


root = tk.Tk()

button_forward = tk.Button(root, text="前进", width=20, height=5)
button_forward.grid(row=0, column=1)
button_forward.bind("<ButtonPress>", lambda event: on_button_press(MESSAGE_FORWARD))
button_forward.bind("<ButtonRelease>", lambda event: on_button_release())

button_left = tk.Button(root, text="左转", width=10, height=5)
button_left.grid(row=1, column=0)
button_left.bind("<ButtonPress>", lambda event: on_button_press(MESSAGE_LEFT))
button_left.bind("<ButtonRelease>", lambda event: on_button_release())

button_stop = tk.Button(root, text="停止", width=20, height=5, bg="red", command=lambda: on_button_release())
button_stop.grid(row=1, column=1)

button_right = tk.Button(root, text="右转", width=10, height=5)
button_right.grid(row=1, column=2)
button_right.bind("<ButtonPress>", lambda event: on_button_press(MESSAGE_RIGHT))
button_right.bind("<ButtonRelease>", lambda event: on_button_release())

button_backward = tk.Button(root, text="后退", width=20, height=5)
button_backward.grid(row=2, column=1)
button_backward.bind("<ButtonPress>", lambda event: on_button_press(MESSAGE_BACKWARD))
button_backward.bind("<ButtonRelease>", lambda event: on_button_release())

label_ip_address = tk.Label(root, text="IP Address:")
label_ip_address.grid(row=3, column=0)

entry_ip_address = tk.Entry(root, width=20)
entry_ip_address.grid(row=3, column=1)

button_set_ip_address = tk.Button(root, text="设置", width=10, command=on_set_ip_address)
button_set_ip_address.grid(row=3, column=2)

root.mainloop()
