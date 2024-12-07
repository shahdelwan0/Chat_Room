import threading
import socket
import random
import difflib

host = "127.0.0.1"
port = 55555
valid_commands = [
    "/kick",
    "/admin",
    "/mute",
    "unmute",
    "!rename",
    "!help",
    "@",
    "!anon",
    "!quit",
]
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()

clients = []
nick_names = []
muted_users = []

admin_sock = None
admin_pass = "123"
pw = None
with open("nrandom_nicknames.txt", "r") as file:
    avaialbe_nicknames = file.read().splitlines()


def broadcast(message, sender=None):
    for client in clients[:]:
        try:
            if sender and client == sender:
                continue
            client.send(message.encode("utf-8"))
        except socket.error as se:
            try:
                index = clients.index(client)
                client.close()
                clients.pop(index)
                nick_names.pop(index)
            except ValueError:
                print("Client already removed or mismatched lists.")


def send_private_msg(sender, recipient, msg):
    if recipient in nick_names:
        recipient_index = nick_names.index(recipient)
        clients[recipient_index].send(f"(Private) {sender}: {msg}\n".encode("utf-8"))
    else:
        sender_index = clients.index(sender)
        clients[sender_index].send("Recipient not found.\n".encode("utf-8"))


def handle_client(client):
    global admin_sock
    admin_mode = False
    index = clients.index(client)
    nick_name = nick_names[index]
    while True:
        try:
            if client in clients:
                message = client.recv(1024).decode("utf-8")
                if not any(message.startswith(cmd) for cmd in valid_commands):
                    close_match = difflib.get_close_matches(
                        message.split()[0], valid_commands, n=1, cutoff=0.5
                    )
                    if close_match:
                        client.send(
                            f"Did you mean '{close_match[0]}'?\n".encode("utf-8")
                        )
                    else:
                        client.send(
                            "Unknown command! Type !help to list the available commands.\n".encode(
                                "utf-8"
                            )
                        )
                        continue

                if nick_name in muted_users:
                    client.send(
                        "You are muted and cannot send messages.\n".encode("utf-8")
                    )
                    continue

                elif message.startswith("@"):
                    try:
                        recipient, msg = message[1:].split(":", 1)
                        send_private_msg(nick_name, recipient, msg)
                    except ValueError:
                        client.send(
                            "Invalid private message format. Use @recipient:message\n".encode(
                                "utf-8"
                            )
                        )

                elif message.startswith("!online"):
                    online_users = ", ".join(nick_names)
                    client.send(f"Online users: {online_users}".encode("utf-8"))

                elif message.startswith("!quit"):
                    client.send("You have disconnected from the chat.".encode("utf-8"))
                    print(f"User \033[1m{nick_name}\033[0m disconnected.")
                    broadcast(f"{nick_name} has left the chat.")
                    clients.remove(client)
                    nick_names.remove(nick_name)
                    client.close()
                    break

                elif message.startswith("!rename"):

                    new_nickName = message[8:]
                    if new_nickName in nick_names:
                        client.send(f"\033[1m{new_nickName}\033[0m already taken!\n")
                    else:
                        nick_name = nick_names[clients.index(client)]
                        nick_names[clients.index(client)] = new_nickName
                        broadcast(
                            f"\033[1m{nick_name}\033[0m is now known as \033[1m{new_nickName}\033[0m.",
                            sender=client,
                        )
                        client.send(
                            f"You have successfully changed your name to \033[1m{new_nickName}\033[0m.\n".encode(
                                "utf-8"
                            )
                        )
                        nick_name = new_nickName

                elif message.startswith("/admin"):
                    pw = message[7:].strip()
                    if pw == admin_pass:
                        admin_mode = True
                        client.send("You are now the admin\n".encode("utf-8"))
                        print(
                            f"\033[1m{nick_names[clients.index(client)]}\033[0m is now in admin position!"
                        )
                    else:
                        client.send("Admin password is wrong.")

                elif message.startswith("/kick") and admin_mode:
                    if pw == admin_pass:
                        target = message[6:]
                        admin_sock = client
                        if target in nick_names:
                            try:
                                target_index = nick_names.index(target)
                                target_sock = clients[target_index]
                                target_sock.send("kicked".encode("utf-8"))
                                print(
                                    f"User \033[1m{target}\033[0m has been kicked by and admin!"
                                )
                                broadcast(
                                    f"We kicked \033[1m{target}\033[0m from the chat!",
                                    admin_sock,
                                )
                                print("closing")
                                print("closed")
                                target_sock.close()
                                clients.remove(target_sock)
                                print("removed")
                                nick_names.remove(target)
                                break
                            except:
                                print("error kicking client")
                        else:
                            client.send(f"User not found for kicking".encode("utf-8"))

                    else:
                        client.send("Incorrect admin password.\n".encode("utf-8"))

                elif message.startswith("/mute") and admin_mode:
                    if pw == admin_pass:
                        muted_user = message[6:]
                        muted_users.append(muted_user)
                        muted_user_index = nick_names.index(muted_user)
                        muted_user_sock = clients[muted_user_index]
                        muted_user_sock.send(
                            "you have been muted by the admin, other clients won't receive your messages from now".encode(
                                "utf-8"
                            )
                        )
                        broadcast(
                            f"\033[1m{muted_user}\033[0m has been muted by the admin.",
                            client,
                        )

                    else:
                        client.send("Incorrect admin password.\n".encode("utf-8"))

                elif message.startswith("/unmute") and admin_mode:
                    if pw == admin_pass:
                        unmuted_user = message[8:]
                        unmute(unmuted_user)
                    else:
                        client.send("Incorrect admin password.\n".encode("utf-8"))

                elif message.startswith("!anon"):
                    anon_message = message[6:]
                    broadcast(
                        f"\033[1m[Anonymous Message]\033[0m: {anon_message}", None
                    )

                else:
                    if client in clients:
                        broadcast(f"{nick_name}: {message}", sender=client)
                    else:
                        print("kk")
            else:
                print("Not found")

        except Exception as e:
            if client in clients:
                clients.remove(client)
                nick_names.remove(nick_name)
                broadcast(f"\033[1m{nick_name}\033[0m has left the chat!", None)
                print(f"Connection was lost with \033[1m{nick_name}\033[0m")
                client.close()
                break
            else:
                print(f"User \033[1m{nick_name}\033[0m has disconnected")


def accept_connections():
    while True:
        client, address = server.accept()
        print(f"Connection established: {address}")

        while avaialbe_nicknames:
            nick_name = random.choice(avaialbe_nicknames)
            if nick_name not in nick_names:
                break

        if not avaialbe_nicknames:
            client.send(
                "No more nicknames available. Disconnecting...\n".encode("utf-8")
            )
            client.close()
            continue

        nick_names.append(nick_name)
        clients.append(client)

        print(f"User \033[1m{nick_name}\033[0m connected.")
        broadcast(f"\033[1m{nick_name}\033[0m has joined the chat!", client)
        client.send(
            f"You were assigned nickname \033[1m{nick_name}\033[0m\n".encode("utf-8")
        )
        client.send(f"Enjoy chatting!\n".encode("utf-8"))

        thread = threading.Thread(target=handle_client, args=(client,))
        thread.start()


def unmute(user):
    if user in muted_users:
        muted_users.remove(user)
        broadcast(f"\033[1m{user}\033[0m has been unmuted by the admin.", None)
    else:
        print(f"User \033[1m{user}\033[0m is not in the muted list or does not exist.")


print("Server Successfully Started.")
accept_connections()
