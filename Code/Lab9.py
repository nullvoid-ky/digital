import tkinter as tk
from tkinter import messagebox
import random
import time

class BinaryQuizApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Binary Operations Quiz")

        # Set the window to fullscreen
        self.root.attributes('-fullscreen', True)
        
        self.win_count = 0
        self.lose_count = 0
        self.total_time = 0

        # Create GUI components
        self.create_widgets()
        self.new_question()

    def create_widgets(self):
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_rowconfigure(1, weight=1)
        self.root.grid_rowconfigure(2, weight=1)
        self.root.grid_rowconfigure(3, weight=1)
        self.root.grid_rowconfigure(4, weight=1)

        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_columnconfigure(1, weight=1)

        self.label_binary0 = tk.Label(self.root, font=('Helvetica', 48), anchor='center')
        self.label_binary0.grid(row=0, column=0, columnspan=2, pady=20)

        self.label_binary1 = tk.Label(self.root, font=('Helvetica', 48), anchor='center')
        self.label_binary1.grid(row=1, column=0, columnspan=2, pady=20)

        self.label_operation = tk.Label(self.root, font=('Helvetica', 48), anchor='center')
        self.label_operation.grid(row=2, column=0, columnspan=2, pady=20)

        self.label_time = tk.Label(self.root, font=('Helvetica', 36), anchor='center', text="Time: 0.000")
        self.label_time.grid(row=3, column=0, columnspan=2, pady=20)

        self.entry_hex = tk.Entry(self.root, font=('Helvetica', 48), justify='center')
        self.entry_hex.grid(row=4, column=0, columnspan=2, pady=20)

        self.entry_hex.bind("<Return>", self.on_submit)

        self.submit_button = tk.Button(self.root, text="Submit", font=('Helvetica', 36), command=self.check_answer)
        self.submit_button.grid(row=5, column=0, columnspan=2, pady=20)

        self.stats_label = tk.Label(self.root, font=('Helvetica', 30), anchor='center')
        self.stats_label.grid(row=6, column=0, columnspan=2, pady=20)

    def generate_random_binary(self):
        return format(random.randint(0, 255), '08b')

    def bin_to_dec(self, binary_str):
        return int(binary_str, 2)

    def dec_to_hex(self, decimal_num):
        return format(decimal_num & 0xFF, '02X')  # Format as two digits

    def format_binary(self, binary_str):
        return f"{binary_str[:4]} {binary_str[4:]}"

    def new_question(self):
        self.bin_num0 = self.generate_random_binary()
        self.bin_num1 = self.generate_random_binary()

        self.operation = random.choice(['+', '-', '^', '<<'])

        formatted_bin_num0 = self.format_binary(self.bin_num0)
        formatted_bin_num1 = self.format_binary(self.bin_num1)

        self.label_binary0.config(text=f"Binary 0: {formatted_bin_num0}")
        self.label_binary1.config(text=f"Binary 1: {formatted_bin_num1}")
        self.label_operation.config(text=f"Operation: {self.operation}")

        dec_num0 = self.bin_to_dec(self.bin_num0)
        dec_num1 = self.bin_to_dec(self.bin_num1)

        if self.operation == '+':
            self.correct_sum = (dec_num0 + dec_num1) & 0xFF
        elif self.operation == '-':
            self.correct_sum = (dec_num0 - dec_num1) & 0xFF
        elif self.operation == '^':
            self.correct_sum = dec_num0 ^ dec_num1
        elif self.operation == '<<':
            self.correct_sum = (dec_num0 << 1) & 0xFF

        self.correct_hex = self.dec_to_hex(self.correct_sum)

        self.entry_hex.delete(0, tk.END)

        self.start_time = time.time()
        self.update_timer()

    def update_timer(self):
        elapsed_time = time.time() - self.start_time
        self.label_time.config(text=f"Time: {elapsed_time:.3f}")
        self.root.after(10, self.update_timer)

    def check_answer(self):
        user_input = self.entry_hex.get().strip().upper()
        end_time = time.time()
        response_time = end_time - self.start_time

        if user_input == self.correct_hex:
            self.win_count += 1
            messagebox.showinfo("Result", f"Correct! Time taken: {response_time:.2f} seconds")
        else:
            self.lose_count += 1
            messagebox.showerror("Result", f"Wrong! The correct answer was {self.correct_hex}. Time taken: {response_time:.2f} seconds")

        self.total_time += response_time
        self.update_stats()
        self.new_question()

    def on_submit(self, event):
        self.check_answer()

    def update_stats(self):
        total_attempts = self.win_count + self.lose_count
        win_rate = (self.win_count / total_attempts * 100) if total_attempts > 0 else 0
        average_time = (self.total_time / total_attempts) if total_attempts > 0 else 0
        stats_text = (f"Wins: {self.win_count}\n"
                      f"Losses: {self.lose_count}\n"
                      f"Win Rate: {win_rate:.2f}%\n"
                      f"Average Time: {average_time:.2f} seconds")
        self.stats_label.config(text=stats_text)

if __name__ == "__main__":
    root = tk.Tk()
    app = BinaryQuizApp(root)
    root.mainloop()
