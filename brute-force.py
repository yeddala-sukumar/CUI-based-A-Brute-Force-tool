import time
import threading
import tkinter as tk
from tkinter import messagebox, filedialog

class BruteForceApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Brute Force Code Cracker")

        # Variables
        self.target_code = tk.StringVar()
        self.length = tk.IntVar(value=4)
        self.is_running = False
        self.progress = tk.DoubleVar(value=0)
        self.log_file = None

        # UI Elements
        self.create_widgets()

    def create_widgets(self):
        # Target Code
        tk.Label(self.root, text="Target Code:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.target_entry = tk.Entry(self.root, textvariable=self.target_code)
        self.target_entry.grid(row=0, column=1, padx=5, pady=5)

        # Code Length
        tk.Label(self.root, text="Code Length:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
        self.length_entry = tk.Entry(self.root, textvariable=self.length)
        self.length_entry.grid(row=1, column=1, padx=5, pady=5)

        # Start Button
        self.start_button = tk.Button(self.root, text="Start", command=self.start_brute_force)
        self.start_button.grid(row=2, column=0, padx=5, pady=5)

        # Stop Button
        self.stop_button = tk.Button(self.root, text="Stop", command=self.stop_brute_force, state="disabled")
        self.stop_button.grid(row=2, column=1, padx=5, pady=5)

        # Progress Bar
        self.progress_label = tk.Label(self.root, text="Progress:")
        self.progress_label.grid(row=3, column=0, padx=5, pady=5, sticky="e")
        self.progress_bar = tk.Label(self.root, textvariable=self.progress)
        self.progress_bar.grid(row=3, column=1, padx=5, pady=5)

        # Log File Button
        self.log_button = tk.Button(self.root, text="Set Log File", command=self.set_log_file)
        self.log_button.grid(row=4, column=0, columnspan=2, pady=10)

    def set_log_file(self):
        self.log_file = filedialog.asksaveasfilename(
            title="Save Log File",
            defaultextension=".log",
            filetypes=(("Log Files", "*.log"), ("All Files", "*.*")),
        )
        if self.log_file:
            messagebox.showinfo("Log File", f"Log file set to: {self.log_file}")

    def start_brute_force(self):
        target = self.target_code.get()
        try:
            length = int(self.length.get())
        except ValueError:
            messagebox.showerror("Error", "Code length must be a number.")
            return

        if not target.isdigit() or len(target) != length:
            messagebox.showerror("Error", "Please enter a valid numeric target code of the specified length.")
            return

        self.is_running = True
        self.start_button.config(state="disabled")
        self.stop_button.config(state="normal")

        # Run brute force in a separate thread
        threading.Thread(target=self.brute_force_code, args=(target, length), daemon=True).start()

    def stop_brute_force(self):
        self.is_running = False
        self.start_button.config(state="normal")
        self.stop_button.config(state="disabled")

    def brute_force_code(self, target_code, length):
        start_time = time.time()
        attempts = 0
        max_attempts = 10**length

        # Open log file if specified
        log_file = open(self.log_file, "w") if self.log_file else None

        for code in range(max_attempts):
            if not self.is_running:
                if log_file:
                    log_file.close()
                return

            guess = f"{code:0{length}}"  # Format as zero-padded string
            if log_file:
                log_file.write(f"Trying: {guess}\n")
            attempts += 1

            # Update progress
            progress = (code + 1) / max_attempts * 100
            self.progress.set(f"{progress:.2f}% - Trying: {guess}")
            self.root.update()

            # Check if the code matches
            if guess == target_code:
                end_time = time.time()
                messagebox.showinfo(
                    "Success",
                    f"Code cracked! The code is {guess}\n"
                    f"Attempts: {attempts}\n"
                    f"Time taken: {end_time - start_time:.2f} seconds",
                )
                break

        if log_file:
            log_file.close()

        # Reset UI state
        self.is_running = False
        self.start_button.config(state="normal")
        self.stop_button.config(state="disabled")
        self.progress.set("0.00%")

# Main function to run the app
if __name__ == "__main__":
    root = tk.Tk()
    app = BruteForceApp(root)
    root.mainloop()
