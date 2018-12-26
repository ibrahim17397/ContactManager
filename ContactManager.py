from cm_db import database
from cm_gui import Gui
from tkinter import Tk


def main():
    db = database()
    root=Tk()
    application = Gui(root,db)
    root.mainloop()



if __name__ == "__main__":
    main()
