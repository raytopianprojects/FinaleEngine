from window import window
from panda3d.core import WindowProperties, load_prc_file_data, VirtualFileSystem, Filename
from uuid import uuid4
from tkinter import ttk, filedialog
import tkinter
import subprocess
import webbrowser
from idlelib.percolator import Percolator
from idlelib.colorizer import ColorDelegator
import pathlib

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
    if current_project_vfs:
        # Create the code editor window
        code_editor = new_window(title="Code Editor")

        side_frame = ttk.Frame(master=code_editor)
        side_frame.grid(column=0, row=0, sticky="nsew", rowspan=2)

        # The list of python files that can be editied
        code_items = tkinter.Listbox(master=side_frame)
        code_items.grid(column=0, row=1, columnspan=2, sticky="nsew")

        for item in VFS.scan_directory(current_project_vfs + "/Code"):
            # Convert item into a str because currently its a panda3d filepath object
            item = str(item)

            # we only want the file name not the path so break the filepath up into a list and get the last index
            item = item.split("/")
            item = item[-1]
            code_items.insert(tkinter.END, item)

        # By setting the row and column configure for the code items grid entry we make sure that it fills the grid
        side_frame.rowconfigure(1, weight=1)
        side_frame.columnconfigure(0, weight=1)

        # Create an entry widget so users can name the script
        code_file_name = ttk.Entry(master=side_frame)
        code_file_name.grid(column=1, row=0)

        # TODO Check if file name already exists and if it does append 1
        def add_item():
            if code_file_name.get() == "":
                VFS.create_file(current_project_vfs + f"/Code/new_file_{add_item.index}.py")
                code_items.insert(tkinter.END, f"new_file_{add_item.index}")
            else:
                if pathlib.Path(code_file_name.get()).suffix:
                    VFS.create_file(current_project_vfs + f"/Code/{code_file_name.get()}")
                    code_items.insert(tkinter.END, code_file_name.get())
                else:
                    VFS.create_file(current_project_vfs + f"/Code/{code_file_name.get()}.py")
                    code_items.insert(tkinter.END, code_file_name.get() + ".py")

            # Increment add_item's index, so we don't overwrite any files
            add_item.index += 1

        add_item.index = 0

        # Create a button that adds new script
        add_code = ttk.Button(master=side_frame, text="New Script", command=add_item)
        add_code.grid(column=0, row=0, sticky="n")

        # The text editor itself
        code_textbox = tkinter.Text(master=code_editor)

        # This uses python's built in idle syntax highlighting so we don't have to write our own
        Percolator(code_textbox).insertfilter(ColorDelegator())

        code_textbox.grid(column=1, row=0, rowspan=2, sticky="nsew")

        # Each widget will now fill the frame/window
        code_editor.grid_columnconfigure(0, weight=1)
        code_editor.grid_columnconfigure(1, weight=1)
        code_editor.grid_rowconfigure(0, weight=1)

        # We use this function as a callback when someone selects one of the entires in the code_items listbox
        # When they due we open that file and insert it into the code editor
        def open_code_file(event):
            # Get the selected listbox item
            code_selection = event.widget.curselection()

            # Check if we even have a selection
            if code_selection:
                # Get the filename
                file_to_open = event.widget.get(code_selection[0])

                # Store the filename so we can save to the proper file in auto_save_code
                open_code_file.code_item_selection = file_to_open

                # Open the file
                file = VFS.read_file(current_project_vfs + "/Code/" + file_to_open, auto_unwrap=True)

                # Clear the textbox so tkinter doesn't append the text onto the last text
                code_textbox.delete("1.0", tkinter.END)

                # Insert the text from the file into the textbox
                code_textbox.insert("1.0", file)

        # Code item selection lets us track the name of the selected file so we can auto save to it
        # when the text inside is edited
        open_code_file.code_item_selection = None

        # Open the appropriate file when an item is selected
        code_items.bind("<<ListboxSelect>>", open_code_file)

        # We need to save the coded file to disk automatically whenever the user types
        def auto_save_code(event):
            if open_code_file.code_item_selection:
                VFS.write_file(current_project_vfs + "/Code/" + open_code_file.code_item_selection,
                               auto_wrap=True,
                               data=bytes(event.widget.get("1.0", tkinter.END), encoding='utf8'))

        # Auto save when coding in the code_textbox
        code_textbox.bind("<KeyRelease>", auto_save_code)


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
                     "Code Editor", code,
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
