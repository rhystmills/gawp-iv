import svgwrite
import random

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

tileSize = 1;

def drawThing(position1, position2):
    return dwg.line(position1, position2, transform=f"rotate({getRotation(position1)})")

def getRotation(position):
    return str(random.randint(0,1) * 90) + f" {position[0] + tileSize/2} {position[1] + tileSize/2}"

for x in range(0,99):
    for y in range (0,99):
        dwg.add(drawThing((x, y),(x + tileSize, y + tileSize)))

dwg.saveas("svg/truchet_003.svg")


# subdivision_probability = 0.6

# def draw_square_or_subdivide(position, width, height, depth):
#     if depth < 7 and random.random() < subdivision_probability:
#         new_depth = depth + 1
#         return subdivide(position, width, height, new_depth)
#     color_fill = choose_fill()
#     return dwg.rect(position, (width, height), fill=color_fill)

# def choose_fill():
#     n = random.random()
#     if n > 0.98: return "#00ecff"
#     if n > 0.96: return "#f300c8"
#     if n > 0.94: return "#ffe321"
#     if n > 0.9: return "#000000"
#     return "#ffffff"

# def subdivide(position, width, height, depth):
#     group = dwg.g()
#     for x in range(0, 2):
#         for y in range(0, 2):
#             square_width = width/2
#             square_height = height/2
#             x_position = position[0] + (x * square_width)
#             y_position = position[1] + (y * square_height)
#             square_position = (x_position, y_position)
#             group.add(draw_square_or_subdivide(square_position, square_width, square_height, depth))
#     return group

# dwg.add(subdivide((0,0), width, height, 0))
# dwg.saveas("iii008.svg")

### 007 series - increasing subdisivion chance