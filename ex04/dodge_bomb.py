import pygame as pg
import sys
from random import randint

def check_bound(obj_rct, scr_rct):
    """
    obj_rct:こうかとんrct,または,爆弾rct
    scr_rct:スクリーンrct
    領域内：+1/領域外：-1
    """
    yoko, tate = +1, +1
    if obj_rct.left < scr_rct.left or scr_rct.right < obj_rct.right: 
        yoko = -1
    if obj_rct.top < scr_rct.top or scr_rct.bottom < obj_rct.bottom: 
        tate = -1
    return yoko, tate

def main():
    hp = 200
    # 1
    pg.display.set_caption("逃げろ！こうかとん")
    scrn_sfc = pg.display.set_mode((1600, 900))
    scrn_rct = scrn_sfc.get_rect()
    bg_sfc = pg.image.load("fig/pg_bg.jpg")
    bg_rct = bg_sfc.get_rect()

    fonto = pg.font.Font(None,100)
    
    # 3
    tori_sfc = pg.image.load("fig/6.png")
    tori_sfc = pg.transform.rotozoom(tori_sfc, 0, 2.0)
    tori_rct = tori_sfc.get_rect()
    tori_rct.center = 900, 400

    #death
    d_sfc = pg.image.load("fig/ene2.png")
    d_sfc = pg.transform.rotozoom(d_sfc, 0, 3.0)
    d_rct = d_sfc.get_rect()
    d_rct.center = tori_rct.centerx, tori_rct.centery

    # 5
    hl_sfc = pg.Surface((20, 20)) # 空のSurface
    hl_sfc.set_colorkey((0, 0, 0)) # 四隅の黒い部分を透過させる
    pg.draw.circle(hl_sfc, (0, 255, 0), (10, 10), 10) # 円を描く
    hl_rct = hl_sfc.get_rect()
    hl_rct.centerx = randint(0, scrn_rct.width)
    hl_rct.centery = randint(0, scrn_rct.height)

    # 敵
    bomb_sfc = pg.image.load("fig/teki.png")
    bomb_sfc = pg.transform.rotozoom(bomb_sfc, 0, 2.0)
    bomb_rct = bomb_sfc.get_rect()
    bomb_rct.centerx = randint(0, scrn_rct.width)
    bomb_rct.centery = randint(0, scrn_rct.height)

    # 6
    vx, vy = 1, 1
    zx, zy = 2, 2 # 回復の移動処理

    clock = pg.time.Clock() # 1
    while True:
        scrn_sfc.blit(bg_sfc, bg_rct) # 2
        d_rct.center = tori_rct.centerx, tori_rct.centery

        if hp >= 200: # HPの色設定
            col = "green"
        elif  200> hp > 100:
            col = "yellow"
        else:
            col = "red"
        txt = fonto.render(str(f"HP{hp}"), True, col) # hp表示
        scrn_sfc.blit(txt,(200,100))
        
        for event in pg.event.get(): # 2
            if event.type == pg.QUIT: return

        key_states = pg.key.get_pressed() #key操作
        if key_states[pg.K_UP]:    tori_rct.centery -= 1
        if key_states[pg.K_DOWN]:  tori_rct.centery += 1
        if key_states[pg.K_LEFT]:  tori_rct.centerx -= 1
        if key_states[pg.K_RIGHT]: tori_rct.centerx += 1
        yoko, tate = check_bound(tori_rct, scrn_rct)
        if yoko == -1:
            if key_states[pg.K_LEFT]: 
                tori_rct.centerx += 1
            if key_states[pg.K_RIGHT]:
                tori_rct.centerx -= 1
        if tate == -1:
            if key_states[pg.K_UP]: 
                tori_rct.centery += 1
            if key_states[pg.K_DOWN]:
                tori_rct.centery -= 1   

        scrn_sfc.blit(tori_sfc, tori_rct) # 練習3
        if hp <= 1: # 死んだときに骸骨表示する(delayはかけているが0にすると表示が遅い)
            scrn_sfc.blit(d_sfc, d_rct) # とりを骸骨にする

        # 7
        yoko, tate = check_bound(bomb_rct, scrn_rct)
        vx *= yoko
        vy *= tate
        bomb_rct.move_ip(vx, vy) # 6
        scrn_sfc.blit(bomb_sfc, bomb_rct) # 5

        # 回復の移動処理
        x, y = check_bound(hl_rct, scrn_rct)
        zx *= x
        zy *= y
        hl_rct.move_ip(zx, zy) 
        scrn_sfc.blit(hl_sfc, hl_rct)

        if tori_rct.colliderect(hl_rct): # こうかとんと回復が重なったらhp+0.5
            hp += 0.5

        # 8
        if tori_rct.colliderect(bomb_rct): # こうかとんと爆弾が重なったらhp-0.5
            hp -= 0.5
        
        scrn_sfc.blit(txt,(200,100))

        if hp <= -1: # hpがゼロ以下で終了(0だと最後の表示がずれるため-1)
            pg.time.delay(2000)
            return

        pg.display.update() #2
        clock.tick(1000)
        

if __name__ == "__main__":
    pg.init() # 初期化
    main() # ゲームの本体
    pg.quit() # 初期化の解除
    sys.exit()