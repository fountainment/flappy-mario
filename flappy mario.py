import fountain
import sys
import random
from hashlib import md5
import time

from pygame.locals import *

have = 0
wudi = 0

class cnPair(fountain.render.baseObj):
    def __init__(self, cnimage, x, y):
        self.cn1 = fountain.render.drawObj(cnimage)
        self.cn2 = fountain.render.drawObj(cnimage)
        self.x = x
        self.y = y
        self.z = 0.5
        self.cn1.set_Center(x, y - 50 - 266, self.z)
        self.cn2.set_Center(x, y + 50 + 266, self.z)
        self.cn2.rotate(0.0, 0.0, 180)
        self.ring = 0
        self.havestar = 0

    def set_y(self, y):
        d = 0
        if self.y != y:
            d = (y - self.y) / 3
        self.y = self.y + d
        self.cn1.set_y(self.y - 316)
        self.cn2.set_y(self.y + 316)

    def draw(self):
        global have, mod
        self.cn1.set_x(self.x)
        self.cn2.set_x(self.x)
        self.cn1.draw()
        self.cn2.draw()
        if self.havestar == 1:
            star.set_Center(*self.get_Center())
            star.draw()
        if self.x < -27:
            self.x += 900
            if have == 0:
                if random.randint(1, 20) == 1:
                    self.havestar = 1
                    have = 1
                else:
                    self.havestar = 0
                    have = 0
            self.y = random.randint(200, 420)
            self.cn1.set_Center(self.x, self.y - 316, self.z)
            self.cn2.set_Center(self.x, self.y + 316, self.z)
            self.ring = 0

def encode53(x):
    a = str(x)
    for i in range(3):
        a = md5(a).hexdigest().upper()
    return a

def printScore(score, num, center = 650, interval = 40):
    ss = str(score)
    sn = len(ss)
    n = 0
    for i in range(-(sn - 1) * (interval / 2), (sn - 1) * (interval / 2) + 1, interval):
        num.set_x(center + i)
        num.draw(int(ss[n]))
        n += 1

def jumpf():
    global speed
    if man.get_y() < 500:
        speed = flyspeed
    soundEffect[0].play(jumps)

def gencnp(x1, y1, y2, interval, n):
    xp = []
    for i in range(n):
        xp.append(cnPair(cnimage, x1, random.randint(y1, y2)))
        x1 += interval
    return xp

def diefunc():
    global live, mspeed, speed, bottomy, fpsc, score, highscore
    if live == 1:
        fountain.media.stopmusic()
        soundEffect[1].play(dies)
        live = 0
        mspeed = 0
        speed = 0
        bottomy = -1000
        fpsc = 0
        if score > highscore:
            highscore = score
            new.set_visible(True)
            fountain.data.dump('./game.dat', (highscore, encode53(highscore)))
    

def restart():
    global mspeed, speed, cnp, live, score, fpsc, bottomy, have
    mspeed = 2.0
    speed = 0
    cnp = gencnp(800, 200, 420, 150, 6)
    man.set_Center(240, 240, 5)
    manj.set_Center(240, 240, 5)
    mand.set_Center(240, 240, 5)
    mang.set_Center(240, 240, 5)
    mangj.set_Center(240, 240, 5)
    gameover.set_transp(0.0)
    rec.set_transp(0.0)
    new.set_transp(0.0)
    hnum.set_transp(0.0)
    num.set_Center(100, 420, 50)
    new.set_visible(False)
    live = 1
    score = 0
    fpsc = 0
    fountain.media.playmusic(-1)
    bottomy = 127
    start = 0
    have = 0

def WUDI():
    global mode
    man.state = 'WUDI'
    fountain.media.stopmusic()
    fountain.media.loadmusic('./music/god.mp3')
    fountain.media.playmusic(-1)
    mode = -1

def NORMAL():
    global mode
    man.state = 'NORMAL'
    fountain.media.stopmusic()
    fountain.media.loadmusic('./music/bgm.mp3')
    fountain.media.playmusic(-1)
    mode = 1

