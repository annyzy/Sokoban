import utilitiesLWB
import train

if __name__ == '__main__':
    #Sokoban = utilitiesLWB.loadMapFromVisualRepresentationTxt("TestingUtilites")
    Sokoban = utilitiesLWB.GenerateMap(10, 10, 3, 20)
    direction=0
    gif_images=[]
    utilitiesLWB.showMap(Sokoban.currMap)

    for i in range(6):
        reward=Sokoban.getReward(direction)
        if (reward == None):
            break
        print("-------------------------------------------\nreward="+str(reward)+"\n")
        Sokoban=Sokoban.move(direction)
        utilitiesLWB.showMap(Sokoban.currMap)
        gif_images.append(utilitiesLWB.Map2Png(Sokoban.currMap))
    utilitiesLWB.Png2Gif(gif_images,'./')
    
    