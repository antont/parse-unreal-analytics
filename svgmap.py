import pua
import svgwrite

import levelinfo #app specific info about the 3D scenes (unreal levels)

def init_drawing(i):
    dwg = svgwrite.Drawing(f'level_{i+1}.svg', profile='full')

    #coords of the level to show background image (map) correctly. should use the data for the given level, but now in wip we only have 1
    coords = levelinfo.MainLibrary
    min_x = coords[0][0]
    max_x = coords[1][0]
    min_y = coords[0][1]
    max_y = coords[3][1]
    width = max_x - min_x
    height= max_y - min_y

    dwg.add(dwg.image("Map-MainLibrary.png", x=min_x, y=min_y, width=width, height=height))
    dwg.viewbox(min_x, min_y, width, height)

    #debug: draw the level corners:
    #for c in coords:
    #    x, y, z = c
    #    dwg.add(dwg.circle((x, y), 100, fill="green")) #stroke=svgwrite.rgb(10, 10, 16, '%')))

    #marker biz from https://github.com/mozman/svgwrite/blob/master/examples/marker.py
    #svg arrow head from https://vanseodesign.com/web-design/svg-markers/

    marker_arrow = dwg.marker(markerWidth=100, markerHeight=100, refX=9, refY=3, orient="auto", markerUnits="strokeWidth")
    marker_arrow.viewbox(minx=-40, miny=-40, width=80, height=80)
    marker_arrow.add(dwg.path("M0,0 L0,6 L9,3 z", fill="#f00"))
    
    dwg.defs.add(marker_arrow)

    markers = (None, None, marker_arrow)
    return dwg, markers

def draw(dwg, markers, prev_point, point):
    #print(location)
    if prev_point is not None:
        #print(f"Line: {prev_point, point}")
        line = dwg.line(prev_point, point, stroke='blue', stroke_width=5)
        line.set_markers(markers)
        dwg.add(line)

    dwg.add(dwg.circle((x, y), 10)) #stroke=svgwrite.rgb(10, 10, 16, '%')))

session = pua.get_session() #could give the source log file pathname

"""now a picture per level visit. does not check names of levels or anything yet."""
for i, level in enumerate(session): #.levels: #could include metadata, now is just the list of levels
    dwg, markers = init_drawing(i)

    #old system to set view bounds so that log data fits. not used now, as we set the view to show the whole level
    #all_x = []
    #all_y = []

    #previous teleport point so that can draw a line from there to current
    prev_point = None

    for t in level: #.teleports:
        x, y, z = t #.location) 
        draw(dwg, markers, prev_point, (x, y))  #what if we wanna show what happened between the teleports? (interacts)

        #for bounds calc for viewbox below
        #all_x.append(x)
        #all_y.append(y)

        prev_point = (x, y)

    #min_x = min(all_x)
    #max_x = max(all_x)
    #min_y = min(all_y)
    #max_y = max(all_y)

    #margin = 2000
    #min_x -= margin
    #min_y -= margin
    #max_x += margin
    #max_y += margin

    #dwg.viewbox(min_x, min_y, max_x - min_x, max_y - min_y)

    dwg.save()