import os
import tkinter as tk
from tkinter import filedialog as fd

from tkinter.messagebox import showinfo

class MenuBar(tk.Menu):
    def __init__(self, master = None):
        super(MenuBar, self).__init__(master)
        self.option_add('*tearOff', False)

        filemenu = FileMenu(self)
        self.add_cascade(label="File", menu = filemenu)
        
        editmenu = EditMenu(self)
        self.add_cascade(label="Edit", menu = editmenu)
        
        helpmenu = HelpMenu(self)
        self.add_cascade(label="Help", menu = helpmenu)
        
    def donothing(self):
        filewin = tk.Toplevel(self.master)
        button = tk.Button(filewin, text="Do nothing button")
        button.pack()

    def load_file(self, filename):
        self.master.load_file(filename)

    def save_file(self, withdialog = False):
        filename = self.master.filename.get()
        if (withdialog or (len(filename) == 0)):
            filetypes = ( ('text files', '*.txt'), ('All files', '*.*') )
            initialfile = ('Untitled' if len(filename) == 0 else filename)
            filename = fd.asksaveasfilename(
                title = 'Save a file',
                initialfile = initialfile,
                initialdir = os.curdir,
                defaultextension = ".txt",
                filetypes = filetypes)
        self.master.save_file(filename)

    def set_dimensions(self, newbool):
        self.dimwin = tk.Toplevel(self.master)
        self.dimwin.title('Dimensions')
        parambox = tk.Frame(self.dimwin)
        parambox.pack()

        labelcolumn = tk.Label(parambox, text="Column:")
        labelrow = tk.Label(parambox, text="Row:")
        labelperiod = tk.Label(parambox, text="Period:")
        spincolumn = tk.Spinbox(parambox, textvariable=self.master.column, from_=1, to=64)
        spinrow = tk.Spinbox(parambox, textvariable=self.master.row, from_=1, to=64)
        spinperiod = tk.Spinbox(parambox, textvariable=self.master.period, from_=1, to=16)

        button = tk.Button(parambox, text='Ok', command = lambda : self.dimensions_destroy(newbool))

        labelcolumn.grid(row=0, column=0)
        labelrow.grid(row=1, column=0)
        labelperiod.grid(row=2, column=0)
        spincolumn.grid(row=0, column=1)
        spinrow.grid(row=1, column=1)
        spinperiod.grid(row=2, column=1)

        button.grid(row=3, column=0, columnspan=2)

    def dimensions_destroy(self, newbool):
        self.dimwin.destroy()
        if (newbool or self.master.isnew):
            self.master.create()
        else:
            self.master.update_dimensions()

    def close(self):
        self.master.destroy()

    def get_filename(self):
        return self.master.filename.get()

    def quit(self):
        self.master.quit()

class FileMenu(tk.Menu):
    def __init__(self, master):
        super(FileMenu, self).__init__(master)
        
        self.add_command(label="New", command = lambda : master.set_dimensions(True))
        self.add_command(label="Open", command = self.open_file)
        self.add_command(label="Save", command = lambda : master.save_file(False))
        self.add_command(label="Save as...", command = lambda : master.save_file(True))
        self.add_command(label="Close", command = master.close)
        self.add_separator()
        self.add_command(label="Exit", command = master.quit)

    def open_file(self):
        filetypes = ( ('text files', '*.txt'), ('All files', '*.*') )

        filename = fd.askopenfilename(
            title = 'Open a file',
            initialdir = os.curdir,
            filetypes = filetypes)
        if (filename):
            self.master.load_file(filename)

    def save_file_as(self):
        filetypes = ( ('text files', '*.txt'), ('All files', '*.*') )

        filename = fd.asksaveasfilename(
            title = 'Save a file',
            initialfile = self.master.get_filename(),
            initialdir = os.curdir,
            defaultextension = ".txt",
            filetypes = filetypes)
        self.master.save_file(filename)

    def save_file(self):
        self.master.save_file()

class EditMenu(tk.Menu):
    def __init__(self, master):
        super(EditMenu, self).__init__(master)
        
        self.add_command(label="Undo", command = master.donothing)
        self.add_command(label="Redo", command = master.donothing)
        self.add_separator()
        self.add_command(label="Cut", command = master.donothing)
        self.add_command(label="Copy", command = master.donothing)
        self.add_command(label="Paste", command = master.donothing)
        self.add_command(label="Delete", command = master.donothing)
        self.add_command(label="Select All", command = master.donothing)
        self.add_separator()
        self.add_command(label="Set Dimensions", command = lambda : master.set_dimensions(False))

class HelpMenu(tk.Menu):
    def __init__(self, master):
        super(HelpMenu, self).__init__(master, name='help')
        
        self.add_command(label="Help Index", command = master.donothing)
        self.add_command(label="About...", command = self.about)

    def about(self):
        win=tk.Toplevel(self.master)
        win.title('about')
        box = tk.Frame(win)
        box.pack()
        label = tk.Label(box, text='LLSpread\n\nFrank Everdij (2022)', padx=10, pady=10)
        label.pack()
        button = tk.Button(box, text='Ok', command = win.destroy)
        button.pack(side='bottom')

