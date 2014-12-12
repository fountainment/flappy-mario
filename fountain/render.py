# -*- coding: utf-8 -*-

from OpenGL.GL import *
from OpenGL.GLU import *
import random
import PIL.Image as Image

textureDic = {}

def ftEnable(x):
    if x == 'LINESMOOTH':
        glEnable(GL_LINE_SMOOTH)
        glHint(GL_LINE_SMOOTH_HINT, GL_FASTEST)
    elif x == 'POINTSMOOTH':
        glEnable(GL_POINT_SMOOTH)
        glHint(GL_POINT_SMOOTH_HINT, GL_NICEST)
    elif x == 'MULTISAMPLE':
        glEnable(GL_MULTISAMPLE)

def ftSetClearColor(r, g, b, a = 1.0):
    glClearColor(r, g, b, a)

def oglInit(w, h, zrange = (-100, 100)):
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    glShadeModel(GL_SMOOTH)
    glViewport(0, 0, w, h)
    glClearColor(0.0, 0.0, 0.0, 1.0)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0, w, 0, h, *zrange)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

def recordList(image):
    glNewList(image.listID, GL_COMPILE)
    glBegin(GL_QUADS)
    glTexCoord2f(0, 0)
    glVertex2f(-image.w2, -image.h2)
    glTexCoord2f(1, 0)
    glVertex2f(image.w2, -image.h2)
    glTexCoord2f(1, 1)
    glVertex2f(image.w2, image.h2)
    glTexCoord2f(0, 1)
    glVertex2f(-image.w2, image.h2)
    glEnd()
    glEndList()
    
class imageObj:
    def __init__(self, filename = None, string = None, w = None, h = None):
        global textureDic
        if filename != None:
            pic = Image.open(filename)
            self.oriSize = pic.size[:]
            self.pics = pic.tostring("raw", "RGBA", 0, -1)
        else:
            self.pics = string
            self.oriSize = (w, h)
        self.textureID = glGenTextures(1)
        self.listID = glGenLists(1)
        textureDic[filename] = self.textureID
        glBindTexture(GL_TEXTURE_2D, self.textureID)
        glTexEnvf(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_REPLACE)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, self.oriSize[0], self.oriSize[1], 0, GL_RGBA, GL_UNSIGNED_BYTE, self.pics)
        self.w2 = self.oriSize[0] / 2
        self.h2 = self.oriSize[1] / 2
        recordList(self)

    def bindTex(self, mode = GL_MODULATE):
        glTexEnvf(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, mode)
        glBindTexture(GL_TEXTURE_2D, self.textureID)

    def drawQuad(self, horN = 1.0, verN = 1.0, horI = 0, verI = 0):
        if horN == 1.0 and verN == 1.0:
            glCallList(self.listID)
        else:
            w2 = self.w2 / horN
            h2 = self.h2 / verN
            tl = horI / horN
            tr = tl + (1.0 / horN)
            tb = verI / verN
            tt = tb + (1.0 / verN)
            glBegin(GL_QUADS)
            glTexCoord2f(tl, tb)
            glVertex2f(-w2, -h2)
            glTexCoord2f(tr, tb)
            glVertex2f(w2, -h2)
            glTexCoord2f(tr, tt)
            glVertex2f(w2, h2)
            glTexCoord2f(tl, tt)
            glVertex2f(-w2, h2)
            glEnd()

    def blit(self, x, y):
        glBlitFrameBuffer()

    def zoom(self, x):
        if (x > 0):
            self.w2 *= x
            self.h2 *= x
        recordList(self)

class baseObj:
    def set_Center(self, x, y, z = 0):
        self.x = x
        self.y = y
        self.z = z

    def set_LeftBottom(self, x, y, z = 0):
        self.x = x + self.image.w2
        self.y = y + self.image.h2
        self.z = z

    def get_Center(self):
        return (self.x, self.y, self.z)

    def get_x(self):
        return self.x

    def get_y(self):
        return self.y

    def set_x(self, x):
        self.x = x

    def set_y(self, y):
        self.y = y

    def move(self, x, y, z = 0):
        self.x += x
        self.y += y

    def update(self):
        self.move(*self.speed)

    def rotate(self, x, y, z):
        self.xAg += x
        self.yAg += y
        self.zAg += z

    def set_visible(self, x):
        self.visible = x