TDG = fountain.gamesys.game('Flappy Mario', (750, 500), fs = False, ogl = True, renderFps = 60)
fountain.render.oglInit(*TDG.winSize)
bgimage = fountain.render.imageObj('./image/bg.png')
fgimage = fountain.render.imageObj('./image/fg.png')
cnimage = fountain.render.imageObj('./image/cn.png')
manimage = fountain.render.imageObj('./image/man01.png')
manjimage = fountain.render.imageObj('./image/man02.png')
mandimage = fountain.render.imageObj('./image/man03.png')
numimage = fountain.render.imageObj('./ui/num.png')
welcomeimage = fountain.render.imageObj('./ui/welcome.png')
starimage = fountain.render.imageObj('./image/st.png')
overimage = fountain.render.imageObj('./ui/gameover.png')
mangimage = fountain.render.imageObj('./image/god01.png')
mangjimage = fountain.render.imageObj('./image/god02.png')

#final
newimage = fountain.render.imageObj('./ui/new.png')
recimage = fountain.render.imageObj('./ui/rec.png')
hnumimage = fountain.render.imageObj('./ui/hnum.png')

openAnime = fountain.render.animeObj(fountain.data.loadcAnime('./image/movie/movie.ani'), 375, 250, 80, 2)

bg = fountain.render.drawObj(bgimage)
fg1 = fountain.render.drawObj(fgimage)
fg2 = fountain.render.drawObj(fgimage)
man = fountain.render.drawObj(manimage)
manj = fountain.render.drawObj(manjimage)
mand = fountain.render.drawObj(mandimage)
mang = fountain.render.drawObj(mangimage)
mangj = fountain.render.drawObj(mangjimage)
welcome = fountain.render.drawObj(welcomeimage)
gameover = fountain.render.drawObj(overimage)
star = fountain.render.drawObj(starimage)
num = fountain.render.drawObj(numimage, horN = 10.0, verN = 1.0)
cnp = gencnp(800, 200, 420, 150, 6)

#final

new = fountain.render.drawObj(newimage)
rec = fountain.render.drawObj(recimage)
hnum = fountain.render.drawObj(hnumimage, horN = 10.0, verN = 1.0)


bg.set_LeftBottom(0, 0)
fg1.set_LeftBottom(0, 0, 1)
fg2.set_LeftBottom(fgimage.oriSize[0], 0, 1)
man.set_Center(240, 240, 5)
manj.set_Center(240, 240, 5)
mand.set_Center(240, 240, 5)
mang.set_Center(240, 240, 5)
mangj.set_Center(240, 240, 5)
num.set_Center(100, 420, 50)
welcome.set_Center(375, 400, 60)
gameover.set_Center(375, 400, 60)
gameover.set_transp(0.0)

#final
new.set_Center(304, 50, 60)
new.set_transp(0.0)
rec.set_Center(350, 50, 60)
rec.set_transp(0.0)
hnum.set_Center(375, 50, 60)
hnum.set_transp(0.0)
new.set_visible(False)


fountain.media.loadmusic('./music/bgm.mp3')

jumps = fountain.media.Sound('./music/jump.wav')
coins = fountain.media.Sound('./music/coin.wav')
dies = fountain.media.Sound('./music/die.wav')
overs = fountain.media.Sound('./music/over.wav')
soundEffect = [fountain.media.Channel(0), fountain.media.Channel(1)]
soundEffect[0].set_volume(0.1)
soundEffect[1].set_volume(0.1)
fountain.media.music.set_volume(0.2)
high = fountain.data.load('game.dat')
if high == None:
    highscore = 0
elif encode53(high[0]) != high[1]:
    highscore = 0
else:
    highscore = high[0]

mw2 = man.image.w2 - 2
mh2 = man.image.h2 - 2 

pw2 = cnimage.w2 - 2
ph2 = cnimage.h2 - 2
fpsc = 0

start = 0
speed = 0
mspeed = 2.0
live = 1
score = 0
bottomy = 127
diedelay = 150
flyspeed = 7.0

vis = 1
mode = 1
fn = 1
mod = 3
man.state = 'NORMAL'

