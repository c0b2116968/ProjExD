import pygame as pg
import sys
from random import randint

# 玉の設定
BULLET_MAX = 100 
bull_n = 0
bull_x =[0]*BULLET_MAX
bull_y =[0]*BULLET_MAX
bull_f =[False]*BULLET_MAX
img = pg.image.load("fig/10.png")

def set_bullet(px,py):#弾のスタンバイ
    global bull_n
    bull_f[bull_n] = True
    bull_x[bull_n] = px-16
    bull_y[bull_n] = py-32
    bull_n = (bull_n+1)%BULLET_MAX

def move_bullet(screen):#弾を飛ばす
    for i in range(BULLET_MAX):
        if bull_f[i] == True:
            bull_y[i] = bull_y[i] - 5  
            screen.blit(img,[bull_x[i],bull_y[i]])
            if bull_y[i] < 0:
                bull_f[i] = False

class Screen: # 背景の設定
    def __init__(self, title, wh, pic):
        pg.display.set_caption(title)
        self.sfc = pg.display.set_mode(wh)
        self.rct = self.sfc.get_rect()
        self.bgi_sfc = pg.image.load(pic)
        self.bgi_rct = self.bgi_sfc.get_rect()

    def blit(self):
        self.sfc.blit(self.bgi_sfc, self.bgi_rct)
        return self.sfc

class Bird: # こうかとんのせってい
    key_delta = {
        pg.K_UP:    [0, -1],
        pg.K_DOWN:  [0, +1],
        pg.K_LEFT:  [-1, 0],
        pg.K_RIGHT: [+1, 0],
    }

    def __init__(self, img, zoom, xy,space=0):
        sfc = pg.image.load(img)
        self.sfc = pg.transform.rotozoom(sfc, 0, zoom)
        self.rct = self.sfc.get_rect() 
        self.rct.center = xy # こうかとんの位置
        self.space = space

    def blit(self, scr):
        scr.sfc.blit(self.sfc, self.rct)

    def update(self, scr): # キーが押された時の処理
        key_states = pg.key.get_pressed()
        for key, delta in Bird.key_delta.items():
            if key_states[pg.K_SPACE]:
                self.space += 1
                if self.space%500==1:
                    set_bullet(self.rct.centerx, self.rct.centery)
            if key_states[key]:
                self.rct.centerx += delta[0]
                self.rct.centery += delta[1]
                if check_bound(self.rct, scr.rct) != (+1, +1):
                    self.rct.centerx -= delta[0]
                    self.rct.centery -= delta[1]
        self.blit(scr)


class Bomb: # 爆弾の追加
    def __init__(self, color, rad, vxy, scr):
        self.sfc = pg.Surface((rad*2, rad*2)) # 空のSurface
        self.sfc.set_colorkey((0, 0, 0)) # 四隅の黒い部分を透過させる
        pg.draw.circle(self.sfc, color, (rad, rad), rad) # 爆弾用の円を描く
        self.rct = self.sfc.get_rect()
        self.rct.centerx = randint(0, scr.rct.width)
        self.rct.centery = randint(0, scr.rct.height)
        self.vx, self.vy = vxy # 練習6

    def blit(self, scr):
        scr.sfc.blit(self.sfc, self.rct)

    def update(self, scr):
        self.rct.move_ip(self.vx, self.vy) # 練習6
        yoko, tate = check_bound(self.rct, scr.rct)
        self.vx *= yoko
        self.vy *= tate
        self.blit(scr)


class Mob: # 敵キャラの追加
    def __init__(self, img, zoom, vxy, scr):
        sfc = pg.image.load(img) # 写真を追加
        self.sfc = pg.transform.rotozoom(sfc, 0, zoom)
        self.rct = self.sfc.get_rect()
        self.rct.centerx = randint(0, scr.rct.width) #ランダムの位置に生成
        self.rct.centery = randint(0, scr.rct.height)
        self.vx, self.vy = vxy #移動速度設定

    def blit(self, scr):
        scr.sfc.blit(self.sfc, self.rct)

    def update(self, scr):
        self.rct.move_ip(self.vx, self.vy) # 練習6
        yoko, tate = check_bound(self.rct, scr.rct)
        self.vx *= yoko
        self.vy *= tate
        self.blit(scr)


def check_bound(obj_rct, scr_rct):
    """
    obj_rct:こうかとんrct,または,爆弾rct
    scr_rct:スクリーンrct
    領域内:+1/領域外:-1
    """
    yoko, tate = +1, +1
    if obj_rct.left < scr_rct.left or scr_rct.right < obj_rct.right: 
        yoko = -1
    if obj_rct.top < scr_rct.top or scr_rct.bottom < obj_rct.bottom: 
        tate = -1
    return yoko, tate


def main():
    scr = Screen("逃げろ！こうかとん", (1600, 900), "fig/space.jpg")
    # 練習3
    tori = Bird("fig/6.png", 2.0, (900, 400))
    # 練習5
    bkd = Bomb((255, 0, 0), 10, (1, 1), scr)
    # 敵
    mob = Mob("fig/teki.png", 2.0, (1, 1), scr)
    clock = pg.time.Clock() # 練習1

    while True:
        s = scr.blit()
        for event in pg.event.get(): # 練習2
            if event.type == pg.QUIT:
                return
        move_bullet(s)
        tori.update(scr)
        # 練習7
        bkd.update(scr)
        # 敵キャラの更新
        mob.update(scr)

        if tori.rct.colliderect(bkd.rct) or tori.rct.colliderect(mob.rct):
            return

        pg.display.update() #練習2
        clock.tick(1000)


if __name__ == "__main__":
    pg.init() # 初期化
    main()    # ゲームの本体
    pg.quit() # 初期化の解除
    sys.exit()
