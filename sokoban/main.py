import utilitiesLWB
import train

if __name__ == '__main__':
    Sokoban = utilitiesLWB.loadMapFromVisualRepresentationTxt("TestingUtilites");
    direction=0
    utilitiesLWB.showMap(Sokoban.currMap)
    for i in range(6):
        reward=Sokoban.getReward(direction)
        if (reward == None):
            break
        print("-------------------------------------------\nreward="+str(reward)+"\n")
        Sokoban=Sokoban.move(direction)
        utilitiesLWB.showMap(Sokoban.currMap)