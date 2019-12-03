from tkinter import *
from handle_query import *

class Window(Frame):
    def __init__(self, master = None):
        self.DB = data_base()
        Frame.__init__(self, master)
        self.master = master
        self.get_start()

    def get_start(self):
        self.master.title("Search Box")

        self.pack(fill = BOTH, expand =1)

        processButton = Button(self, text ="Search", command = self.process)
        processButton.place(x = 0, y = 0)

        outputLabel = Label(self, text="Result")
        outputLabel.place(x = 0, y = 50)

        self.outputText = Text(self, height = 28, width = 50)
        self.outputText.place(x=0, y=100)

        self.inputText = Entry(self, width=30)
        self.inputText.place(x = 150, y = 0)

    def process(self):
        target = self.inputText.get()
        result = self.DB.ask(target)
        self.outputText.delete('1.0', END)
        self.outputText.update()
        self.outputText.insert(INSERT, "\n".join(result))


root = Tk()
root.geometry("800x1000")
app = Window(root)

root.mainloop()

