
import tkinter as tk
from tkinter import scrolledtext
import threading
from assistant import execute_command
from voice import VoiceAssistant


class JarvisGUI:

    def __init__(self, root):
        self.root = root
        self.root.title("eJARVIS 2.0 - Smart Voice Assistant")
        self.root.geometry("900x650")
        self.root.minsize(650, 500)
        self.root.configure(bg="#0b1220")

        self.voice = VoiceAssistant()
        self.busy = False

        self.create_interface()

        greeting = "Hello! I am eJARVIS 2.0. How can I help you?"

        self.add_message("eJARVIS", greeting)

        self.root.after(
          500,
         lambda: threading.Thread(
         target=self.voice.speak,
         args=(greeting,),
         daemon=True
         ).start()
        )   

    def create_interface(self):

        # Header
        header = tk.Frame(self.root, bg="#111c30", pady=18)
        header.pack(fill="x")

        title = tk.Label(
            header,
            text="eJARVIS 2.0",
            font=("Segoe UI", 25, "bold"),
            fg="#38bdf8",
            bg="#111c30"
        )
        title.pack()

        subtitle = tk.Label(
            header,
            text="SMART PERSONAL VOICE ASSISTANT",
            font=("Segoe UI", 9),
            fg="#94a3b8",
            bg="#111c30"
        )
        subtitle.pack(pady=4)

        # Status
        self.status = tk.Label(
            self.root,
            text="● ONLINE",
            font=("Segoe UI", 10, "bold"),
            fg="#22c55e",
            bg="#0b1220"
        )
        self.status.pack(pady=8)

        # Chat window
        self.chat = scrolledtext.ScrolledText(
            self.root,
            wrap=tk.WORD,
            font=("Segoe UI", 11),
            bg="#111c30",
            fg="#e2e8f0",
            insertbackground="white",
            relief="flat",
            padx=15,
            pady=15,
            state="disabled"
        )
        self.chat.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=10
        )

        self.chat.tag_config(
            "user",
            foreground="#38bdf8",
            font=("Segoe UI", 11, "bold")
        )

        self.chat.tag_config(
            "jarvis",
            foreground="#4ade80",
            font=("Segoe UI", 11, "bold")
        )

        # Input area
        bottom = tk.Frame(self.root, bg="#0b1220")
        bottom.pack(fill="x", padx=20, pady=15)

        self.entry = tk.Entry(
            bottom,
            font=("Segoe UI", 12),
            bg="#1e293b",
            fg="white",
            insertbackground="white",
            relief="flat"
        )
        self.entry.pack(
            side="left",
            fill="x",
            expand=True,
            ipady=12,
            padx=(0, 8)
        )

        self.entry.bind("<Return>", lambda event: self.send_message())

        send_button = tk.Button(
            bottom,
            text="SEND",
            command=self.send_message,
            bg="#0284c7",
            fg="white",
            font=("Segoe UI", 10, "bold"),
            relief="flat",
            padx=18,
            pady=10,
            cursor="hand2"
        )
        send_button.pack(side="left", padx=4)

        mic_button = tk.Button(
            bottom,
            text="🎤",
            command=self.start_listening,
            bg="#7c3aed",
            fg="white",
            font=("Segoe UI", 14),
            relief="flat",
            padx=14,
            pady=5,
            cursor="hand2"
        )
        mic_button.pack(side="left", padx=4)

        # Footer buttons
        footer = tk.Frame(self.root, bg="#0b1220")
        footer.pack(pady=(0, 12))

        tk.Button(
            footer,
            text="CLEAR CHAT",
            command=self.clear_chat,
            bg="#334155",
            fg="white",
            relief="flat",
            padx=15,
            pady=7
        ).pack(side="left", padx=5)

        tk.Button(
            footer,
            text="EXIT",
            command=self.root.destroy,
            bg="#991b1b",
            fg="white",
            relief="flat",
            padx=15,
            pady=7
        ).pack(side="left", padx=5)

    def add_message(self, sender, message):

        self.chat.config(state="normal")

        if sender == "You":
            tag = "user"
        else:
            tag = "jarvis"

        self.chat.insert(
            tk.END,
            sender + ": ",
            tag
        )

        self.chat.insert(
            tk.END,
            message + "\n\n"
        )

        self.chat.config(state="disabled")
        self.chat.see(tk.END)

    def send_message(self):

        if self.busy:
            return

        command = self.entry.get().strip()

        if not command:
            return

        self.entry.delete(0, tk.END)
        self.process_command(command)

    def process_command(self, command):

        self.add_message("You", command)

        if command.strip().lower() in [
            "exit", "quit", "stop", "bye", "band ho jao"
        ]:
            self.add_message("eJARVIS", "Goodbye! Have a nice day.")
            self.root.after(1200, self.root.destroy)
            return

        self.busy = True
        self.status.config(text="● PROCESSING", fg="#facc15")

        threading.Thread(
            target=self.handle_command,
            args=(command,),
            daemon=True
        ).start()

    def handle_command(self, command):

        response = execute_command(command)

        self.root.after(
            0,
            lambda: self.show_response(response)
        )

        if response != "EXIT":
            self.voice.speak(response)

    def show_response(self, response):

        self.add_message("eJARVIS", response)

        self.status.config(text="● ONLINE", fg="#22c55e")
        self.busy = False

    def start_listening(self):

        if self.busy:
            return

        self.busy = True
        self.status.config(text="● LISTENING...", fg="#facc15")

        threading.Thread(
            target=self.listen_and_process,
            daemon=True
        ).start()

    def listen_and_process(self):

        command = self.voice.listen()

        self.root.after(
            0,
            lambda: self.receive_voice(command)
        )

    def receive_voice(self, command):

        if command.startswith("No speech detected") or \
           command.startswith("Sorry") or \
           command.startswith("Internet") or \
           command.startswith("Microphone") or \
           command.startswith("Voice error"):

            self.add_message("eJARVIS", command)
            self.status.config(text="● ONLINE", fg="#22c55e")
            self.busy = False
            return

        self.busy = False
        self.process_command(command)

    def clear_chat(self):

        self.chat.config(state="normal")
        self.chat.delete("1.0", tk.END)
        self.chat.config(state="disabled")

        self.add_message(
            "eJARVIS",
            "Chat cleared. How can I help you?"
        )
