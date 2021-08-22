import copy
import time
from graphics import *

def d(a, b):
    return abs(a[0]-b[0])+abs(a[1]-b[1])

def max(args):
    i = 0
    for j in range(len(args)):
        if args[j] > args[i]:
            i = j
    return i

def average(args, default=0):
    try:
        return sum(args) / len(args)
    except ZeroDivisionError:
        return default

def mklist(width, height, value):
    ll = [value] * width
    l = []
    for i in range(height):
        l.append(copy.deepcopy(ll))
    return l

def pathfinder(startCoords, endCoords, obstacleCoords, width, height, iterations):
    obstacleCoords.append(startCoords)
    sGrid = mklist(width, height, 0)
    nsGrid = copy.deepcopy(sGrid)
    for i in range(iterations):
        for x in range(width):
            for y in range(height):
                avg = []
                for coords in ((0, -1), (0, 1), (-1, 0), (1, 0)):
                    dx = coords[0]
                    dy = coords[1]
                    try:
                        doAdd = True
                        for coord in obstacleCoords:
                            if tuple(coord) == (x+dx, y+dy):
                                doAdd = False
                        if doAdd and y+coords[1] >= 0 and x+coords[0] >= 0:
                            avg.append(sGrid[y+dy][x+dx])
                    except IndexError:
                        pass
                nsGrid[y][x] = average(avg, nsGrid[y][x])
        sGrid = copy.deepcopy(nsGrid)
        sGrid[endCoords[1]][endCoords[0]] = 1000000
    for coords in obstacleCoords:
        sGrid[coords[1]][coords[0]] = 0
    dcoordlist = []
    currentCoords = list(startCoords)
    dcoords = ((0, -1), (0, 1), (-1, 0), (1, 0))
    while currentCoords != list(endCoords):
        values = []
        try:
            values.append(sGrid[currentCoords[1] + dcoords[0][1]][currentCoords[0] + dcoords[0][0]])
        except IndexError:
            values.append(-1000000)
        try:
            values.append(sGrid[currentCoords[1] + dcoords[1][1]][currentCoords[0] + dcoords[1][0]])
        except IndexError:
            values.append(-1000000)
        try:
            values.append(sGrid[currentCoords[1] + dcoords[2][1]][currentCoords[0] + dcoords[2][0]])
        except IndexError:
            values.append(-1000000)
        try:
            values.append(sGrid[currentCoords[1] + dcoords[3][1]][currentCoords[0] + dcoords[3][0]])
        except IndexError:
            values.append(-1000000)
        mdcoord = dcoords[max(values)]
        dcoordlist.append(mdcoord)
        currentCoords[0] += mdcoord[0]
        currentCoords[1] += mdcoord[1]
    return dcoordlist

def pathfinder_n(startCoords, endCoords, obstacleCoords, width, height, iterations, n):
    obstacleCoords.append(startCoords)
    obstacleCoords.remove(endCoords)
    sGrid = mklist(width, height, 0)
    nsGrid = copy.deepcopy(sGrid)
    ncoordstr = '((0, -i), (0, i), (-i, 0), (i, 0))'
    for i in range(iterations):
        for x in range(width):
            for y in range(height):
                avg = []
                for coords in ((0, -1), (0, 1), (-1, 0), (1, 0)):
                    dx = coords[0]
                    dy = coords[1]
                    try:
                        doAdd = True
                        for coord in obstacleCoords:
                            if tuple(coord) == (x+dx, y+dy):
                                doAdd = False
                        if doAdd and y+coords[1] >= 0 and x+coords[0] >= 0:
                            avg.append(sGrid[y+dy][x+dx])
                    except IndexError:
                        pass
                nsGrid[y][x] = average(avg, nsGrid[y][x])
        sGrid = copy.deepcopy(nsGrid)
        sGrid[endCoords[1]][endCoords[0]] = 1000000
#        for i in range(n, 0, -1):
#            ncoords = eval(ncoordstr)
#            sGrid[ncoords[0][1]][ncoords[0][0]] = 1000000
    for coords in obstacleCoords:
        sGrid[coords[1]][coords[0]] = 0
    dcoordlist = []
    currentCoords = list(startCoords)
    dcoords = ((0, -1), (0, 1), (-1, 0), (1, 0))
    ncoordstr = '((0, -i), (0, i), (-i, 0), (i, 0))'
    while True:
        exit = False
        for i in range(n, 0, -1):
            ncoords = eval(ncoordstr)
            if currentCoords[0] + ncoords[0][0] == endCoords[0] and currentCoords[1] + ncoords[0][1] == endCoords[1]: move = 0; exit = True; break
            if currentCoords[0] + ncoords[1][0] == endCoords[0] and currentCoords[1] + ncoords[1][1] == endCoords[1]: move = 1; exit = True; break
            if currentCoords[0] + ncoords[2][0] == endCoords[0] and currentCoords[1] + ncoords[2][1] == endCoords[1]: move = 2; exit = True; break
            if currentCoords[0] + ncoords[3][0] == endCoords[0] and currentCoords[1] + ncoords[3][1] == endCoords[1]: move = 3; exit = True; break
        if exit:
            break
        values = []
        try:
            values.append(sGrid[currentCoords[1] + dcoords[0][1]][currentCoords[0] + dcoords[0][0]])
        except IndexError:
            values.append(-1000000)
        try:
            values.append(sGrid[currentCoords[1] + dcoords[1][1]][currentCoords[0] + dcoords[1][0]])
        except IndexError:
            values.append(-1000000)
        try:
            values.append(sGrid[currentCoords[1] + dcoords[2][1]][currentCoords[0] + dcoords[2][0]])
        except IndexError:
            values.append(-1000000)
        try:
            values.append(sGrid[currentCoords[1] + dcoords[3][1]][currentCoords[0] + dcoords[3][0]])
        except IndexError:
            values.append(-1000000)
        mdcoord = dcoords[max(values)]
        dcoordlist.append(mdcoord)
        currentCoords[0] += mdcoord[0]
        currentCoords[1] += mdcoord[1]
    return dcoordlist, ncoords[move]

