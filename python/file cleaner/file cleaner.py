import os
import shutil
from tkinter import Tk, filedialog, Button, Label, Listbox, END

FILE_ORGANISATION = [
    (['.exe', '.bat', '.iso'],
     'application',
     ['installer', 'setup', 'launch', 'program', 'tool', 'app', 'application', 'patch']),

    (['.png', '.jpg', '.jpeg', '.bmp', '.gif', '.mp4', '.mpg', '.mp3', '.wav'],
     'media',
     ['image', 'photo', 'screenshot', 'video', 'movie', 'song', 'music', 'recording', 'clip', 'picture', 'media']),

    (['.pdf', '.rtf', '.txt', '.docx', 'accdb', '.doc', '.xls', '.xlsx', '.ppt', '.pptx', '.csv', '.zip', '.rar', '.7z'],
     'workspace',
     ['report', 'invoice', 'document', 'slide', 'spreadsheet', 'assignment', 'notes', 'presentation', 'summary', 'project', 'work', 'school', 'compressed']),

    (['.py', '.js', '.jar'],
     'code',
     ['script', 'code', 'project', 'function', 'module', 'automation', 'backend', 'dev', 'api', 'bot']),

    (['.html', '.css', '.php', '.xml'],
     'web',
     ['web', 'site', 'template', 'page', 'style', 'markup', 'frontend', 'design', 'layout', 'html'])
]

class FileCleanerUI:
    def __init__(self, master):
        self.master = master
        master.title("File Cleaner")

        self.selected_folder = None

        self.label = Label(master, text="No folder selected")
        self.label.pack(pady=5)

        self.select_button = Button(master, text="Select Folder", command=self.select_folder)
        self.select_button.pack(pady=5)

        self.run_button = Button(master, text="Run Program", command=self.run_program, state="disabled")
        self.run_button.pack(pady=5)

        self.listbox = Listbox(master, width=60)
        self.listbox.pack(pady=10)

    def select_folder(self):
        folder_path = filedialog.askdirectory(title="Select Folder")

        if folder_path:
            self.selected_folder = folder_path
            self.label.config(text=f"Selected: {folder_path}")
            self.run_button.config(state="normal")
        else:
            self.label.config(text="No folder selected")
            self.run_button.config(state="disabled")

    def run_program(self):
        self.listbox.delete(0, END)

        if self.selected_folder:
            moved_files = organize_file(dir=self.selected_folder, ui_listbox=self.listbox)

            if not moved_files:
                self.listbox.insert(END, "No files moved.")

def organize_file(org=FILE_ORGANISATION, dir=None, ui_listbox=None):
    if dir is None:
        return
    
    moved_files = []
    for file in os.listdir(dir):
        file_path = os.path.join(dir, file)

        if not os.path.isfile(file_path):
            continue  # Skip directories
        
        name, extension = os.path.splitext(file)
        extension = extension.lower()
        for extensions, foldername, keys in org:
            if extension in extensions or any(key in name.lower() for key in keys):
                target_folder = os.path.join(dir, foldername)

                if not os.path.exists(target_folder):
                    os.makedirs(target_folder)

                target_path = os.path.join(target_folder, file)
                shutil.move(file_path, target_path)
                moved_files.append(f"Moved: {file} → {foldername}")

                if ui_listbox is not None:
                    ui_listbox.insert(END, f"Moved: {file} → {foldername}")
                    
                break
    return moved_files

if __name__ == "__main__":
    root = Tk()
    app = FileCleanerUI(root)
    root.mainloop()