import os
import sys
import subprocess
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk

# -------------------- Ensure Correct Working Directory --------------------
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# -------------------- Root Window --------------------
root = tk.Tk()
root.geometry("600x450")
root.title("MentaLift")  # App name

# -------------------- Set Crisp App Icon --------------------
try:
    icon_image = Image.open("icon.png")  # Ensure icon.png is in the same folder
    icon_image = icon_image.resize((256, 256), Image.LANCZOS)
    icon_photo = ImageTk.PhotoImage(icon_image)
    root.iconphoto(True, icon_photo)
except Exception as e:
    print("⚠ Couldn't load icon:", e)

# -------------------- Main Frame --------------------
main_frame = tk.Frame(root, bg="#f0f8ff")
main_frame.pack(fill="both", expand=True)

# -------------------- App Title with Icon --------------------
try:
    # Load a smaller icon for the title
    icon_image_small = Image.open("icon.png").resize((40, 40), Image.LANCZOS)
    icon_photo_small = ImageTk.PhotoImage(icon_image_small)

    # Label with text + image
    title_label = tk.Label(
        main_frame,
        text=" MentaLift",  # space for spacing
        font=("Helvetica", 30, "bold"),
        bg="#f0f8ff",
        fg="#333",
        image=icon_photo_small,
        compound="left"  # image to the left of text
    )
    title_label.image = icon_photo_small  # keep reference
    title_label.pack(pady=50)

except Exception as e:
    print("⚠ Couldn't load icon for title:", e)
    # Fallback text-only title
    title_label = tk.Label(
        main_frame,
        text="MentaLift",
        font=("Helvetica", 30, "bold"),
        bg="#f0f8ff",
        fg="#333"
    )
    title_label.pack(pady=50)

# -------------------- Function to Run the Kivy App --------------------
def run_existing_app():
    try:
        # Launch main.py in a new Python process (so Tkinter doesn’t block)
        subprocess.Popen([sys.executable, "main.py"])
    except Exception as e:
        messagebox.showerror("Error", f"Failed to launch app:\n{e}")

# -------------------- Buttons --------------------
check_button = tk.Button(
    main_frame,
    text="Check My Mental Status",
    font=("Arial", 16, "bold"),
    width=25,
    height=2,
    bg="#4CAF50",
    fg="white",
    activebackground="#45a049",
    activeforeground="white",
    cursor="hand2",
    command=run_existing_app
)
check_button.pack(pady=20)

# Optional: About button
about_button = tk.Button(
    main_frame,
    text="About MentaLift",
    font=("Arial", 12, "bold"),
    bg="#2196F3",
    fg="white",
    activebackground="#1E88E5",
    activeforeground="white",
    cursor="hand2",
    command=lambda: messagebox.showinfo(
        "About MentaLift",
        "MentaLift – Your digital companion for mental well-being.\n"
        "Designed to monitor mental status and provide daily insights."
    )
)
about_button.pack(pady=10)

# -------------------- Run the App --------------------
root.mainloop()
