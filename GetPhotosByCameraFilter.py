import os
import shutil
import exifread
import tkinter as tk
import tkinter.filedialog

def filter_photos():
    status_label.config(text="Обработка...")
    result_label.config(text="")
    root.update_idletasks()
    source_dir = source_entry.get()
    dest_dir = dest_entry.get()
    camera_make = make_entry.get()

    total_files = 0
    photo_files = 0
    video_files = 0

    processed_files = 0

    for filename in os.listdir(source_dir):
        filepath = os.path.abspath(os.path.join(source_dir, filename))

        if os.path.isfile(filepath):
            total_files += 1

        if not os.path.isfile(filepath) or not filename.lower().endswith(('.jpg', '.jpeg', '.png', '.gif')):
            if filename.lower().endswith(('.avi', '.mp4', '.mov', '.wmv', '.flv', '.mkv', '.avchd', '.mpeg', '.mpg', '.mpeg2', '.mpeg1', '.vob', '.3gp', '.webm')):
                shutil.copy(filepath, dest_dir)
                processed_files += 1
                video_files += 1
            continue

        try:
            with open(filepath, 'rb') as f:
                tags = exifread.process_file(f)
                make = tags.get('Image Make')

                if str(make) == camera_make:
                    shutil.copy(filepath, dest_dir)
                    processed_files += 1
                    photo_files += 1

        except Exception as e:
            print(f"Ошибка при чтении метаданных файла {filepath}: {e}")

    status_label.config(text="Готово")
    result_label.config(text=f"Обработано {processed_files} из {total_files} файлов\nИзображений: {photo_files}\nВидео: {video_files}")


root = tk.Tk()
root.title("GetPhotosByCameraFilter")

frame = tk.Frame(root)
frame.pack(padx=10, pady=10)

source_label = tk.Label(frame, text="Исходная папка:")
source_label.grid(row=0, column=0)
source_entry = tk.Entry(frame, width=50)
source_entry.grid(row=0, column=1)
source_button = tk.Button(frame, text="Обзор...", command=lambda: source_entry.delete(0, tk.END) or source_entry.insert(0, tkinter.filedialog.askdirectory()))
source_button.grid(row=0, column=2)

dest_label = tk.Label(frame, text="Папка назначения:")
dest_label.grid(row=1, column=0)
dest_entry = tk.Entry(frame, width=50)
dest_entry.grid(row=1, column=1)
dest_button = tk.Button(frame, text="Обзор...", command=lambda: dest_entry.delete(0, tk.END) or dest_entry.insert(0, tkinter.filedialog.askdirectory()))
dest_button.grid(row=1, column=2)

make_label = tk.Label(frame, text="Производитель камеры:")
make_label.grid(row=2, column=0)
make_entry = tk.Entry(frame, width=50)
make_entry.grid(row=2, column=1)

start_button = tk.Button(frame, text="Старт", command=filter_photos)
start_button.grid(row=3, column=0, columnspan=3, pady=(10, 0))

status_label = tk.Label(frame, text="")
status_label.grid(row=4, column=0, columnspan=3, pady=(10, 0))

result_label = tk.Label(frame, text="")
result_label.grid(row=5, column=0, columnspan=3, pady=(10, 0))

root.mainloop()
