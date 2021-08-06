import svgwrite
import math
from svgwrite.container import Group
import random
from circle_intersection import Geometry

width = 100
height = 100
dwg = svgwrite.Drawing(
  'test.svg', 
  size=(width, height), 
  profile='tiny', 
  stroke_width=0.15,
  stroke='black',
  stroke_opacity=1.0,
  fill='none'
)
tileSize = 1
factor = 8

def get_intersections(x0, y0, r0, x1, y1, r1):
    # circle 1: (x0, y0), radius r0
    # circle 2: (x1, y1), radius r1

    d=math.sqrt((x1-x0)**2 + (y1-y0)**2)
    
    # non intersecting
    if d > r0 + r1 :
        return None
    # One circle within other
    if d < abs(r0-r1):
        return None
    # coincident circles
    if d == 0 and r0 == r1:
        return None
    else:
        a=(r0**2-r1**2+d**2)/(2*d)
        h=math.sqrt(r0**2-a**2)
        x2=x0+a*(x1-x0)/d   
        y2=y0+a*(y1-y0)/d   
        x3=x2+h*(y1-y0)/d     
        y3=y2-h*(x1-x0)/d 

        x4=x2-h*(y1-y0)/d
        y4=y2+h*(x1-x0)/d
        
        return (x3, y3, x4, y4)

def round_to_4(n):
    return round(n, 4)

def get_rounded_coords(x1, y1, r1, x2, y2, r2):
    intersections = get_intersections(x1, y1, r1, x2, y2, r2)
    if intersections:
        return list(map(
            round_to_4,
            get_intersections(x1, y1, r1, x2, y2, r2)
        ))
    else:
        return list()

def drawThing(x1, y1, x2, y2):
    r2 = tileSize
    intersections = get_rounded_coords(x1, y2, tileSize * factor, x2, y1, r2)
    if (random.randint(0,1) == 0):
        # Add arcs
        rotation = getRotation(x1, y1, tileSize * factor, 90)
        # group = dwg.defs.add(Group(id=f"{str(x1)}a{str(y1)}a{str(x2)}a{str(y2)}"))
        # group.add(dwg.path(
        #     d=draw_arc(x1, y1, x2, y2, tileSize * 2, True),
        #     transform=f"rotate({rotation})"
        #     ))
        # group.add(dwg.path(
        #     d=draw_arc(x1, y1+(tileSize), x2-(tileSize), y2, tileSize, True),
        #     transform=f"rotate({rotation})"
        # ))
        # group.add(dwg.path(
        #     d=draw_arc(x1 + tileSize, y1, intersection_x1, intersection_y1, tileSize),
        #     transform=f"rotate({rotation})"
        # ))
        # group.add(dwg.path(
        #     d=draw_arc(intersection_x2, intersection_y2, x2, y2 - tileSize, tileSize),
        #     transform=f"rotate({rotation})"
        # ))
        # return group
        return draw_arc_tile(x1, y1, x2, y2, tileSize * factor, rotation)
    else:
        # Add lines
        rotation = getRotation(x1, y1, tileSize * factor, 180)
        # group = dwg.defs.add(Group(id=f"{str(x1)}a{str(y1)}a{str(x2)}a{str(y2)}"))
        # group.add(dwg.path(
        #     d=draw_line(x1, y1, x1, y1 + tileSize),
        #     transform=f"rotate({rotation})"
        # ))
        # group.add(dwg.path(
        #     d=draw_line(x1 + tileSize/2, y1, x1 + tileSize/2, y1 + tileSize),
        #     transform=f"rotate({rotation})"
        # ))
        # group.add(dwg.path(
        #     d=draw_line(x2, y1, x2, y1 + tileSize),
        #     transform=f"rotate({rotation})"
        # ))
        return draw_line_tile(x1, y1, x2, y2, rotation)


def draw_arc(x1, y1, x2, y2, radius, altCircle=False):
    arc = f"M{x1},{y1} A{radius},{radius} 0 0 {str(1 if altCircle else 0)} {x2},{y2}"
    return arc
    
def draw_arc_tile(x1, y1, x2, y2, radius, rotation):
    group = dwg.defs.add(Group(id=f"{get_unique_id()}"))
    arcs = []
    biggest_arc = []
    resize = lambda point, n, total_arcs : int(point/total_arcs * (n + 1))
    total_arcs = int(x2-x1/tileSize)
    for n in range(0, total_arcs):
        group.add(dwg.path(
            d=draw_arc(
                x1, 
                y1 + (total_arcs - n - 1), 
                x2 - (total_arcs - n - 1), 
                y2, 
                n + 1, 
                True),
            transform=f"rotate({rotation})"
        ))
        if (n == total_arcs - 1):
            biggest_arc = [x1, y2, radius]
    for n in range (0, total_arcs - 1):
        intersections = get_rounded_coords(
            biggest_arc[0], 
            biggest_arc[1], 
            biggest_arc[2], 
            x2, 
            y1, 
            n + 1
        )
        if intersections:
            [intersection_x1, intersection_y1, intersection_x2, intersection_y2] = intersections
            print(n)
            print(intersections)
            group.add(dwg.path(
                d=draw_arc(x2 - n - 1, y1, intersection_x1, intersection_y1, n + 1),
                transform=f"rotate({rotation})"
            ))
            group.add(dwg.path(
                d=draw_arc(intersection_x2, intersection_y2, x2, y1 + n + 1, n + 1),
                transform=f"rotate({rotation})"
            ))
        else:
            group.add(dwg.path(
                d=draw_arc(x2 - n - 1, y1, x2, y1 + n + 1, n + 1),
                transform=f"rotate({rotation})"
            ))
    return group

def draw_line_tile(x1, y1, x2, y2, rotation):
    # Where the two points are the top left and bottom right corner of the tile
    group = dwg.defs.add(Group(id=f"{get_unique_id()}"))
    thisTileSize = x2 - x1
    for n in range(0, int(thisTileSize/tileSize) + tileSize):
        group.add(dwg.path(
            d=draw_line(x1 + n*tileSize, y1, x1 + n*tileSize, y2),
            transform=f"rotate({rotation})"
        ))
    return group

ids = []
def get_unique_id():
    possibleGroupId = random.randint(0, 1000000)
    if possibleGroupId not in ids:
        ids.append(possibleGroupId)
        return str(possibleGroupId)
    return "sdsd"

def draw_line(x1, y1, x2, y2):
    return f"M {x1} {y1} L {x2} {y2}"

def getRotation(x, y, tileSize, degrees):
    return str(random.randint(0,360/degrees) * 90) + f" {x + tileSize/2} {y + tileSize/2}"

for x in range(0,50):
    for y in range (0,50):
        dwg.add(drawThing(x * factor, y * factor, x * factor + tileSize * factor, y * factor + tileSize * factor))

dwg.saveas("svg/truchet_033.svg")
