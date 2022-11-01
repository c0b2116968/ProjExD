import pygame as pg
import sys
from random import randint

class Screen: # 背景の設定
    def __init__(self, title, wh, pic):
        pg.display.set_caption(title)
        self.sfc = pg.display.set_mode(wh)
        self.rct = self.sfc.get_rect()
        self.bgi_sfc = pg.image.load(pic)
        self.bgi_rct = self.bgi_sfc.get_rect()

    def blit(self):
        self.sfc.blit(self.bgi_sfc, self.bgi_rct)

class Bird: # こうかとんのせってい
    key_delta = {
        pg.K_UP:    [0, -1],
        pg.K_DOWN:  [0, +1],
        pg.K_LEFT:  [-1, 0],
        pg.K_RIGHT: [+1, 0],
    }

    def __init__(self, img, zoom, xy):
        sfc = pg.image.load(img)
        self.sfc = pg.transform.rotozoom(sfc, 0, zoom)
        self.rct = self.sfc.get_rect() 
        self.rct.center = xy # こうかとんの位置

    def blit(self, scr):
        scr.sfc.blit(self.sfc, self.rct)

    def update(self, scr): # キーが押された時の処理
        key_states = pg.key.get_pressed()
        for key, delta in Bird.key_delta.items():
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


class Hp: # 体力の追加
    def __init__(self, hp):
        self.hp = hp

    def update(self, scr):
        fonto = pg.font.Font(None,100)
        txt = fonto.render(str(f"HP{self.hp}"), True, "red") # hp表示 赤文字
        scr.sfc.blit(txt,(200,100))


class Bomb2: # 爆弾２つめ
    def __init__(self, color, rad, vxy, scr):
        self.sfc = pg.Surface((rad*2, rad*2)) 
        self.sfc.set_colorkey((0, 0, 0)) 
        pg.draw.circle(self.sfc, color, (rad, rad), rad)
        self.rct = self.sfc.get_rect()
        self.rct.centerx = randint(0, scr.rct.width) #ランダムの位置に生成
        self.rct.centery = randint(0, scr.rct.height)
        self.vx, self.vy = vxy # 移動速度

    def blit(self, scr):
        scr.sfc.blit(self.sfc, self.rct)

    def update(self, scr):
        self.rct.move_ip(self.vx, self.vy) 
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
    hit = 200 # 体力

    scr = Screen("逃げろ！こうかとん", (1600, 900), "fig/pg_bg.jpg")
    # 練習3
    tori = Bird("fig/6.png", 2.0, (900, 400))
    # 練習5
    bkd = Bomb((255, 0, 0), 10, (1, 1), scr)
    # 敵
    mob = Mob("fig/teki.png", 2.0, (1, 1), scr)
    # 爆弾2つ目
    bkd2 = Bomb((0, 255, 0), 10, (1, 1), scr)

    clock = pg.time.Clock() # 練習1
    while True:
        scr.blit()
        for event in pg.event.get(): # 練習2
            if event.type == pg.QUIT:
                return

        tori.update(scr)
        # 練習7
        bkd.update(scr)
        # 敵キャラの更新
        mob.update(scr)
        # 体力の更新
        HP = Hp(hit)
        HP.update(scr)

        key_states = pg.key.get_pressed() # spaceを押した時の処理
        if key_states[pg.K_SPACE]:
            bkd2.update(scr)

        # 練習8
        if tori.rct.colliderect(bkd.rct) or tori.rct.colliderect(mob.rct) or tori.rct.colliderect(bkd2.rct): # こうかとんrctが敵と爆弾rctと重なったら
            hit -= 1
            if hit <= 0:
                return

        pg.display.update() #練習2
        clock.tick(1000)


if __name__ == "__main__":
    pg.init() # 初期化
    main()    # ゲームの本体
    pg.quit() # 初期化の解除
    sys.exit()
