from src.scan import scan
from src.play import play
from src.render import render
from openni import openni2

if __name__ == '__main__':
    print('Mode (scan/play/render):', end=' ')
    mode = input()
    print('Record filename:', end=' ')
    name = input()
    if mode == 'scan':
        openni2.initialize()
        print('Exposure Strategy (lock/sweep):', end=' ')
        exposure_strategy = input()
        scan(name, exposure_strategy)
        play(name)
        openni2.unload()
    elif mode == 'play':
        openni2.initialize()
        play(name)
        openni2.unload()
    elif mode == 'render':
        render(name)
