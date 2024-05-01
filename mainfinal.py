#them check link
import tkinter as tk
from pytube import YouTube
import customtkinter
import subprocess

# Global variable to track error status
error_status = False

def startDownLoad(option):
    global error_status
    try:
        ytLink = link.get()
        # Kiểm tra định dạng link
        if not ytLink.startswith("https://www.youtube.com/watch?v="):
            error_status = True
            raise ValueError("Invalid YouTube link format!")
        
        ytObject = YouTube(ytLink, on_progress_callback=on_progress)
        if option == "highQuality":
            video = ytObject.streams.get_highest_resolution()
        elif option == "lowQuality":
            video = ytObject.streams.get_lowest_resolution()
        elif option == "audio":
            video = ytObject.streams.get_audio_only()
        else:
            return

        title.configure(text=ytObject.title, text_color="white")
        finishLabel.configure(text="")
        video.download()
        finishLabel.configure(text="Download Successful !", text_color="green")
        error_status = False  # Reset error status if download is successful

    except Exception as e:
        finishLabel.configure(text="Download Error!", text_color="red")
        error_status = True
        print(e)

def open_player():
    subprocess.Popen(["python", "playervid.py"])

# progress bar function
def on_progress(stream, chuck, bytes_remaining):
    total_size = stream.filesize
    bytes_download = total_size - bytes_remaining
    percentage_of_completion = bytes_download / total_size * 100
    per = str(int(percentage_of_completion))
    progress.configure(text=per + '%')
    progress.update()

    # update Progress bar
    progressbar.set(float(percentage_of_completion) / 100)

# Create a pop-up error message
def show_error_message():
    tk.messagebox.showerror("Error", "Invalid YouTube link format!")

# system settings
customtkinter.set_appearance_mode("system")
customtkinter.set_default_color_theme("blue")

# our app frame
app = customtkinter.CTk()
app.geometry("720x480")
# Lấy kích thước màn hình
screen_width = app.winfo_screenwidth()
screen_height = app.winfo_screenheight()

# Lấy kích thước cửa sổ ứng dụng
app_width = 720
app_height = 480

# Tính toán vị trí cho cửa sổ
x = (screen_width - app_width) // 2
y = (screen_height - app_height) // 2

# Đặt vị trí cửa sổ
app.geometry(f"{app_width}x{app_height}+{x}+{y}")

app.title("YouTube Link Download")

# adding UI elements
title = customtkinter.CTkLabel(app, text="Insert a YouTube Link", width=200, height=50, font=("cursive", 28))
title.pack(padx=10, pady=10)

# link input
url_var = tk.StringVar()
link = customtkinter.CTkEntry(app, width=500, height=50, textvariable=url_var)
link.pack()

# finish downloading
finishLabel = customtkinter.CTkLabel(app, text="")
finishLabel.pack()

# progress percentage
progress = customtkinter.CTkLabel(app, text="0%")
progress.pack()

# progressbar
progressbar = customtkinter.CTkProgressBar(app, width=400)
progressbar.set(0)
progressbar.pack(padx=10, pady=10)

# download high quality video button
download_hq = customtkinter.CTkButton(app, text="Download High Quality-Mp4", command=lambda: startDownLoad("highQuality"))
download_hq.pack(padx=10, pady=10)

# download low quality
download_hq = customtkinter.CTkButton(app, text="Download Low Quality-Mp4", command=lambda: startDownLoad("lowQuality"))
download_hq.pack(padx=10, pady=10)

# download audio
download_audio = customtkinter.CTkButton(app, text="Download Mp3", command=lambda: startDownLoad("audio"))
download_audio.pack(padx=10, pady=10)

# open another python file button
open_file_button = customtkinter.CTkButton(app, text="Play Video Downloaded", command=open_player)
open_file_button.pack(side="bottom", padx=10, pady=10, anchor="sw")

# Check for error status and show error message if needed
def check_error_status():
    global error_status
    if error_status:
        show_error_message()

# run app
app.mainloop()
check_error_status()  # Outside of the main loop to check error status after app closes
