import os
import sys
import platform
import subprocess
import wx


class DirFrame(wx.Frame):
    """
    Find project and photo folders matching a pattern.
    Return clickable buttons that open the folder.
    """

    def __init__(self, *args, **kwargs):
        wx.Frame.__init__(self, None, wx.ID_ANY, 'Find Folders',
                          size=(300, 400))
        self.buildGUI()

    def buildGUI(self):
        # Add a panel so it looks correct on all platforms
        self.panel = wx.Panel(self, wx.ID_ANY)
        # Status bar for messages
        self.sb = self.CreateStatusBar()
        self.sb.SetStatusText("Enter search term and hit Enter...")
        # Create the sizers
        self.mainBox = wx.BoxSizer(wx.VERTICAL)       # Everything
        self.promptBox = wx.BoxSizer(wx.HORIZONTAL)   # Prompt for search
        self.resultBox = wx.StaticBoxSizer(wx.VERTICAL,
                                           self.panel, label="Results")
        # Add the inner sizers to the mainBox
        self.mainBox.Add(self.promptBox, 0, wx.EXPAND, 0)
        self.mainBox.Add(self.resultBox, 2, wx.EXPAND, 0)
        # Create and attach search box and prompt to promptBox
        sLabel = wx.StaticText(self.panel, label="Search:")
        self.sString = wx.TextCtrl(self.panel)
        hl = wx.StaticLine(self.panel, style=wx.LI_HORIZONTAL)
        self.promptBox.Add(sLabel, flag=wx.ALL, border=8)
        self.promptBox.Add(self.sString, 1, wx.EXPAND | wx.ALL, 8)
        self.promptBox.Add(hl, 0, wx.ALL, 8)
        # Project folders
        fLabel = wx.StaticText(self.panel, label="Project Folders")
        self.projectFiles = wx.ListBox(self.panel, style=wx.EXPAND)
        self.resultBox.Add(fLabel, 0, wx.ALL, 8)
        self.resultBox.Add(self.projectFiles, 3, wx.EXPAND | wx.ALL, 8)
        # # Photo folders
        pLabel = wx.StaticText(self.panel, label="Photo Folders")
        self.photoFiles = wx.ListBox(self.panel)
        self.resultBox.Add(pLabel, 0, wx.ALL, 8)
        self.resultBox.Add(self.photoFiles, 2, wx.EXPAND | wx.ALL, 8)

        self.panel.SetSizer(self.mainBox)
        self.panel.Fit()

        self.sString.Bind(wx.EVT_KEY_DOWN, self.onKeyPress)
        self.projectFiles.Bind(wx.EVT_LISTBOX, self.launchProject)
        self.photoFiles.Bind(wx.EVT_LISTBOX, self.launchPhotos)

    def onKeyPress(self, event):
        """
        Looks for Enter / Return key in search box.
        """
        keycode = event.GetKeyCode()
        if keycode == wx.WXK_RETURN:
            self.doSearch()
        else:
            event.Skip()

    @staticmethod
    def launchFolder(base, match):
        """
        OS-sensitive folder window launcher.
        """
        full_path = os.path.join(base, match)
        system = platform.system()
        if system == 'Windows':
            subprocess.Popen(['explorer', full_path])
        elif system == 'Darwin':
            subprocess.Popen(['open', full_path])

    def launchProject(self, event):
        """
        Create a list of Project folders.
        """
        match = event.GetEventObject().GetStringSelection()
        self.sb.SetStatusText("Launching {}.".format(match))
        self.launchFolder(PROJECT_BASE, match)

    def launchPhotos(self, event):
        """
        Create a list of photo folders.
        """
        match = event.GetEventObject().GetStringSelection()
        self.sb.SetStatusText("Launching: {}".format(match))
        self.launchFolder(PHOTO_BASE, match)

    @staticmethod
    def findMatches(f_list, search_str):
        """
        Return the list of folders that match the search_str.
        """
        return [x for x in f_list
                if x.upper().count(search_str.upper()) > 0]

    def doSearch(self):
        """
        Execute the search, and post results as widgets.
        """
        ss = self.sString.GetValue()
        if len(ss) < 2:
            self.sb.SetStatusText("Search string too short")
        else:
            self.projectFiles.Clear()
            self.photoFiles.Clear()
            pr_list = self.findMatches(PROJECT_LIST, ss)
            ph_list = self.findMatches(PHOTO_LIST, ss)
            if pr_list:
                self.projectFiles.InsertItems(pr_list, 0)
            # self.projectFiles.SetSize(self.projectFiles.BestSize)
            if ph_list:
                self.photoFiles.InsertItems(ph_list, 0)
            if pr_list or ph_list:
                self.sb.SetStatusText("Click on a folder to open.")
            else:
                self.sb.SetStatusText("No matches found.")


def main():
    global PROJECT_BASE
    global PHOTO_BASE
    global PROJECT_LIST
    global PHOTO_LIST
    try:
        PROJECT_BASE = sys.argv[1]
        PHOTO_BASE = sys.argv[2]
        PROJECT_LIST = os.listdir(PROJECT_BASE)
        PHOTO_LIST = os.listdir(PHOTO_BASE)
    except IndexError:
        print("Usage: python pf.py <folder1> <folder2>")
        # Create and run the application object
    app = wx.App()
    frame = DirFrame().Show()
    app.MainLoop()


# Run the program
if __name__ == '__main__':
    main()