while True:
    fn += 1
    fn %= mod
    if fn == 0:
        vis *= -1
    fountain.render.renderBegin()
    bg.draw()
    for p in cnp:
        p.draw()
    fg1.draw()
    fg2.draw()

    if mode == 1 or vis == 1:
        if live == 1:
            if speed > 0:
                manj.draw()
            else:
                man.draw()
        else:
            mand.draw()
    elif mode == -1:
        if speed > 0:
            mangj.draw()
        else:
            mang.draw()

    if start == 1:
        fg1.move(-mspeed, 0, 0)
        fg2.move(-mspeed, 0, 0)
        man.move(0, speed, 0)
        manj.move(0, speed, 0)
        mand.move(0, speed, 0)
        mang.move(0, speed, 0)
        mangj.move(0, speed, 0)

        for p in cnp:
            mx = man.get_x()
            my = man.get_y()
            px = p.cn1.get_x()
            py = p.cn1.get_y()
            if man.state == 'WUDI':
                if px - mx < 100 and px - mx > -40:
                    p.set_y(man.get_y())
                elif wudi >= 5 and px - mx < 110 and px - mx > 0: 
                    NORMAL()
                    wudi = 0
                    mod = 3
            if mode == 1 and man.state != 'WUDI':
                if (abs(px - mx) < (pw2 + mw2)) and (abs(py - my) < (ph2 + mh2)):
                    diefunc()
                px = p.cn2.get_x()
                py = p.cn2.get_y()
                if (abs(px - mx) < (pw2 + mw2)) and (abs(py - my) < (ph2 + mh2)):
                    diefunc()

            if live == 0:
                if fpsc < diedelay + 1:
                    fpsc += 1
                
            if fpsc == diedelay:
                soundEffect[1].play(overs)
                speed = flyspeed
            
            p.move(-mspeed, 0, 0)
            if p.get_x() == man.get_x() + 4 and p.ring == 0:
                soundEffect[1].play(coins)
                score += 1
                p.ring = 1
                if man.state == 'WUDI':
                    wudi += 1
                    if wudi == 4:
                        mod = 10
                if p.havestar == 1:
                    WUDI()
                    p.havestar = 0
                    have = 0
        #ground loop
        if fg2.get_x() == 375:
            fg1.set_LeftBottom(0, 0, 1)
            fg2.set_LeftBottom(fgimage.oriSize[0], 0, 1)

        #groud colition
        if man.get_y() >= bottomy:
            if fpsc <= 0 or fpsc == diedelay + 1:
                speed -= 0.4
        else:
            speed = 0
            man.set_y(bottomy)
            manj.set_y(bottomy)
            mang.set_y(bottomy)
            mangj.set_y(bottomy)
            mand.set_y(bottomy)

        #print score & highscore
        printScore(score, num, 375)

        #draw GAMEOVER
        if live == 0:
            if man.get_y() == bottomy:
                printScore(highscore, hnum, 410, 22)
                gameover.draw()
                gameover.transp_plus(0.037)
                new.draw()
                new.transp_plus(0.037)
                rec.draw()
                rec.transp_plus(0.037)
                hnum.transp_plus(0.037)
            if man.get_y() < bottomy + 100:
                if num.get_y() > 250:
                    num.move(0, -10, 0)


    #draw WELCOME
    if start != 1:
        welcome.draw()
        
    openAnime.draw()
    fountain.render.renderEnd()

    #event solve
    for event in fountain.pygame.event.get():
        if event.type == QUIT:
            fountain.pygame.quit()
            sys.exit()
        elif event.type == KEYDOWN:
            if event.key == K_ESCAPE or event.key == K_q:
                fountain.pygame.quit()
                sys.exit()
            elif live == 1:
                if start == 1:
                    jumpf()
                else:
                    start = 1
                    if not openAnime.get_busy():
                        fountain.media.playmusic(-1)
                    else:
                        start = 0
            else:
                if man.get_y() == bottomy:
                    restart()
        elif event.type == MOUSEBUTTONDOWN:
            if live == 1:
                if start == 1:
                    jumpf()
                else:
                    start = 1
                    if not openAnime.get_busy():
                        fountain.media.playmusic(-1)
                    else:
                        start = 0
            else:
                if man.get_y() == bottomy:
                    restart()

    TDG.renderEnd()

