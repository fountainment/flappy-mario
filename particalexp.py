import fountain
test = fountain.gamesys.game('particl test', (500, 500))
fountain.render.oglInit(*test.winSize)
fountain.render.ftEnable('POINTSMOOTH')
p = fountain.render.particleGenerater((250, 250), 2000, 0)
while True:
    fountain.render.renderBegin()
    p.drawPoint()
    test.eventSolve()
    fountain.render.renderEnd()
    test.renderEnd()