class SGrid():
    def __init__(self, width, height, win):
        self.width = width
        self.height = height
        self.squares = []
        self.coords = []
        for y in range(height):
            row = []
            for x in range(width):
                self.coords.append((x, y))
                square = Rectangle(Point(x*25+5, y*25+5), Point(x*25+25, y*25+25))
                square.setFill('white')
                square.draw(win)
                row.append(square)
            self.squares.append(row)
    def getGrid(self):
        return self.squares
    def getCoords(self):
        return self.coords
    def getSquare(self, coords):
        return self.squares[coords[1]][coords[0]]
    def getSquares(self):
        squares = []
        for row in self.squares:
            for square in row:
                squares.append(square)
        return squares
    def getClick(self, click):
        squares = self.getSquares()
        for i in range(len(squares)):
            if (squares[i].getP1().getX() <= click.getX() and
            squares[i].getP2().getX() >= click.getX() and
            squares[i].getP1().getY() <= click.getY() and
            squares[i].getP2().getY() >= click.getY()):
                return self.getCoords()[i]
        return None
    def clicked(self, coords, ships, grid, win):
        if coords:
            if self.getSquare(coords).config['fill'] == 'green':
                for ship in ships:
                    if ship.active:
                        shipcoords = []
                        for tship in ships:
                            if tship != ship:
                                shipcoords.append(tship.getCoords())
                        ship.clicked(grid, ships)
                        for dcoords in pathfinder(ship.getCoords(), coords, shipcoords, grid.width, grid.height, d(coords, ship.getCoords()) + 3):
                            dx = dcoords[0]
                            dy = dcoords[1]
                            for i in range(12):
                                ship.img.move(dx*2, dy*2)
                                time.sleep(0.02)
                                update()
                            ship.img.move(dx, dy)
                            update()
                            ship.x += dx
                            ship.y += dy
            elif self.getSquare(coords).config['fill'] == 'red':
                for ship in ships:
                    if ship.active:
                        for ship2 in ships:
                            if ship2.getCoords() == coords:
                                shipcoords = []
                                for tship in ships:
                                    if tship != ship:
                                        shipcoords.append(tship.getCoords())
                                ship.clicked(grid, ships)
                                result = pathfinder_n(ship.getCoords(), coords, shipcoords, grid.width, grid.height, d(coords, ship.getCoords()) + 3, ship.dist)
                                for dcoords in result[0]:
                                    dx = dcoords[0]
                                    dy = dcoords[1]
                                    for i in range(12):
                                        ship.img.move(dx*2, dy*2)
                                        time.sleep(0.02)
                                        update()
                                    ship.img.move(dx, dy)
                                    ship.x += dx
                                    ship.y += dy
                                bullet = Circle(Point((ship.img.getP1().getX() + ship.img.getP2().getX()) / 2,
                                                      (ship.img.getP1().getY() + ship.img.getP2().getY()) / 2), 2.5)
                                bullet.setFill('black')
                                bullet.draw(win)
                                for i in range(12):
                                    bullet.move(result[1][0]*2, result[1][1]*2)
                                    time.sleep(0.02)
                                    update()
                                bullet.move(result[1][0], result[1][1])
                                update()
                                bullet.undraw()
                                del bullet
                                ship2.img.undraw()
                                ships.pop(ships.index(ship2))

