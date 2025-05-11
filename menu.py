import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import subprocess
import sys
import os

def launch_game():
    try:
        root.destroy()
        if not os.path.exists("C:\\Users\\ADMIN\\OneDrive\\Desktop\\chess-ai-main\\src\\main.py"):
            raise FileNotFoundError("Không tìm thấy file game")
        subprocess.Popen([sys.executable, "C:\\Users\\ADMIN\\OneDrive\\Desktop\\chess-ai-main\\src\\main.py"])
    except Exception as e:
        messagebox.showerror("Lỗi", f"Không thể khởi động game:\n{str(e)}")

# Tạo cửa sổ chính
root = tk.Tk()
root.title("Chess with AI")
root.geometry("800x600")
root.configure(bg="#2E3440")

# Load và hiển thị logo
try:
    img = Image.open("C:\\Users\\ADMIN\\OneDrive\\Desktop\\chess-ai-main\\images\\logo.jpg")
    img = img.resize((200, 200), Image.LANCZOS)
    logo_img = ImageTk.PhotoImage(img)
    logo_label = tk.Label(root, image=logo_img, bg="#2E3440")
    logo_label.image = logo_img  # Giữ reference
    logo_label.pack(pady=30)
except FileNotFoundError:
    messagebox.showwarning("Cảnh báo", "Không tìm thấy file logo!")
except Exception as e:
    messagebox.showwarning("Lỗi", f"Lỗi tải logo: {str(e)}")

# Tiêu đề game
title_label = tk.Label(root, 
                      text="CHESS WITH AI",
                      font=("Arial", 36, "bold"),
                      fg="#88C0D0",
                      bg="#2E3440")
title_label.pack(pady=10)

# Nút Play Game
play_button = tk.Button(root,
                       text="▶ BẮT ĐẦU",
                       command=launch_game,
                       font=("Arial", 24, "bold"),
                       bg="#88C0D0",
                       fg="#2E3440",
                       activebackground="#81A1C1",
                       activeforeground="#ECEFF4",
                       borderwidth=0,
                       padx=40,
                       pady=15,
                       cursor="hand2")

play_button.pack(pady=50)

# Hiệu ứng hover
def on_enter(e):
    play_button.config(bg="#81A1C1", fg="#ECEFF4")

def on_leave(e):
    play_button.config(bg="#88C0D0", fg="#2E3440")

play_button.bind("<Enter>", on_enter)
play_button.bind("<Leave>", on_leave)

root.mainloop()