import random
import time

al = 26  # アルファベット
tal = 10 # 対象
kal = 2  # 欠損
tr = 2 # 回数

def shutudai(a):
    ap = random.sample(a, tal)
    print("対象：", end="")
    for j in sorted(ap): 
        print(j, end=" ")
    print()

    k = random.sample(ap, kal)
    print("表示：", end="")
    for c in ap: 
        if c not in k:
            print(c, end=" ")
    print()
    print("欠損：", k)
    return k


def kaito(kotae):
    n = int(input("欠損はいくつ？："))
    if n != kal:
        print("不正解")
    else:
        print("正解.欠損を1つずつ入力.")
        for i in range(n):
            c = input(f"{i+1}文字目を入力：")
            if c not in kotae:
                print("不正解です．またチャレンジしてください．")
                return False
            else:
                kotae.remove(c)
        else:
            print("欠損文字も含めて正解")
            return True
    return False


if __name__ == "__main__":
    alphabet = [chr(i+65) for i in range(al)]

    k = shutudai(alphabet)
    r = kaito(k)
    


