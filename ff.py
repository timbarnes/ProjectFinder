import os
import subprocess
import shlex
import tkinter
from tkinter import ttk

PROJECT_BASE = './Test/'
PHOTO_BASE = './Test/'

PROJECT_LIST = os.listdir(PROJECT_BASE)
PHOTO_LIST = os.listdir(PHOTO_BASE)


def popup(message):
    """
    Simple popup message box.
    """
    w = tkinter.Toplevel()
    m = tkinter.Message(w, text=message, width=400)
    m.grid(row=0, column=0, pady=20)
    e = ttk.Button(w, text="OK", command=w.destroy)
    e.grid(row=1, column=0, pady=20)


def error(message):
    """
    Print an error to a pop-up.
    """
    popup("Error: {}".format(message))


class Application(ttk.Frame):
    """
    Build the application window and initialize a project
    """
    # Initialize an empty project

    def __init__(self, master=None):
        # Create the main frame
        ttk.Frame.__init__(self, master)
        # Create the communicating variables
        self.search_string = tkinter.StringVar()
        self.grid()
        self.createWidgets()

    def createWidgets(self):
        """
        Create the elements of the UI and connect to variables.
        """
        # Frame with prompt, string, and go button
        self.query_frame = ttk.Frame(self, borderwidth=2)
        self.query_frame.grid(row=0, column=0)

        self.prompt = ttk.Label(self.query_frame,
                                text="Search for:", justify='right')
        self.prompt.grid(row=0, column=0)

        self.search_string = ttk.Entry(self.query_frame,
                                       textvariable=self.search_string)
        self.search_string.grid(row=1, column=0)

        self.go = ttk.Button(self.query_frame, text='GO',
                             command=self.go_search)
        self.go.grid(row=2, column=0)

        self.photo_frame = ttk.LabelFrame(self, text='Photo Folders',
                                          borderwidth=2, width=200)
        self.photo_frame.grid(row=1, column=0)

        self.project_frame = ttk.LabelFrame(self, text='Project Folders',
                                            borderwidth=2, width=200)
        self.project_frame.grid(row=0, column=1)

    def launchWindow(self, match):
        """
        Create a window to view the folder matched.
        """
        full_path = shlex.quote(os.path.join(PROJECT_BASE, match))
        print(os.getcwd())
        print("Launching folder <{}>".format(full_path))
        subprocess.call('open {}'.format(full_path))

    @staticmethod
    def findMatches(f_list, search_str):
        """
        Return the list of folders that match the search_str.
        """
        if len(search_str) > 1:
            return [x for x in f_list if x.upper().count(search_str.upper()) > 0]
        else:
            error("Search needs at least two characters.")

    def showResults(self, frame, matches):
        """
        Generate buttons in _frame_ for _matches_.
        """
        print(len(matches))
        widget_list = []
        i = 0
        for match in matches:
            widget_list.append(ttk.Button(
                frame, text=match, width=25,
                command=lambda: self.launchWindow(match)))
            widget_list[-1].grid(row=i, column=0)
            i += 1

    def go_search(self):
        """
        Execute the search, and post results as widgets.
        """
        pr_list = self.findMatches(PROJECT_LIST, self.search_string.get())
        ph_list = self.findMatches(PHOTO_LIST, self.search_string.get())
        if pr_list:
            self.showResults(self.project_frame, pr_list)
        if ph_list:
            self.showResults(self.photo_frame, pr_list)


app = Application()
app.master.title('Project Create and Update')
app.mainloop()
