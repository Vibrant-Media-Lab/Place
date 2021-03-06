import smbus
import time

import urllib.request

from ServerConnector import Connector
from Panel import Panel

bus = smbus.SMBus(1)
ADDR = 0x04


WHITE_PIXEL = [0x1, 0x1, 0x1]
BLACK_PIXEL = [0x0, 0x0, 0x0]


panel1 = Panel(bus, 0x04)
#panel2 = Panel(bus, 0x05)

panels = [[panel1]]

color_grid = [[0 for x in range(15)] for y in range(15)]
color_grid[0][0] = [[[0 for x in range(3)] for y in range(32)] for z in range(32)]
color_grid[0][1] = [[[0 for x in range(3)] for y in range(32)] for z in range(32)]

#panel.fill_rect([0,0], [32,32], WHITE_PIXEL)

connector = Connector("http://pathealy.pythonanywhere.com/get_grid")
ticks = 0
ticked = False
wait_flag = False

while True:
    data = connector.get_dump()
    ticked = False
    for x in range(len(panels)):
        for y in range(len(panels[x])):
            try:
                if ticks % 5 == 0:
                    panels[0][0].draw_pixel([0,0], data[0][0][0][0])
                if(panels[x][y] is not None):
                    grid = data[x][y]
                    for i in range(len(grid)):
                        for j in range(len(grid[i])):
                            if not list(color_grid[x][y][j][i]) == list(grid[j][i]):
                                panels[x][y].draw_pixel([j, i], grid[j][i])
                                if waitFlag:
                                    time.sleep(6)
                                    panels[x][y].draw_pixel([j,i], grid[j][i])
                                    waitFlag = False
                                color_grid[x][y][j][i] = list(grid[j][i])
                                time.sleep(0.0001)
                                ticked = True
                                ticks = 0
                                
            except:
                print(y, " Failed")
                waitFlag = True
                color_grid[0][0] = [[[0 for x in range(3)] for y in range(32)] for z in range(32)]
                color_grid[0][1] = [[[0 for x in range(3)] for y in range(32)] for z in range(32)]
                time.sleep(6)                
    if not ticked:
        print("No update")
        ticks = ticks + 1
    if ticks > 100:
        time.sleep(60)
    elif ticks > 10:
        time.sleep(5)
    else:
        time.sleep(1)
    
