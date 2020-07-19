from os import listdir
from os.path import isfile, join, getctime, exists

import os
import shutil
import datetime
import tkinter as tk

from tkinter import filedialog

class File_Grouper(object):
    def __init__(self, path, dest_path):
        if exists(path) and exists(dest_path):
            self.path = path
            self.dest_path = dest_path
        else:
            raise Exception("Dir not found")
        self.filenames = [f for f in listdir(path) if isfile(join(path, f))]
        self.dates_modified = [getctime(join(path,f)) for f in self.filenames]
        self.filenames, self.dates_modified = zip(*sorted(zip(self.filenames, self.dates_modified), key=lambda x: x[1]))
    
    def group_files(self, threshold):
        groups = {}
        thres = threshold * 60
        current_group = None
        for i in range(len(self.filenames)):
            if not current_group:
                current_group = self.dates_modified[i]
                groups[current_group] = []
            if self.dates_modified[i] - current_group > thres:
                current_group = self.dates_modified[i]
                groups[current_group] = [self.filenames[i]]
            else:
                groups[current_group].append(self.filenames[i])
        self._create_dirs(groups)

    def _create_dirs(self, groups):
        for k, v in groups.items():
            ts = datetime.datetime.fromtimestamp(int(k))
            current_dest = join(self.dest_path, str(ts).replace(':', '-'))
            if not exists(current_dest):
                os.mkdir(current_dest)
            for f in v:
                shutil.copy(join(self.path, f), join(current_dest, f))
        print(f"Directories created at {self.dest_path}")
            
        
window = tk.Tk()
window.path = filedialog.askdirectory()
window.dest_path = filedialog.askdirectory()
grouper = File_Grouper(window.path, window.dest_path)
grouper.group_files(10)
label = tk.Label(text="Τα αρχεία σου οργανώθηκαν!\nΜε αγάπη,\nΆγγελος", height=10, width=30, font=("Courier", 20))
label.pack()
window.mainloop()
        
        
