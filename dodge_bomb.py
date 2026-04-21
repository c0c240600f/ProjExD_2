import os
import sys
import time  # 課題１
import random
import pygame as pg


WIDTH, HEIGHT = 1100, 650
DELTA = {
    pg.K_UP : (0, -5),   # 上
    pg.K_DOWN : (0, +5),  # 下
    pg.K_LEFT : (-5, 0),  # 左
    pg.K_RIGHT : (+5, 0),  # 右
}


os.chdir(os.path.dirname(os.path.abspath(__file__)))


def check_bound(rct: pg.Rect) -> tuple[bool, bool]:
    """
    引数：こうかとんRectか爆弾Rect
    戻り値：タプル（横方向判定結果, 縦方向判定結果）
    画面内ならTrue, 画面外ならFalse
    """
    yoko, tate = True, True
    if rct.left < 0 or WIDTH < rct.right:  # 横方向判定
        yoko = False
    if rct.top < 0 or HEIGHT < rct.bottom:  # 縦方向判定
        tate = False
    return yoko, tate


def gameover(screen: pg.Surface) -> None:  # 課題１
    """
    ゲームオーバー画面を表示する関数
    """
    black = pg.Surface((WIDTH, HEIGHT))  # 1-1
    pg.draw.rect(black, (0, 0, 0), pg.Rect(0, 0, WIDTH, HEIGHT))
    black.set_alpha(200)  # 1-2
    font = pg.font.Font(None, 80)  # 1-3
    text = font.render("Game Over", True, (255, 255, 255))
    text_rect = text.get_rect(center=(WIDTH//2, HEIGHT//2))
    kk_dead = pg.image.load("fig/0.png")
    kk_dead = pg.transform.rotozoom(kk_dead, 0, 0.9)
    kk_rct = kk_dead.get_rect()
    kk_rct.center = (WIDTH//2 -200, HEIGHT//2)
    kk_dead_2 = pg.image.load("fig/0.png")
    kk_dead_2 = pg.transform.rotozoom(kk_dead_2, 0, 0.9)
    kk_rct_2 = kk_dead_2.get_rect()
    kk_rct_2.center = (WIDTH//2 +200, HEIGHT//2)
    screen.blit(black, (0, 0))
    screen.blit(kk_dead, kk_rct)
    screen.blit(kk_dead_2, kk_rct_2)
    screen.blit(text, text_rect)
    pg.display.update()
    time.sleep(5)


def init_bb_imgs() -> tuple[list[pg.Surface], list[int]]:  # 課題３
    """
    時間とともに爆弾が拡大、加速させる関数
    """
    bb_imgs = []
    bb_accs = []

    for r in range(1, 11):  # 1〜10段階
        bb_img = pg.Surface((20*r, 20*r))
        pg.draw.circle(bb_img, (255, 0, 0), (10*r, 10*r), 10*r)
        bb_img.set_colorkey((0, 0, 0))
        bb_imgs.append(bb_img)
    bb_accs = [a for a in range(1, 11)]
    return bb_imgs, bb_accs


def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("fig/pg_bg.jpg")    
    kk_img = pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 0.9)
    kk_rct = kk_img.get_rect()
    kk_rct.center = 300, 200

    bb_img = pg.Surface((20, 20))  # 爆弾用の空のSurface
    pg.draw.circle(bb_img, (255, 0, 0), (10, 10), 10)
    bb_img.set_colorkey((0, 0, 0))
    bb_rct = bb_img.get_rect()  # 爆弾のbb_rctの取得
    bb_rct.centerx = random.randint(0, WIDTH)  # 初期座標の設定
    bb_rct.centery = random.randint(0, HEIGHT)
    vx, vy = +5, +5  # 爆弾の速度

    bb_imgs, bb_accs = init_bb_imgs()  # 課題２ 呼び出し

    clock = pg.time.Clock()
    tmr = 0
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return
            
        if kk_rct.colliderect(bb_rct):  # こうかとんの衝突判定
            gameover(screen) # 課題１
            return
        
        screen.blit(bg_img, [0, 0]) 

        key_lst = pg.key.get_pressed()
        sum_mv = [0, 0]
        #if key_lst[pg.K_UP]:
            #sum_mv[1] -= 5
        #if key_lst[pg.K_DOWN]:
            #sum_mv[1] += 5
        #if key_lst[pg.K_LEFT]:
            #sum_mv[0] -= 5
        #if key_lst[pg.K_RIGHT]:
            #sum_mv[0] += 5
            
        for key, mv in DELTA.items():
            if key_lst[key]:
                sum_mv[0] += mv[0]  #横方向
                sum_mv[1] += mv[1]  #縦方向
    
        kk_rct.move_ip(sum_mv)
        if check_bound(kk_rct) != (True, True):  # 位置の判定
            kk_rct.move_ip(-sum_mv[0],-sum_mv[1])
        screen.blit(kk_img, kk_rct)
        #bb_rct.move_ip(vx, vy)  # 爆弾を移動させる
        yoko, tate = check_bound(bb_rct)  # 爆弾の反射
        if not yoko:
            vx *= -1
        if not tate:
            vy *= -1
        
        bb_img = bb_imgs[min(tmr // 500, 9)]  # 課題２ 加速
        acc = bb_accs[min(tmr // 500, 9)]
        avx = vx * acc
        avy = vy * acc
        bb_rct.width = bb_img.get_rect().width
        bb_rct.height = bb_img.get_rect().height
        bb_rct.move_ip(avx, avy)

        screen.blit(bb_img, bb_rct)  # 爆弾の表示

        pg.display.update()
        tmr += 1
        clock.tick(50)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()