class drawObj(baseObj):
    def __init__(self, image, horN = 1.0, verN = 1.0):
        self.image = image
        self.x = 0.0
        self.y = 0.0
        self.z = 0.0
        self.xAg = 0.0
        self.yAg = 0.0
        self.zAg = 0.0
        self.horN = horN
        self.verN = verN
        self.transp = 1.0
        self.visible = True

    def draw(self, horI = 0, verI = 0):
        if self.visible == True:
            glEnable(GL_TEXTURE_2D)
            self.image.bindTex()
            glPushMatrix()
            glTranslatef(self.x, self.y, self.z)
            if self.xAg != 0:
                glRotatef(self.xAg, 1.0, 0.0, 0.0)
            if self.yAg != 0:
                glRotatef(self.yAg, 0.0, 1.0, 0.0)
            if self.zAg != 0:
                glRotatef(self.zAg, 0.0, 0.0, 1.0)
            glColor4f(1.0, 1.0, 1.0, self.transp)
            glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
            self.image.drawQuad(self.horN, self.verN, horI, verI)
            glPopMatrix()
            glDisable(GL_TEXTURE_2D)
            glColor4f(1.0, 1.0, 1.0, 1.0)

    def set_transp(self, x):
        self.transp = x

    def transp_plus(self, x):
        if self.transp < 1.0:
            self.transp += x

class animeObj(baseObj):
    def __init__(self, animeData, x = 0, y = 0, z = 0, ppf = 1):
        self.frames = []
        for pic in animeData:
            self.frames.append(imageObj(None, *pic))
        self.x, self.y, self.z = x, y, z
        self.framen = len(self.frames)
        self.ppf = ppf
        self.n = 0
        self.mn = 0

    def set_at(self, x):
        self.n = x
        self.mn = 0

    def draw(self):
        if self.n < self.framen:
            glEnable(GL_TEXTURE_2D)
            glPushMatrix()
            glTranslatef(self.x, self.y, self.z)
            self.frames[self.n].bindTex()
            self.frames[self.n].drawQuad()
            glPopMatrix()
            glDisable(GL_TEXTURE_2D)
            self.mn += 1
            self.mn %= self.ppf
            if self.mn == 0:
                self.n += 1
    
    def get_busy(self):
        return not self.n == self.framen

    def get_framen(self):
        return self.framen

    def get_at(self):
        return self.n

def shakeBegin(a = 2):
    x = random.randint(-a, a)
    y = random.randint(-a, a)
    z = random.randint(-a, a)
    glPushMatrix()
    glTranslatef(x, y, z);

def shakeEnd():
    glPopMatrix()

def renderBegin():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glEnable(GL_DEPTH_TEST)
    pass

def renderEnd():
    pass

class particle(baseObj):
    def __init__(self, pos, size, speed):
        self.set_Center(*pos)
        self.speed = speed
        self.size = size

    def drawPoint(self):
        glPointSize(self.size)
        glBegin(GL_POINTS)
        glVertex3f(self.x, self.y, self.z)
        glEnd()

class particleGenerater(baseObj):
    def __init__(self, pos, num, direct = (0, 0)):
        self.set_Center(*pos)
        self.pList = []
        for i in range(num):
            self.pList.append(particle((random.randint(-100, 100), random.randint(-100, 100)), random.random() * 5, ((random.randint(-100,100) / 100.0), random.randint(-100,100) / 100.0)))

    def drawPoint(self):
        glPushMatrix()
        glTranslatef(self.x, self.y, self.z)
        for p in self.pList:
            glColor3f(random.random(), random.random(), random.random())
            p.drawPoint()
            p.update()
        glPopMatrix()


