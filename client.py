import threading
import socket
import datetime


client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(("127.0.0.1", 55555))
stop_threading = threading.Event()


def read_from_server():
    global stop_threading
    while True:
        if stop_threading.is_set() or client._closed:
            print("Closing the connection....")
            stop_threading.set()
            client.close()
            break

        try:
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            message = client.recv(1024).decode("utf-8")

            if not message.strip():
                print("server closed")
                stop_threading.set()
                break

            else:
                print(f"{timestamp}- {message}")

        except Exception as e:
            print(f"Error in read: {e}")
            client.close()
            stop_threading.set()
            break


def write():
    global stop_threading
    while True:
        if stop_threading.is_set() or client._closed:
            print("Closing the connection....")
            stop_threading.set()
            break
        try:

            message = input("")
            if message.startswith("@"):
                client.send(message.encode("utf-8"))

            elif message == "!rename":
                new_nickName = message.split(" ", 1)[1]
                client.send(f"!rename {new_nickName}".encode("utf-8"))

            elif message.startswith("/admin"):
                client.send(message.encode("utf-8"))

            elif message == "!online":
                client.send(message.encode("utf-8"))

            elif message == "!quit":
                client.send(message.encode("utf-8"))
                stop_threading.set()
                break

            elif message == "!help":
                help_message = """
                Available commands:
                !quit      - Disconnect from the server and exit the program.
                !online     - List all online users.
                @<user>:    - Send a private message to a specific user (e.g. @username: message).
                !rename <new_name> - Change your nickname.
                !help       - List all available commands for you."""
                print(help_message)
                continue

            elif message.startswith("!anon"):
                client.send(message.encode("utf-8"))
            elif message == "/kick":
                client.send(message.encode("utf-8"))
            else:
                if not client._closed:
                    client.send(message.encode("utf-8"))
                else:
                    continue

        except Exception as e:
            print(f"Error in write: {e}")
            stop_threading.set()
            break


recv_thread = threading.Thread(target=read_from_server)
recv_thread.start()

write_thread = threading.Thread(target=write)
write_thread.start()
