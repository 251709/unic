from tkinter import Canvas, Tk

root = Tk()
root.geometry("600x600")

canvas = Canvas(root, width=600, height=600, bg="white")
canvas.pack()

root.mainloop()