# Real-Time Chatroom Application
This is a Python-based real-time chat application designed to provide a smooth and user-friendly messaging experience. With features like dynamic user management, admin privileges, and private messaging, it serves as an excellent project for exploring socket programming and multi-threaded application design.

## 🚀 Features
### User Functionality
* **Dynamic Nickname Assignment:** Automatically assigns unique nicknames to new users.
* **Rename Option:** Change your nickname anytime using the !rename command.
* **Private Messaging:** Send direct messages using @username: message.
* **Command Help:** Use !help to list all available commands.
* **Anonymous Messaging:** Broadcast anonymous messages with !anon.
* **View Online Users:** Check the list of connected users with the !online command.
___
### Admin Functionality
* **Admin Authentication:** Secure access to admin-specific commands with a password.
* **User Moderation**:
  * **/kick <user>**: Remove a user from the chat.
  * **/mute <user>**: Silence a user from sending messages.
  * **/unmute <user>**: Restore a muted user's messaging privileges.
___
### Robust Design
* **Threaded Architecture:** Efficiently handles multiple clients simultaneously.
* **Command Suggestions:** Offers smart suggestions for mistyped commands.
* **Error Handling:** Ensures stability and prevents server crashes due to unexpected inputs.
___
## 🛠️ Technologies Used
* **Python:** The core programming language.
* **Socket Programming:** Facilitates server-client communication.
* **Threading:** Enables handling multiple clients concurrently.
* **Difflib:** Provides smart command suggestions for better user experience.
* **File Handling:** Manages dynamic nickname allocation.
