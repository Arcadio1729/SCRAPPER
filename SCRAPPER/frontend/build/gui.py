
# This file was generated by the Tkinter Designer by Parth Jadhav
# https://github.com/ParthJadhav/Tkinter-Designer


from pathlib import Path

# from tkinter import *
# Explicit imports to satisfy Flake8
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage


OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"C:\ja\moje\SCRAPPER\frontend\build\assets\frame0")


def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)


window = Tk()

window.geometry("1920x960")
window.configure(bg = "#FFFFFF")


canvas = Canvas(
    window,
    bg = "#FFFFFF",
    height = 960,
    width = 1920,
    bd = 0,
    highlightthickness = 0,
    relief = "ridge"
)

canvas.place(x = 0, y = 0)
canvas.create_rectangle(
    846.0,
    28.0,
    1920.0,
    932.0,
    fill="#FFFFFF",
    outline="")

canvas.create_text(
    232.0,
    130.0,
    anchor="nw",
    text="GUI Kit 1.0 ",
    fill="#F38504",
    font=("AppleSDGothicNeo ExtraBold", 83 * -1)
)

canvas.create_text(
    232.0,
    290.0,
    anchor="nw",
    text="for GUI-based Python code generator\nOpen Source Software",
    fill="#F38504",
    font=("AppleSDGothicNeo Medium", 35 * -1)
)

canvas.create_rectangle(
    232.0,
    762.0,
    620.0,
    830.0,
    fill="#000000",
    outline="")
window.resizable(False, False)
window.mainloop()
