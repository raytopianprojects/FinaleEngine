from window import window
from panda3d.core import WindowProperties, load_prc_file_data, VirtualFileSystem, Filename
from uuid import uuid4
from tkinter import ttk, filedialog
import tkinter
import configparser

parser = configparser.ConfigParser()

window.windowType = 'none'

window.startTk()
window.tkRoot.title("Finale Engine Editor")

menubar = tkinter.Menu(window.tkRoot)
window.tkRoot.config(menu=menubar)

VFS = VirtualFileSystem.get_global_ptr()


def new_window(title=""):
    _window = tkinter.Toplevel(window.tkRoot)
    _window.title(title)
    return _window


# Creates a new project and the required folders in the project directory
def new_project():
    # TODO CHECK IF A FILE ALREADY EXISTS, and ask if they want to use base panda3d
    project_path = filedialog.askdirectory(title="New Project")
    project_path = Filename.fromOsSpecific(project_path)

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
    project_path = filedialog.askopenfile(title="Load Project")

    print(project_path.read())


def play():
    ...


def play_from_start():
    ...


def new_level_test():
    ...


def load_level_test():
    ...


def database():
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
        add_item.index += 1

    add_item.index = 0

    database_items_add_button = tkinter.Button(master=frame1, text="+", padx=10, command=add_item)
    database_items_add_button.grid(column=0, row=1, columnspan=2, sticky=tkinter.EW)

    def get_data(event):
        selection = event.widget.curselection()
        if selection:
            index = selection[0]
            data = event.widget.get(index)

            try:
                with open(data + ".txt", "r") as file:
                    parser.read(file)
                    print(parser)
            except:
                pass

    database_items.bind("<<ListboxSelect>>", get_data)

    frame2 = tkinter.Frame(master=window.tkRoot)
    frame2.grid(column=1, row=0, columnspan=3)


def code():
    ...


def assets():
    ...


def settings():
    ...


def help_():
    ...


def resize_window(event):
    window_properties = WindowProperties.getDefault()
    window_properties.set_origin((0, 0))
    window_properties.set_size((int(event.width * .8), int(event.height)))
    window.win.requestProperties(window_properties)


window.tkRoot.bind("<Configure>", resize_window)

for x in [["File", ["New", new_project,
                    "Load", load_project,
                    "Save", lambda: print('NEW'),
                    "Exit", lambda: print('NEW'),
                    "Quit Finale Engine", lambda: print('NEW')]],
          ["Game", ["Play", lambda: print('NEW'),
                    "Play from Start", lambda: print('NEW'),
                    "New Level Test", lambda: print('NEW'),
                    "Load Level Test", lambda: print("New")]],
          ["Tools", ["Database", database,
                     "Code", lambda: print('NEW'),
                     "Assets", lambda: print('NEW'),
                     "Music", lambda: print('NEW'),
                     "Sequence", lambda: print('NEW')]],
          ["Settings", ["Level Settings", lambda: print('NEW'),
                        "Game Settings", lambda: print('NEW')]],
          ["Help", ["Docs", lambda: print('NEW'),
                    "Panda3D Docs", lambda: print('NEW')]]
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
