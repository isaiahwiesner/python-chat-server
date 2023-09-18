import socket
import threading
import tkinter
import tkinter.scrolledtext
from tkinter import simpledialog

HOST = "127.0.0.1" # localhost IP
# HOST = "10.16.26.156" # private IP
#   connect to 142.55.3.15
PORT = 9090

class Client:
    # Initialization
    def __init__(self, host, port):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((host, port))
        msg = tkinter.Tk()
        msg.geometry("500x300")
        msg.title("Nickname")
        msg.withdraw()
        self.nickname = simpledialog.askstring("Nickname", "Please choose a nickname", parent=msg)
        self.gui_done = False
        self.running = True
        gui_thread = threading.Thread(target=self.gui_loop)
        recv_thread = threading.Thread(target=self.receive)
        gui_thread.start()
        recv_thread.start()

    # GUI Loop
    def gui_loop(self):
        self.win = tkinter.Tk()
        self.win.title("Chat")

        self.chat_label = tkinter.Label(self.win, text="Chat:")
        self.chat_label.config(font=("Arial", 12))
        self.chat_label.pack(padx=20, pady=5)

        self.text_area = tkinter.scrolledtext.ScrolledText(self.win)
        self.text_area.pack(padx=20, pady=5)
        self.text_area.config(state="disabled")

        self.msg_label = tkinter.Label(self.win, text="Message:")
        self.msg_label.config(font=("Arial", 12))
        self.msg_label.pack(padx=20, pady=5)

        self.input_area = tkinter.Text(self.win, height=3)
        self.input_area.config(font=("Arial", 12))
        self.input_area.pack(padx=20, pady=5)

        self.send_btn = tkinter.Button(master=self.win, text="Send", command=self.write)
        self.send_btn.config(font=("Arial", 12))
        self.send_btn.pack(padx=20, pady=5)

        self.gui_done = True

        self.win.protocol("WM_DELETE_WINDOW", self.stop)

        self.win.mainloop()

    # Receive
    def receive(self):
        while self.running:
            try:
                message = self.sock.recv(1024).decode("utf-8")
                if message == "NICK":
                    self.sock.send(self.nickname.encode("utf-8"))
                else:
                    if self.gui_done:
                        self.text_area.config(state="normal")
                        self.text_area.insert("end", message)
                        self.text_area.yview("end")
                        self.text_area.config(state="disabled")
            except ConnectionAbortedError:
                break
            except:
                print("Error")
                self.sock.close()
                self.sock.send(f'{self.nickname} has disconnected from the server.'.encode("utf-8"))
                break

    # Write
    def write(self):
        message = f'{self.nickname}: {self.input_area.get("1.0", "end")}'
        self.sock.send(message.encode("utf-8"))
        self.input_area.delete("1.0", "end")

    # Stop
    def stop(self):
        self.running = False
        self.win.destroy()
        self.sock.close()
        self.sock.send(f'{self.nickname} has disconnected from the server.'.encode("utf-8"))
        exit(0)

if __name__ == "__main__":
    client = Client(HOST, PORT)