class Ship():
    def __init__(self, x, y, moves, dist, win, color):
        self.img = Rectangle(Point(x*25+10, y*25+10), Point(x*25+20, y*25+20))
        self.img.setFill(color)
        self.img.draw(win)
        self.x = x
        self.y = y
        self.moves = moves
        self.dist = dist
        self.active = False
    def getCoords(self):
        return self.x, self.y
    def getClick(self, click):
        if (self.img.getP1().getX() <= click.getX() and
        self.img.getP2().getX() >= click.getX() and
        self.img.getP1().getY() <= click.getY() and
        self.img.getP2().getY() >= click.getY()):
            return True
        return False
    def clicked(self, grid, ships):
        if self.moves != 0 and self.dist != 0:
            for square in grid.getSquares():
                if square.config['fill'] != 'white':
                    square.setFill('white')
        if self.active:
            self.active = False
        elif not self.active:
            squares = grid.getGrid()
            coords = grid.getCoords()
            l = mklist(grid.width, grid.height, False)
            l[self.y][self.x] = True
            lnew = copy.deepcopy(l)
            dcoords = ((0, -1), (0, 1), (-1, 0), (1, 0))
            ncoordstr = '((0, -j), (0, j), (-j, 0), (j, 0))'
            for i in range(self.moves):
                for x in range(grid.width):
                    for y in range(grid.height):
                        checks = []
                        try:
                            if y+dcoords[0][1] >= 0 and x+dcoords[0][0] >= 0:
                                checks.append(l[y+dcoords[0][1]][x+dcoords[0][0]])
                            else:
                                raise IndexError
                        except IndexError:
                            checks.append(False)
                        try:
                            if y+dcoords[1][1] >= 0 and x+dcoords[1][0] >= 0:
                                checks.append(l[y+dcoords[1][1]][x+dcoords[1][0]])
                            else:
                                raise IndexError
                        except IndexError:
                            checks.append(False)
                        try:
                            if y+dcoords[2][1] >= 0 and x+dcoords[2][0] >= 0:
                                checks.append(l[y+dcoords[2][1]][x+dcoords[2][0]])
                            else:
                                raise IndexError
                        except IndexError:
                            checks.append(False)
                        try:
                            if y+dcoords[3][1] >= 0 and x+dcoords[3][0] >= 0:
                                checks.append(l[y+dcoords[3][1]][x+dcoords[3][0]])
                            else:
                                raise IndexError
                        except IndexError:
                            checks.append(False)
                        coordlist = []
                        for ship in ships:
                            coordlist.append(ship.getCoords())
                        if checks[0] or checks[1] or checks[2] or checks[3]:
                            if (x, y) not in coordlist:
                                lnew[y][x] = True
                            else:
                                lnew[y][x] = None
                l = copy.deepcopy(lnew)
            for x in range(grid.width):
                for y in range(grid.height):
                    if not (x == self.x and y == self.y):
                        if l[y][x]:
                            squares[y][x].setFill('green')
                        else:
                            for j in range(self.dist, 0, -1):
                                ncoords = eval(ncoordstr)
                                checks = []
                                try:
                                    if y+dcoords[0][1] >= 0 and x+dcoords[0][0] >= 0:
                                        checks.append(l[y+ncoords[0][1]][x+ncoords[0][0]])
                                    else:
                                        raise IndexError
                                except IndexError:
                                    checks.append(False)
                                try:
                                    if y+dcoords[1][1] >= 0 and x+dcoords[1][0] >= 0:
                                        checks.append(l[y+ncoords[1][1]][x+ncoords[1][0]])
                                    else:
                                        raise IndexError
                                except IndexError:
                                    checks.append(False)
                                try:
                                    if y+dcoords[2][1] >= 0 and x+dcoords[2][0] >= 0:
                                        checks.append(l[y+ncoords[2][1]][x+ncoords[2][0]])
                                    else:
                                        raise IndexError
                                except IndexError:
                                    checks.append(False)
                                try:
                                    if y+dcoords[3][1] >= 0 and x+dcoords[3][0] >= 0:
                                        checks.append(l[y+ncoords[3][1]][x+ncoords[3][0]])
                                    else:
                                        raise IndexError
                                except IndexError:
                                    checks.append(False)
                                if checks[0] or checks[1] or checks[2] or checks[3]:
                                    for ship in ships:
                                        if ship.getCoords() == (x, y):
                                            squares[y][x].setFill('red')
            update()
            for tship in ships:
                if tship != self:
                    tship.active = False
            self.active = True

win = GraphWin('Grid', 500, 500, autoflush=False)
grid = SGrid(15, 15, win)
ships = [Ship(3, 4, 3, 1, win, 'red'),
         Ship(6, 8, 5, 1, win, 'blue'),
         Ship(2, 13, 1, 1, win, 'yellow'),
         Ship(7, 10, 10, 1, win, 'purple'),
         Ship(10, 10, 0, 0, win, 'black'),
         Ship(10, 11, 0, 0, win, 'black'),
         Ship(10, 12, 0, 0, win, 'black'),
         Ship(10, 13, 0, 0, win, 'black'),
         Ship(10, 14, 0, 0, win, 'black'),
         Ship(11, 10, 0, 0, win, 'black'),
         Ship(12, 10, 0, 0, win, 'black'),
         Ship(14, 14, 2, 1, win, 'green'),
         Ship(12, 3, 15, 1, win, 'orange')]
update()
while True:
    try:
        click = win.getMouse()
    except GraphicsError:
        break
    coords = grid.getClick(click)
    if coords and grid.getSquare(coords).config['fill'] != 'white':
        grid.clicked(grid.getClick(click), ships, grid, win)
    else:
        for ship in ships:
            if ship.getClick(click):
                ship.clicked(grid, ships)

win.close()
