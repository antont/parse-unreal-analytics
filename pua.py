import json

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
leveldata = {i['name']:i['value'] for i in beginLevel['attributes']}
#for attr in levelattrs:
print(leveldata)

#first level should always be the library lobby
assert leveldata['LevelName'] == 'MainLibrary'

for e in events[2:20]:
    ename = e['eventName']
    print(ename)
    
    #here we can get Teleport coord data within level, untill hit another BeginLevel
