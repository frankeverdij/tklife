import tkinter as tk

"""
  0 and 1 for Life's normal states, 2 and 3 for cells which disregard rules,
  4 and 5 for unknown cells without and with labels.
"""
fgfield = [ 'white', 'black', 'white', 'black', 'black', 'black' ]
bgfield = [ 'black', 'white', 'black', 'white', 'grey', 'lightgrey' ]
cell2val = {"0": 0 , "1": 1, "0'": 2, "1'": 3, "*": 4, " ": 5}
fieldvalue = [ key for (key, val) in cell2val.items() ]
cell2field = { "0": '   ', "1": '   ', "0'": ' # ', "1'": ' # ', "*": '   ' }

class Board(tk.Frame):
    def __init__(self, master):
        super(Board, self).__init__(master)

    def create(self):
        row = self.master.row.get()
        column = self.master.column.get()
        if (row == 0) or (column == 0):
            raise "Board.new called with zero dimension(s)"
        self.generation = self.master.generation.get()
        self.field = [ [tk.StringVar(self,'   ') for _ in range(column) ] for _ in range(row) ]
        self.labels = [ [] for _ in range(row) ]
        self.i_saved = -1
        self.j_saved = -1

        self.focus_set()
        self.bind('<Key>', lambda e: self.on_keyhandler(e))

        for i,row_ in enumerate(self.field):
            for j,column_ in enumerate(row_):
                L = self.tile(i, j)
                self.labels[i].append(L)

    def tile(self, i, j):
        L = tk.Label(self, textvariable=self.field[i][j], relief=tk.RAISED, fg=fgfield[4], bg=bgfield[4], width=3, height=1)
        L.grid(row=i, column=j, ipadx=4, ipady=5)
        L.bind('<Button-1>',lambda e,i=i,j=j: self.on_leftclick(i, j, e))
        L.bind('<Button-2>',lambda e,i=i,j=j: self.on_middleclick(i, j, e))
        L.bind('<Button-3>',lambda e,i=i,j=j: self.on_rightclick(i, j, e))
        return L

    def get_value(self, label):
        return cell2val.get(label, 5)

    def get_field(self, field):
        return cell2field.get(field, field)

    def refresh(self):
        self.generation = self.master.generation.get()
        for label in self.grid_slaves():
            r = int(label.grid_info()["row"])
            c = int(label.grid_info()["column"])
            fstate = self.master.spread.sheet[self.generation][r][c].get()
            val = self.get_value(fstate)
            self.field[r][c].set(self.get_field(fstate))
            label.config(bg=bgfield[val], fg=fgfield[val], relief=tk.RAISED)
        self.i_saved = -1

    def resize(self):
        newcolumn = self.master.column.get()
        difcolumn = newcolumn - len(self.field[0])
        if (difcolumn < 0):
            self.labels[:][newcolumn: newcolumn - difcolumn].destroy()
        else:
            for i in range(len(self.field)):
                for j in range(newcolumn - difcolumn, newcolumn):
                    self.field[i].append(tk.StringVar(self,'   '))
                    L = self.tile(i, j)
                    self.labels[i].append(L)


    def on_leftclick(self, i, j, event):
        val = self.get_value(self.master.spread.sheet[self.generation][i][j].get())
        if (val < 5):
            if val == 4:
                val = 0
            else: 
                val += 1
                val = val % 4
        else:
            return

        self.field[i][j].set(' # ' if (val == 2 or val == 3) else '   ')
        event.widget.config(bg=bgfield[val], fg=fgfield[val])
        self.master.spread.sheet[self.generation][i][j].set(fieldvalue[val])

    def widget_raise(self):
        for label in self.grid_slaves():
            label.config(relief=tk.RAISED)

    def on_middleclick(self, i, j, event):
        self.labels[self.i_saved][self.j_saved].config(relief=tk.RAISED)
        event.widget.config(bg=bgfield[5], fg=fgfield[5])
        val = self.get_value(self.master.spread.sheet[self.generation][i][j].get())
        if (val < 5):
            self.field[i][j].set('   ')
            self.master.spread.sheet[self.generation][i][j].set('   ')
            self.i_saved = i
            self.j_saved = j
            event.widget.config(relief=tk.RIDGE)
        else:
            if (self.i_saved < 0):
                self.i_saved = i
                self.j_saved = j
                event.widget.config(relief=tk.RIDGE)
            else:
                self.i_saved = -1

    def on_rightclick(self, i, j, event):
        val = self.get_value(self.master.spread.sheet[self.generation][i][j].get())
        if (val == 4):
            self.on_middleclick(i, j, event)
            return

        val = 4
        self.master.spread.sheet[self.generation][i][j].set(fieldvalue[val])
        self.field[i][j].set('   ')
        event.widget.config(bg=bgfield[val], fg=fgfield[val], relief=tk.RAISED)

    def on_keyhandler(self, event):
        if (self.i_saved < 0):
            return

        i = self.i_saved
        j = self.j_saved
        var = self.master.spread.sheet[self.generation][i][j].get()
        val = self.get_value(var)
        if (val == 5):
            if (event.keysym == 'Escape'):
                self.labels[self.i_saved][self.j_saved].config(relief=tk.RAISED)
                self.i_saved = -1
                return

            if (event.char == '-'):
                if (var[0] == '-'):
                    var = ' ' + var[1:]
                else:
                    if not var.isspace():
                        var = event.char + var[1:]
                    else:
                        return

            if event.char.isalpha():
                if (var[1] == ' '):
                    var = var[0] + event.char + ' '
                else:
                    if (var[2] == ' '):
                        var = var[0:2] + event.char
                    else:
                        var = var[0] + event.char + ' '
            self.master.spread.sheet[self.generation][i][j].set(var)
            self.field[i][j].set(var)

