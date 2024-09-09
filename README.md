
# Chat Client Application

## Description
This project is a simple client-side chat application built using Python's socket module for networking and Tkinter for creating a graphical user interface (GUI). The chat application allows users to connect to a server, send and receive messages, and export the chat history in a user-friendly format. The interface maintains a clean, modern look with a dark theme, and users can send messages by pressing the Enter key.

## Key Features
- **Real-time Chat:** Users can send and receive messages instantly.
- **Dark Theme UI:** The chat window features a modern dark theme, making it visually appealing.
- **Export Chat History:** Users can export their chat history as either a plain text file or a JSON file.
- **Custom Message Alignment:** Messages sent by the user are right-aligned, while received messages are left-aligned.
- **Enter Key Functionality:** Allows users to send messages by pressing the Enter key.

## Installation Instructions
1. Ensure Python 3.x is installed on your machine.
2. Clone the repository or download the project files.
3. Open a terminal or command prompt in the project directory.
4. Install the necessary dependencies (if any) using pip:
    ```bash
    pip install tkinter
    ```
5. Run the client application using:
    ```bash
    python client.py
    ```

## Usage Instructions
1. Enter your username in the provided field.
2. Click "Join" to connect to the server.
3. Type your messages in the input box at the bottom and either press Enter or click "Send."
4. To export the chat, click the "Export Chat" button. Choose between saving as a text file or a JSON file.

## Technologies Used
- **Python:** The primary language used for networking and GUI creation.
- **Tkinter:** A Python library used for building the graphical user interface.
- **Socket Programming:** Enables real-time communication between the client and the server.
- **JSON:** Used for exporting chat history in a structured format.

