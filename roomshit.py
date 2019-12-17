import random as rn

rooms = []

def generateMaze(rooms):



    xCord = rn.randint(0,2)
    yCord = rn.randint(0,2)

    roomCord = [xCord,yCord]
    
    generateRoom(roomCord,rooms)
    
    
    


def generateRoom(cords,rooms):
    room = Room(cords)
    
    rooms.append(room)
    


    rnd = rn.randint(1,2)
    if rnd == 1:
        room.doorsExist[0] = True

    if room.doorsExist[0]:
        room.doorsExist[0] = False
        generateRoom([cords[0]+1,cords[1]],rooms)
        


class Room:
    def __init__(self,worldCord,doors=[False,False,False,False]):
        self.positon = worldCord
        self.doorsExist = doors

        

generateMaze(rooms)

for i in range(len(rooms)):
    print(rooms[i].positon)

