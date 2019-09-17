import pua
import svgwrite

def init_drawing(i):
    dwg = svgwrite.Drawing(f'level_{i+1}.svg', profile='full')

    #marker biz from https://github.com/mozman/svgwrite/blob/master/examples/marker.py
    #svg arrow head from https://vanseodesign.com/web-design/svg-markers/

    marker_arrow = dwg.marker(markerWidth=100, markerHeight=100, refX=9, refY=3, orient="auto", markerUnits="strokeWidth")
    marker_arrow.viewbox(minx=-20, miny=-20, width=40, height=40)
    marker_arrow.add(dwg.path("M0,0 L0,6 L9,3 z", fill="#f00"))
    
    dwg.defs.add(marker_arrow)

    markers = (None, None, marker_arrow)
    return dwg, markers

def draw(dwg, markers, prev_point, point):
    #print(location)
    if prev_point is not None:
        #print(f"Line: {prev_point, point}")
        line = dwg.line(prev_point, point, stroke='blue')
        line.set_markers(markers)
        dwg.add(line)

    dwg.add(dwg.circle((x, y), 3)) #stroke=svgwrite.rgb(10, 10, 16, '%')))

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