import tkinter as tk
import tkinter.messagebox as tkm

def click_number(event):   #数字の入力関数
    btn = event.widget
    num = btn["text"]
    #tkm.showinfo(f"{num}", f"{num}のボタンが押されました")
    entry.insert(tk.END, num)

def click_equal(event):   #イコールの関数
    eqn = entry.get()
    res = eval(eqn)
    entry.delete(0,tk.END)
    entry.insert(tk.END, res)

def click_del(event):      #ACの関数
    den = entry.delete(0,tk.END)

def click_reverse(event):    #符号の反転関数
    ren = entry.get()
    riv = int(ren) * -1
    entry.delete(0,tk.END)
    entry.insert(tk.END, riv)

def click_back(event):    #C --一文字消す処理の関数
    br = entry.get()
    k = br[0:-1]
    entry.delete(0,tk.END)
    entry.insert(tk.END,k)

root = tk.Tk()
root.geometry("300x500")     #画面の大きさ

entry = tk.Entry(root, width=10, font=(", 40"),justify="right",bg="black",fg="white")  #数字の入力欄の設定
entry.grid(row=0, column=0, columnspan=3)

r, c = 1, 0
numbers = list(range(9, -1, -1))
operators = ["+"]                            #1~9,+のボタンを作る,押された場合、処理
for i, num in enumerate(numbers+operators, 1):
    btn = tk.Button(root, text=f"{num}", font=("", 30), width=4, height=1)
    btn.bind("<1>",click_number)
    btn.grid(row=r, column=c)
    c += 1
    if i%3 == 0:
        r += 1
        c = 0

btn = tk.Button(root,text=f"=", font=("", 30), width=4, height=1) #=のボタンについて
btn.bind("<1>",click_equal)
btn.grid(row=r, column=c)

btn = tk.Button(root,text="AC", font=("",30), width=4, height=1,bg="red",fg = "white") #ACのボタンについて #色の修正
btn.bind("<1>",click_del)
btn.grid(row=r+1, column=0)

btn = tk.Button(root,text="C", font=("",30), width=4, height=1) #C()backspace)のボタンについて
btn.bind("<1>",click_back)
btn.grid(row=r+1, column=1)

btn = tk.Button(root,text="+/-", font=("",30), width=4, height=1) #符号反転のボタンについて
btn.bind("<1>",click_reverse)
btn.grid(row=r+1, column=2)


root.mainloop()

