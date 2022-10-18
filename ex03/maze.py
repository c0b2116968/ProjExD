import tkinter as tk
import maze_maker as mm #8

def key_down(event):
    global key
    key = event.keysym

def key_up(event):
    global key
    key = ""

def main_proc():
    global cx, cy, mx, my
    if key == "Up" and ml[my-1][mx] != 1: #修正箇所
        my -= 1
    elif key == "Down" and ml[my+1][mx] != 1:
        my += 1
    elif key == "Left" and ml[my][mx-1] != 1:
        mx -= 1
    elif key == "Right" and ml[my][mx+1] != 1:
        mx += 1
    cx, cy = mx*100+50, my*100+50
    
    if mx == gx and my == gy: #ゴールについたときの処理
        canv.create_text(750,450,text="GOAL!!",font=("",150),fill="green") #文字を表示させる #修正箇所

    elif mx == nx and my == ny: #敵についてしまったときの処理
        canv.create_text(750,450,text="DEAD",font=("",150),fill="red") #文字を表示させる

    canv.coords("tori", cx, cy)
    root.after(100, main_proc)


if __name__ == "__main__":
    root = tk.Tk()
    root.title("迷えるこうかとん") #1

    mx,my = 1,1  #自分の座標
    gx,gy = 13,1 # ゴールの座標
    nx,ny = 13,7 #敵の座標

    canv = tk.Canvas(root,width=1500,height=900,bg="black")
    canv.pack()  #2
 
    ml = mm.make_maze(15, 9) #9
    ms = mm.show_maze(canv, ml) #10

    gool = tk.PhotoImage(file="fig/8.png")  #ゴールの写真表示
    zx,zy = (gx*100)+50, (gy*100)+50
    canv.create_image(zx,zy,image=gool,tag="gool") 

    ene = tk.PhotoImage(file="fig/ene.png")  #敵の写真追加
    px,py = (nx*100)+50, (ny*100)+50
    canv.create_image(px,py,image=ene,tag="ene")

    tori = tk.PhotoImage(file="fig/2.png")
    cx,cy = (mx*100)+50, (my*100)+50 
    canv.create_image(cx, cy, image=tori, tag="tori") #3

    key = "" #4
    root.bind("<KeyPress>",key_down) #5
    root.bind("<KeyRelease>",key_up) #6

    main_proc() #7

    root.mainloop()