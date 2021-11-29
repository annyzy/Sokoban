import utilitiesLWB


if __name__ == '__main__':
    # Sokoban = utilitiesLWB.loadMapFromTxt("input00");
    Sokoban = utilitiesLWB.loadMapFromVisualRepresentationTxt("TestingUtilites");
    direction=0
    print(Sokoban.getReward(direction))
    # utilitiesLWB.showMap(Sokoban.currMap)
    # print("-------------------------------------------\nreward="+str(Sokoban.getReward(direction))+"\n")
    # Sokoban.move(direction)
    # utilitiesLWB.showMap(Sokoban.currMap)
    # # utilitiesLWB.showMap(Sokoban.currMap)
    # # print(Sokoban.getAgentPosition())
    # # print(Sokoban.getBoxPositions())
    # # print(Sokoban.getWallPositions())
    # # print(Sokoban.getStorageLocation())
    # # print(Sokoban.moveUp() == None)