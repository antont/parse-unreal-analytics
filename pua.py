import json

with open("data/Zotac06/282c0f304a7d160ff93664ad17e0a5db-2018.04.17-14.54.24.analytics", "r") as read_file:
    data = json.load(read_file)

#print(data)

#string constants to avoid typos in parsing .. todo?

sessionId = data['sessionId']

events = data['events']

start = events[0]
#print(start)
assert start['eventName'] == 'StartSession'

beginLevel = events[1]
#print(beginLevel)
assert beginLevel['eventName'] == 'BeginLevel'
leveldata = {i['name']:i['value'] for i in beginLevel['attributes']}
#for attr in levelattrs:
print(leveldata)

#first level should always be the library lobby
assert leveldata['LevelName'] == 'MainLibrary'

countTeleport = 0
countInteract = 0
for e in events[2:]:
    ename = e['eventName']
    #print(ename)
    if ename == 'Teleport':
        countTeleport += 1
    if ename == 'Interact':
        countInteract += 1
    
    #here we can get Teleport coord data within level, until hit another BeginLevel
    if ename == 'BeginLevel':
        print("new BeginLevel")
        print("Teleport count in prev was: %d" % countTeleport)
        print("Interact count in prev was: %d" % countInteract)
        countTeleport = 0
        countInteract = 0

        leveldata = {i['name']:i['value'] for i in e['attributes']}
        print(leveldata)

