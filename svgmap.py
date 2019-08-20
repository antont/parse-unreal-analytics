import pua

def draw(location):
    print(location)

session = pua.get_session()

for level in session: #.levels: #could include metadata, now is just the list of levels
    for t in level: #.teleports:
        draw(t) #.location) #what if we wanna show what happened between the teleports?

