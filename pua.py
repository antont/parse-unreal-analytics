import json

#string constants to avoid typos in parsing .. todo?

def eventattrs(e):
    return {i['name']:i['value'] for i in e['attributes']}

def parseloc(locstr): #numbers from: 'X=-662.731 Y=491.465 Z=26.824'
    components = locstr.split(' ')
    
    def float_of_comp(compstr):
        v = compstr.split('=')[1]
        return float(v)

    coords = [float_of_comp(c) for c in components]
    return coords        

def parse_events(events):
    session = [] #all levels
    teleports = [] #teleports within a level
    #interacts = [] #interacts between teleports?

    for e in events:
        ename = e['eventName']
        #print(ename)
        if ename == 'Teleport':
            eventdata = eventattrs(e)
            locstr = eventdata['Location']
            coords = parseloc(locstr)
            teleports.append(coords)
        #if ename == 'Interact'
        #    countInteract += 1
        
        #here we can get Teleport coord data within level, until hit another BeginLevel
        if ename == 'BeginLevel':
            print("new BeginLevel")
            print("Teleport count in prev was: %d" % len(teleports))
            #print("Interact count in prev was: %d" % countInteract)
            session.append(teleports) #session is now a list of 'levels' i.e. a list of teleports
            teleports = []
            #countInteract = 0

            leveldata = eventattrs(e)
            print(leveldata)

    return session

def get_session():
    with open("data/Zotac06/282c0f304a7d160ff93664ad17e0a5db-2018.04.17-14.54.24.analytics", "r") as read_file:
        data = json.load(read_file)

    #print(data)
    
    sessionId = data['sessionId']
    events = data['events']

    start = events[0]
    #print(start)
    assert start['eventName'] == 'StartSession'

    beginLevel = events[1]
    #print(beginLevel)
    assert beginLevel['eventName'] == 'BeginLevel'
    leveldata = eventattrs(beginLevel)
    #for attr in levelattrs:
    print(leveldata)

    #first level should always be the library lobby
    assert leveldata['LevelName'] == 'MainLibrary'

    session = parse_events(events[2:])
    return session

if __name__ == '__main__':
    get_session()