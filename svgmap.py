import pua
import svgwrite

def init_drawing(i):
    dwg = svgwrite.Drawing(f'level_{i+1}.svg', profile='full')

    #marker biz from https://github.com/mozman/svgwrite/blob/master/examples/marker.py

    #--start-- A red point as marker-start element
    # 'insert' represents the insertation point in user coordinate space
    # in this example its the midpoint of the circle, see below
    marker_start = dwg.marker(insert=(0, 0), size=(5, 5)) # target size of the marker

    # setting a user coordinate space for the appanded graphic elements
    # bounding coordinates for this example:
    # minx = -5, maxx = +5, miny = -5, maxy = +5
    marker_start.viewbox(minx=-5, miny=-5, width=10, height=10) # the marker user coordinate space
    marker_start.add(dwg.circle((0, 0), r=10)).fill('red', opacity=0.5)
    
    #--end-- A blue point as marker-end element
    marker_end = dwg.marker(size=(20, 20)) # marker defaults: insert=(0,0)
    # set viewbox to the bounding coordinates of the circle
    marker_end.viewbox(-1, -1, 2, 2)
    marker_end.add(dwg.circle(fill='blue', fill_opacity=0.5)) # circle defaults: insert=(0,0), r=1
    
    dwg.defs.add(marker_start)
    dwg.defs.add(marker_end)

    markers = (marker_start, None, marker_end)
    return dwg, markers

def draw(dwg, markers, prev_point, point):
    #print(location)
    if prev_point is not None:
        #print(f"Line: {prev_point, point}")
        line = dwg.line(prev_point, point, stroke='blue')
        line.set_markers(markers)
        dwg.add(line)

    #dwg.add(dwg.circle((x, y), 10)) #stroke=svgwrite.rgb(10, 10, 16, '%')))

session = pua.get_session() #could give the source log file pathname

"""now a picture per level visit. does not check names of levels or anything yet."""
for i, level in enumerate(session): #.levels: #could include metadata, now is just the list of levels
    dwg, markers = init_drawing(i)

    all_x = []
    all_y = []

    #previous teleport point so that can draw a line from there to current
    prev_point = None

    for t in level: #.teleports:
        x, y, z = t #.location) 
        draw(dwg, markers, prev_point, (x, y))  #what if we wanna show what happened between the teleports? (interacts)

        #for bounds calc for viewbox below
        all_x.append(x)
        all_y.append(y)

        prev_point = (x, y)

    min_x = min(all_x)
    max_x = max(all_x)
    min_y = min(all_y)
    max_y = max(all_y)

    dwg.viewbox(min_x, min_y, max_x - min_x, max_y - min_y)
    dwg.save()