from window import window
from panda3d.core import WindowProperties, load_prc_file_data, VirtualFileSystem, Filename
from uuid import uuid4
from tkinter import ttk, filedialog
import tkinter
import subprocess
import webbrowser

window.windowType = 'none'

window.startTk()
window.tkRoot.title("Finale Engine Editor")

menubar = tkinter.Menu(window.tkRoot)
window.tkRoot.config(menu=menubar)

VFS = VirtualFileSystem.get_global_ptr()

current_project: str = None
current_project_vfs: str = None


def new_window(title=""):
    _window = tkinter.Toplevel(window.tkRoot)
    _window.title(title)
    return _window


# Creates a new project and the required folders in the project directory
def new_project():
    # TODO CHECK IF A FILE ALREADY EXISTS, and ask if they want to use base panda3d
    global current_project, current_project_vfs

    project_path = filedialog.askdirectory(title="New Project")
    current_project = project_path

    project_path = Filename.fromOsSpecific(project_path)
    current_project_vfs = project_path

    for folders in ["Textures", "Audio", "Data", "Others", "Models", "Code", "Levels", "Fonts", "Shaders",
                    "Particles", "FinaleEngine"]:
        VFS.make_directory(project_path + "/" + folders)

    VFS.create_file(project_path + "/main.py")

    # Create the defualt main.py file
    VFS.write_file(auto_wrap=True, filename=project_path + "/main.py", data=b"""
from FinaleEngine.window import window

window.run()
""")

    for file in ["__init__", "entities", "entity", "utilities", "window"]:
        python_file = VFS.read_file(file + ".py", auto_unwrap=True)
        VFS.create_file(project_path + f"/FinaleEngine/{file}.py")
        VFS.write_file(auto_wrap=True, filename=project_path + f"/FinaleEngine/{file}.py", data=python_file)


def load_project():
    global current_project, current_project_vfs
    current_project = filedialog.askdirectory(title="Load Project")
    current_project_vfs = Filename.fromOsSpecific(current_project)


def play():
    if current_project:
        try:
            print(current_project, "/main.py 1")
            subprocess.Popen("python " + current_project + "/main.py 1")
        except:
            subprocess.Popen("python " + current_project + "\main.py 1")


def play_from_here():
    ...


def new_level_test():
    ...


def load_level_test():
    ...


def database():
    """Creates the database widget/window which allows the user to create and manage different types of data.
    Such as CSV"""

    global current_project_vfs

    # TODO
    # Add options for different datatypes for now just do python dicts with str and ast.literal_eval
    # each data item should be a folder similar to the levels

    database_window = new_window(title="Database")
    frame1 = tkinter.Frame(master=database_window)
    frame1.grid(column=0, row=0, columnspan=4)

    database_items = tkinter.Listbox(master=frame1)

    scroll_bar = tkinter.Scrollbar(master=frame1, orient=tkinter.VERTICAL, command=database_items.yview)

    database_items.configure(yscrollcommand=scroll_bar.set)

    database_items.grid(column=0, row=0, columnspan=2)

    scroll_bar.grid(column=1, row=0, columnspan=2, sticky=tkinter.NE + tkinter.SE)

    def add_item():
        database_items.insert(tkinter.END, f"New Data {add_item.index}")
        VFS.make_directory(current_project_vfs + f"/Data/New Data {add_item.index}")
        add_item.index += 1

    add_item.index = 0

    database_items_add_button = tkinter.Button(master=frame1, text="+", padx=10, command=add_item)
    database_items_add_button.grid(column=0, row=1, columnspan=2, sticky=tkinter.EW)

    # Loads each folder into the database items
    def get_data(event):
        selection = event.widget.curselection()
        if selection:
            index = selection[0]
            data = event.widget.get(index)

            try:
                with open(data + ".txt", "r") as file:
                    ...
            except:
                pass

    database_items.bind("<<ListboxSelect>>", get_data)

    frame2 = tkinter.Frame(master=window.tkRoot)
    frame2.grid(column=1, row=0, columnspan=3)


# The code editor window which lets users edit python code
def code():

    # Create the code editor window
    code_editor = new_window(title="Code Editor")

    #
    add_code = tkinter.Button(master=code_editor, text="New Script")
    add_code.grid(column=0, row=0, sticky="nsew")

    code_items = tkinter.Listbox(master=code_editor)
    code_items.grid(column=0, row=1, rowspan=2, sticky="nsew")

    code_text = tkinter.Text(master=code_editor)
    code_text.grid(column=1, row=0, columnspan=4, rowspan=2, sticky="nsew")

    # Each widget will now fill the frame/window
    code_editor.grid_columnconfigure(0, weight=1)
    code_editor.grid_columnconfigure(1, weight=1)
    code_editor.grid_rowconfigure(0, weight=1)


def assets():
    ...


def settings():
    ...


def help_():
    ...


# The music player window lets users test their sound effects and music tracks in the editor
# It also lets people listen to the music while they're designing their levels to get into the mood better
def music():
    music_player = new_window("Music Player")
    music_items = tkinter.Listbox(master=music_player)

    scroll_bar = tkinter.Scrollbar(master=music_player, orient=tkinter.VERTICAL, command=music_items.yview)

    music_items.grid(row=0, column=0)
    scroll_bar.grid(column=1, row=0, columnspan=2, sticky=tkinter.NE + tkinter.SE)

    volume_text = tkinter.Label(master=music_player, text="Volume")
    volume_text.grid(column=3, row=0)

    volume_value = tkinter.IntVar()

    volume = ttk.Scale(master=music_player, variable=volume_value, from_=0, to=100, orient=tkinter.HORIZONTAL)
    volume.grid(column=4, row=0)

    panning_text = ttk.Label(master=music_player, text="Panning")
    panning_text.grid(column=3, row=1)


def resize_window(event):
    window_properties = WindowProperties.getDefault()
    window_properties.set_origin((0, 0))
    window_properties.set_size((int(event.width * .8), int(event.height)))
    window.win.requestProperties(window_properties)


window.tkRoot.bind("<Configure>", resize_window)

for x in [["File", ["New", new_project,
                    "Load", load_project,
                    "Save As", lambda: print('NEW'),
                    "Exit", quit]],
          ["Game", ["Play", play,
                    "New Level Test", lambda: print('NEW'),
                    "Load Level Test", lambda: print("New")]],
          ["Tools", ["Database", database,
                     "Code", code,
                     "Assets", lambda: print('NEW'),
                     "Music", music,
                     "Sequence", lambda: print('NEW')]],
          ["Settings", ["Level Settings", lambda: print('NEW'),
                        "Game Settings", lambda: print('NEW')]],
          ["Help", ["Docs", lambda: print('NEW'),
                    "Panda3D Docs", lambda: webbrowser.open("docs.panda3d.org")]]
          ]:
    menu = tkinter.Menu(menubar, tearoff=0)

    try:
        for y in range(0, len(x[1]), 2):
            if x[1][y] != "":
                menu.add_command(label=x[1][y], command=x[1][y + 1])
            else:
                menu.add_command(command=x[1][y + 1])
    except:
        pass

    menubar.add_cascade(
        label=x[0],
        menu=menu,
    )

window_properties = WindowProperties.getDefault()
window_properties.set_parent_window(window.tkRoot.winfo_id())
window_properties.set_origin((0, 0))
window_properties.set_size(1, 1)

window.openDefaultWindow(props=window_properties)

window.run()
