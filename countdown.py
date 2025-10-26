import tkinter as tk
from tkinter import messagebox
import time
import threading
import winsound  # works on Windows; optional alternative for mac/linux below
# --- Helper function to format seconds as MM:SS or H:MM:SS ---
def format_time(seconds):
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    secs = seconds % 60
    if hours:
        return f"{hours:02}:{minutes:02}:{secs:02}"
    return f"{minutes:02}:{secs:02}"
# --- Timer class ---
class CountdownTimer:
    def __init__(self, root):
        self.root = root
        self.root.title("Countdown Timer")
        self.root.geometry("350x250")
        self.root.resizable(False, False)
        self.running = False
        self.remaining = 0
        # UI elements
        tk.Label(root, text="Enter time (seconds):", font=("Arial", 12)).pack(pady=5)
        self.entry = tk.Entry(root, font=("Arial", 14), justify='center')
        self.entry.pack(pady=5)

        self.time_label = tk.Label(root, text="00:00", font=("Arial", 36, "bold"))
        self.time_label.pack(pady=10)
        # Button frame
        btn_frame = tk.Frame(root)
        btn_frame.pack(pady=10)
        self.start_btn = tk.Button(btn_frame, text="Start", width=8, command=self.start_timer)
        self.start_btn.grid(row=0, column=0, padx=5)
        self.pause_btn = tk.Button(btn_frame, text="Pause", width=8, command=self.pause_timer, state='disabled')
        self.pause_btn.grid(row=0, column=1, padx=5)
        self.reset_btn = tk.Button(btn_frame, text="Reset", width=8, command=self.reset_timer, state='disabled')
        self.reset_btn.grid(row=0, column=2, padx=5)
    # --- Core timer logic ---
    def start_timer(self):
        if not self.running:
            try:
                total = int(self.entry.get())
                if total <= 0:
                    raise ValueError
                self.remaining = total
                self.running = True
                self.entry.config(state='disabled')
                self.start_btn.config(state='disabled')
                self.pause_btn.config(state='normal')
                self.reset_btn.config(state='normal')
                self.update_timer()
            except ValueError:
                messagebox.showerror("Invalid Input", "Please enter a positive integer.")

    def update_timer(self):
        if self.running:
            self.time_label.config(text=format_time(self.remaining))
            if self.remaining > 0:
                self.remaining -= 1
                self.root.after(1000, self.update_timer)
            else:
                self.running = False
                self.entry.config(state='normal')
                self.start_btn.config(state='normal')
                self.pause_btn.config(state='disabled')
                winsound.Beep(1000, 800)  # Play sound (Windows)
                messagebox.showinfo("Time's Up!", "Time's up!")
    def pause_timer(self):
        if self.running:
            self.running = False
            self.pause_btn.config(text="Resume")
        else:
            self.running = True
            self.pause_btn.config(text="Pause")
            self.update_timer()
    def reset_timer(self):
        self.running = False
        self.remaining = 0
        self.entry.config(state='normal')
        self.time_label.config(text="00:00")
        self.start_btn.config(state='normal')
        self.pause_btn.config(state='disabled', text="Pause")
        self.reset_btn.config(state='disabled')
# --- Main window setup ---
if __name__ == "__main__":
    root = tk.Tk()
    app = CountdownTimer(root)
    root.mainloop()
