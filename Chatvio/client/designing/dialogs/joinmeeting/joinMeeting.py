from tkinter import (
    Tk,
    Toplevel,
    Entry,
    Button,
    DISABLED,
    ACTIVE,
    END
) 


class JoinMeeting(object):
    def __init__(self):
        self.master = Tk()
        self.master.title("Enter your meeting ID")
        self.master.configure(bg="#2d2d2d")
        
        self.master.resizable(0, 0)
        self.width, self.height = 500, 300
        self.master.geometry("{0.width}x{0.height}".format(self))
        
        self.state = False
        
    def validate(self, event = None):
        if self.state:
            return
        self.state = True
        code = self.entry.get()
        
        ## Entry
        self.entry.delete(0, END)
        self.entry.insert(0, "Validating...")
        self.entry.configure(fg="#3d3c3c")
        self.entry.configure(state=DISABLED)
        
        ## Top level
        window = Toplevel()
        window.title("Loading...")
        window.configure(bg="#2d2d2d")
        window.geometry("250x80")
        window.resizable(0, 0)
        
        window.mainloop()
        
    def changeButtonSize(self, height=30):
        self.button['height'] = height
        
    def createWidgets(self):
        ## entry
        self.entry = Entry(bg="white", fg="black")
        self.entry.place(x=90, y=50, height=40, width=310)
        self.entry.bind("<Return>", self.validate)
        
        ## button
        self.button = Button(
            bg="#2d2d2d", text="Submit meeting ID", fg="orange", command=self.validate
        )
        self.button.place(x=90, y=150, height=30, width=310)
        self.button.bind('<Enter>', lambda event : self.changeButtonSize(70))
        self.button.bind('<Leave>', lambda event : self.changeButtonSize())

    def stop(self):
        self.master.destroy()
    
    def run(self):
        self.createWidgets()
        self.master.mainloop()
        
    
if __name__ == "__main__":
    obj = JoinMeeting()
    obj.run()