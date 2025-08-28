import tkinter as tk
from tkinter import messagebox

def find_topper():
    try:
        data_str = entry.get()
        if not data_str.strip():
            result_label.config(text="Please enter at least one score.", fg="#FF5733", font=("Helvetica", 12))
            return

        scores_data = {}
        for entry_item in data_str.split(','):
            parts = entry_item.strip().split(':')
            if len(parts) == 2:
                name, score_str = parts
                scores_data[name.strip()] = int(score_str.strip())
            else:
                raise ValueError("Incorrect format")

        if not scores_data:
            raise ValueError("No valid entries found")

        top_scorer = max(scores_data, key=scores_data.get)
        highest_score = scores_data[top_scorer]

        if highest_score > 95:
            result_label.config(text=f"Highest Score > 95 by {top_scorer} 🏆",
                                fg="#FFD700", font=("Arial", 16, "bold"))
        else:
            result_label.config(text=f"Highest Score: {highest_score} by {top_scorer}",
                                fg="#FFFFFF", font=("Arial", 16))

    except ValueError as e:
        result_label.config(text=f"Error: {e}. Please use 'Name:Score' format.",
                            fg="#FF5733", font=("Helvetica", 12))
    except Exception as e:
        result_label.config(text=f"An unexpected error occurred: {e}",
                            fg="#FF5733", font=("Helvetica", 12))

root = tk.Tk()
root.title("🏆 Top Scorer")
root.geometry("500x350")
root.configure(bg="#0A1828")

title_frame = tk.Frame(root, bg="#FFD700")
title_frame.pack(pady=20, padx=15, fill="x")
title_label = tk.Label(title_frame, text="🏆 TOP SCORER", bg="#FFD700", fg="#0A1828",
                       font=("Arial", 24, "bold"))
title_label.pack(ipady=10)

input_frame = tk.Frame(root, bg="#0A1828")
input_frame.pack(pady=10)

entry_label = tk.Label(input_frame, text="Enter scores (e.g., John:98, Jane:92):",
                       bg="#0A1828", fg="#FFFFFF", font=("Arial", 12))
entry_label.pack(pady=(0, 5))

entry = tk.Entry(input_frame, width=40, font=("Helvetica", 12),
                 bg="#1A2D3E", fg="#FFFFFF", insertbackground="#FFD700")
entry.pack(pady=5)
entry.bind("<Return>", lambda event=None: find_topper())

topper_button = tk.Button(root, text="Find Topper", command=find_topper,
                          bg="#FFD700", fg="#0A1828", font=("Helvetica", 14, "bold"),
                          bd=0, relief="flat", activebackground="#E5C100")
topper_button.pack(pady=20, ipadx=20, ipady=10)

result_label = tk.Label(root, text="", bg="#0A1828", fg="#FFFFFF", font=("Arial", 16))
result_label.pack(pady=(10, 0))

root.mainloop()
