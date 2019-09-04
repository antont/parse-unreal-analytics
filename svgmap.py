import pua
import svgwrite

def draw(dwg, prev_point, point):
    #print(location)
    if prev_point is not None:
        #print(f"Line: {prev_point, point}")
        dwg.add(dwg.line(prev_point, point, stroke='blue'))

    dwg.add(dwg.circle((x, y), 10)) #stroke=svgwrite.rgb(10, 10, 16, '%')))

session = pua.get_session() #could give the source log file pathname

"""now a picture per level visit. does not check names of levels or anything yet."""
for i, level in enumerate(session): #.levels: #could include metadata, now is just the list of levels
    dwg = svgwrite.Drawing(f'level_{i+1}.svg', profile='tiny')
    all_x = []
    all_y = []

    #previous teleport point so that can draw a line from there to current
    prev_point = None

    for t in level: #.teleports:
        x, y, z = t #.location) 
        draw(dwg, prev_point, (x, y))  #what if we wanna show what happened between the teleports? (interacts)

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