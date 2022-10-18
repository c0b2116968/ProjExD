import tkinter as tk

if __name__ == "__main__":
    root = tk.Tk()
    root.title("迷えるこうかとん") #1

    canv = tk.Canvas(root,width=1500,height=900,bg="black")
    canv.pack()  #2

    tori = tk.PhotoImage(file="fig/0.png")
    cx,cy = 300,400
    canv.create_image(cx, cy, image=tori, tag="tori") #3

    root.mainloop()