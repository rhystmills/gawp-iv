import svgwrite
import math
from svgwrite.container import Group
import random
from circle_intersection import Geometry

width = 50
height = 50
dwg = svgwrite.Drawing(
  'test.svg', 
  size=(width, height), 
  profile='tiny', 
  stroke_width=0.15,
  stroke='black',
  stroke_opacity=1.0,
  fill='none'
)

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
    return list(map(
        round_to_4,
        get_intersections(x1, y1, r1, x2, y2, r2)
    ))

print(get_rounded_coords(0,0,1,1,1,1))

tileSize = 1

def drawThing(x1, y1, x2, y2):
    r2 = tileSize/2
    [intersection_x1, intersection_y1, intersection_x2, intersection_y2] = get_rounded_coords(x1, y2, tileSize, x2, y1, r2)
    rotation = getRotation(x1, y1, tileSize)
    group = dwg.defs.add(Group(id=f"{str(x1)}a{str(y1)}a{str(x2)}a{str(y2)}"))
    group.add(dwg.path(
        d=drawArc(x1, y1, x2, y2, tileSize, True),
        transform=f"rotate({rotation})"
        ))
    group.add(dwg.path(
        d=drawArc(x1, y1+(tileSize/2), x2-(tileSize/2), y2, tileSize/2, True),
        transform=f"rotate({rotation})"
    ))
    # group.add(dwg.path(
    #     d=drawArc(x1 + tileSize/2, y1, x2, y2 - tileSize/2, tileSize/2),
    #     transform=f"rotate({rotation})"
    # ))
    group.add(dwg.path(
        d=drawArc(x1 + tileSize/2, y1, intersection_x1, intersection_y1, tileSize/2),
        transform=f"rotate({rotation})"
    ))
    group.add(dwg.path(
        d=drawArc(intersection_x2, intersection_y2, x2, y2 - tileSize/2, tileSize/2),
        transform=f"rotate({rotation})"
    ))
    return group

def drawArc(x1, y1, x2, y2, radius, altCircle=False):
    arc = f"M{x1},{y1} A{radius},{radius} 0 0 {str(1 if altCircle else 0)} {x2},{y2}"
    return arc
    
def getRotation(x, y, tileSize):
    return str(random.randint(0,3) * 90) + f" {x + tileSize/2} {y + tileSize/2}"

for x in range(0,16):
    for y in range (0,32):
        dwg.add(drawThing(x, y, x + tileSize, y + tileSize))

dwg.saveas("svg/truchet_024.svg")
