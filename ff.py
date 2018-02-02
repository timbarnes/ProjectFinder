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
        self.createWidgets()
        self.found_widgets = []

    def createWidgets(self):
        """
        Create the elements of the UI and connect to variables.
        """
        self.grid()
        self.search_string = tkinter.StringVar()
        # Frame with prompt, string, and go button
        self.query_frame = ttk.Frame(self, borderwidth=5)
        self.query_frame.grid(row=0, column=0)

        self.prompt = ttk.Label(self.query_frame,
                                text="Search for:", justify='right')
        self.prompt.grid(row=0, column=0)

        self.search_string = ttk.Entry(self.query_frame, width=25,
                                       textvariable=self.search_string)
        self.search_string.bind('<Return>', self.onEnter)
        self.search_string.grid(row=1, column=0)

        self.go = ttk.Button(self.query_frame, text='GO',
                             command=self.go_search)
        self.go.grid(row=2, column=0)

        self.photo_frame = ttk.LabelFrame(self, text='Photo Folders',
                                          borderwidth=5, width=200)
        self.photo_frame.grid(row=1, column=0)

        self.project_frame = ttk.LabelFrame(self, text='Project Folders',
                                            borderwidth=5, width=200)
        self.project_frame.grid(row=2, column=0)

    def onEnter(self, event):
        """
        Hitting enter should be the same as clicking GO.
        """
        self.go_search()

    def launchWindow(self, match):
        """
        Create a window to view the folder matched.
        """
        full_path = os.path.join(PROJECT_BASE, match)
        subprocess.run(["open", full_path])

    @staticmethod
    def findMatches(f_list, search_str):
        """
        Return the list of folders that match the search_str.
        """
        return [x for x in f_list
                if x.upper().count(search_str.upper()) > 0]

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
        self.found_widgets += widget_list  # Save the created widgets

    def destroyWidgets(self):
        """
        Delete any widgets in self.widget_list, because this is a new run.
        """
        for w in self.found_widgets:
            w.destroy()

    def go_search(self):
        """
        Execute the search, and post results as widgets.
        """
        ss = self.search_string.get()
        if len(ss) < 2:
            error("Search string too short")
        else:
            pr_list = self.findMatches(PROJECT_LIST, ss)
            ph_list = self.findMatches(PHOTO_LIST, ss)
            self.destroyWidgets()  # Delete any previous results
            if pr_list:
                self.showResults(self.project_frame, pr_list)
            if ph_list:
                self.showResults(self.photo_frame, pr_list)


app = Application()
app.master.title('Project Finder')
app.mainloop()
