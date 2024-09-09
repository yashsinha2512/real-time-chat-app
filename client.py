import socket
import threading
import tkinter as tk
from tkinter import scrolledtext, messagebox, filedialog
import json

HOST = '127.0.0.1'
PORT = 1234

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Chat history for export
chat_history = []

# Add a message to the message box with alignment for sent/received
def add_message(message, sender=""):
    message_box.config(state=tk.NORMAL)

    # Customize alignment based on sender (right-align for "You", left-align for others)
    alignment = 'right' if sender == 'You' else 'left'
    
    if sender:
        formatted_message = f"{sender}: {message}\n"
    else:
        formatted_message = f"{message}\n"

    # Add message to the box based on alignment
    message_box.insert(tk.END, formatted_message)

    # Save to chat history for export
    chat_history.append({'sender': sender, 'message': message})

    # Apply alignment
    message_box.tag_add("message", "end-1c linestart", "end-1c lineend")
    message_box.tag_configure("right", justify="right", foreground="#7289DA")
    message_box.tag_configure("left", justify="left", foreground="#99AAB5")

    message_box.tag_add(alignment, "end-1c linestart", "end-1c lineend")
    message_box.config(state=tk.DISABLED)
    message_box.yview(tk.END)  # Auto-scroll to the latest message

# Export chat history
def export_chat():
    file_format = filedialog.asksaveasfilename(defaultextension=".txt", 
                                               filetypes=[("Text Files", "*.txt"), ("JSON Files", "*.json")])
    
    if file_format.endswith('.txt'):
        with open(file_format, 'w') as f:
            for chat in chat_history:
                f.write(f"{chat['sender']}: {chat['message']}\n")
    elif file_format.endswith('.json'):
        with open(file_format, 'w') as f:
            json.dump(chat_history, f, indent=4)
    else:
        messagebox.showerror("Save Error", "Unsupported file format")

# Connect to the server
def connect():
    try:
        client.connect((HOST, PORT))
        add_message("[SERVER] Connected to the server")
    except:
        messagebox.showerror("Connection error", f"Failed to connect to {HOST}:{PORT}")
        return

    username = username_textbox.get()
    if username:
        client.sendall(username.encode())
    else:
        messagebox.showerror("Invalid username", "Username cannot be empty")
        return

    threading.Thread(target=listen_for_messages_from_server, args=(client,)).start()

    # Disable username input after joining
    username_textbox.config(state=tk.DISABLED)
    username_button.config(state=tk.DISABLED)

# Send the message to the server
def send_message(event=None):  # Optional event for Enter key binding
    message = message_textbox.get()
    if message:
        client.sendall(message.encode())
        add_message(message, "You")  # Right-align messages you send
        message_textbox.delete(0, tk.END)
    else:
        messagebox.showerror("Empty message", "Message cannot be empty")

# Listen for incoming messages from the server
def listen_for_messages_from_server(client):
    while True:
        try:
            message = client.recv(2048).decode('utf-8')
            if message:
                username, content = message.split('~')
                if username != username_textbox.get():  # Avoid displaying your own message twice
                    add_message(content, username)  # Left-align messages from others
            else:
                break
        except:
            messagebox.showerror("Error", "Lost connection to the server")
            break

# Tkinter GUI setup
root = tk.Tk()
root.geometry("600x600")
root.title("Chat Client")
root.configure(bg="#2C2F33")  # Set background for the dark theme

# Create top frame for entering username
top_frame = tk.Frame(root, bg="#2C2F33")
top_frame.pack(side=tk.TOP, fill=tk.X)

username_label = tk.Label(top_frame, text="Enter Username:", font=("Helvetica", 14), bg="#2C2F33", fg="white")
username_label.pack(side=tk.LEFT, padx=10, pady=10)

username_textbox = tk.Entry(top_frame, font=("Helvetica", 14))
username_textbox.pack(side=tk.LEFT, padx=10)

username_button = tk.Button(top_frame, text="Join", font=("Helvetica", 14), command=connect, bg="#7289DA", fg="white")
username_button.pack(side=tk.LEFT, padx=10)

export_button = tk.Button(top_frame, text="Export Chat", font=("Helvetica", 14), command=export_chat, bg="#7289DA", fg="white")
export_button.pack(side=tk.LEFT, padx=10)

# Middle frame for the message display
middle_frame = tk.Frame(root, bg="#2C2F33")
middle_frame.pack(pady=10)

# Add a scrolled text box for the chat window
message_box = scrolledtext.ScrolledText(middle_frame, state=tk.DISABLED, wrap=tk.WORD, height=25, width=70, bg="#36393F", fg="white")
message_box.pack()

# Bottom frame for message input and export button
bottom_frame = tk.Frame(root, bg="#2C2F33")
bottom_frame.pack(side=tk.BOTTOM, fill=tk.X)

message_textbox = tk.Entry(bottom_frame, font=("Helvetica", 14), width=45)
message_textbox.pack(side=tk.LEFT, padx=10, pady=10)

message_textbox.bind("<Return>", send_message)  # Bind Enter key to send_message function

message_button = tk.Button(bottom_frame, text="Send", font=("Helvetica", 14), command=send_message, bg="#7289DA", fg="white")
message_button.pack(side=tk.LEFT, padx=10, pady=10)

# Main loop to keep the GUI running
root.mainloop()
