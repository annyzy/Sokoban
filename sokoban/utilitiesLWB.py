import numpy as np
from SokobanMap import SokobanMap
from PIL import Image
import imageio
from map_generator.MapGenerator import generate_map
#map中数值含义：      0:空白    1：墙     2：箱子位置    3：箱子目标    4：小人    5:箱子在目标上    6:小人在目标上
#map values：      0:null    1：wall     2：box    3：storage location    4：agent    5:box in storage   6:agent on storage

def loadMapFromTxt(fileName):
    with open("./inputTxt/"+fileName+".txt","r") as f:
        walls=[]
        boxes=[]
        targets=[]
        for line in f:
            # 第一行：  列数 与 行数
            # 1st line：  numRows & numColumns
            firstLine = line.strip('\n')
            currline = firstLine.split(" ")
            numRows=int(currline[0])
            numColumns=int(currline[1])
            currMap = np.zeros((numRows, numColumns), dtype=int)

            # 第二行：  墙
            # 2nd line：  Walls
            secondLine = next(f).strip('\n')
            currline = secondLine.split(" ")
            nWallSquares = int(currline[0])
            for i in range(nWallSquares):
                currRow = int(currline[2*i+1])-1
                currColumn = int(currline[2*i+2])-1
                walls.append([currRow,currColumn])
                currMap[currRow][currColumn]=1

            # 第三行：  箱子
            # 3rd line：  Boxes
            thirdLine = next(f).strip('\n')
            currline = thirdLine.split(" ")
            nBoxes = int(currline[0])
            for i in range(nBoxes):
                currRow = int(currline[2*i+1])-1
                currColumn = int(currline[2*i+2])-1
                boxes.append([currRow,currColumn])
                currMap[currRow][currColumn]=2

            # 第四行：  目标
            # 4th line：  Storage locations
            fourthLine = next(f).strip('\n')
            currline = fourthLine.split(" ")
            nStorageLocations = int(currline[0])
            for i in range(nStorageLocations):
                currRow = int(currline[2*i+1])-1
                currColumn = int(currline[2*i+2])-1
                targets.append([currRow,currColumn])
                currMap[currRow][currColumn]=3

            # 第五行：  小人
            # 5th line：  Agent
            fifthLine = next(f).strip('\n')
            currline = fifthLine.split(" ")
            agentRow=int(currline[0])-1
            agentColumn=int(currline[1])-1
            agent=[currRow,currColumn]
            if ([currRow,currColumn] in targets):
                currMap[agentRow][agentColumn] = 6
            else:
                currMap[agentRow][agentColumn] = 4
            break
        # 新建一个 sokobanMap类
        # create a SokobanMap object
        return SokobanMap(walls,boxes,targets,agent,currMap)

def isAllTarget(Sokoban : SokobanMap):
    boxes=Sokoban.getBoxPositions()
    targets=Sokoban.getStorageLocation()
    for box in boxes:
        if not(box in targets):
            return False
    return True

def isDeadLock(Sokoban : SokobanMap):
    currMap=Sokoban.getCurrMap()
    boxes=Sokoban.getBoxPositions()
    #http://www.sokobano.de/wiki/index.php?title=Deadlocks
    # Dead square deadlocks
    # Freeze deadlocks
    for i in range(len(boxes)):
        boxRow=boxes[i][0]
        boxColumn=boxes[i][1]
        if (currMap[boxRow][boxColumn] == 5):
            continue
        up=currMap[boxRow-1][boxColumn]
        up=(up == 1) or (up == 2) or (up == 5)
        right=currMap[boxRow][boxColumn+1]
        right=(right == 1) or (right == 2) or (right == 5)
        down=currMap[boxRow+1][boxColumn]
        down=(down == 1) or (down == 2) or (down == 5)
        left=currMap[boxRow][boxColumn-1]
        left=(left == 1) or (left == 2) or (left == 5)
        if (up and right) or (right and down) or (down and left) or (left and up):
            return True
    # Corral deadlocks
    # Closed diagonal deadlocks
    # Bipartite deadlocks
    # Deadlocks due to frozen boxes
    return False

def loadMapFromVisualRepresentationTxt(fileName):
    with open("./inputTxt/"+fileName+".txt","r") as f:
        maxlength=-1;
        walls=[]
        boxes=[]
        targets=[]
        currMap=[]
        lineCt=-1
        for line in f:
            lineCt=lineCt+1
            currLineMap=[]
            currLine = line.strip('\n')
            if (len(currLine)>maxlength):
                maxlength=len(currLine)
            for i in range(len(currLine)):
                currStr=currLine[i]
                if (currStr == " "):
                    currLineMap.append(0)
                elif (currStr == "#"):
                    currLineMap.append(1)
                    walls.append([lineCt,i])
                elif (currStr == "."):
                    currLineMap.append(3)
                    targets.append([lineCt,i])
                elif (currStr == "@"):
                    currLineMap.append(4)
                    agent=[lineCt,i]
                elif (currStr == "$"):
                    currLineMap.append(2)
                    boxes.append([lineCt,i])
                elif (currStr == "V"):
                    currLineMap.append(5)
                    boxes.append([lineCt,i])
                    targets.append([lineCt,i])
                elif (currStr == "O"):
                    currLineMap.append(6)
                    agent=[lineCt,i]
                    targets.append([lineCt,i])
                else:
                    print("Wrong format.")
                    return None
            currMap.append(currLineMap)
    for i in range(len(currMap)):
        for j in range(maxlength-len(currMap[i])):
            currMap[i].append(0)
    currMap=np.array(currMap)
    return SokobanMap(walls, boxes, targets, agent, currMap)

def showMap(currMap):
#map中数值含义：      0:空白    1：墙     2：箱子位置    3：箱子目标    4：小人    5:箱子在目标上    6:小人在目标上
#map values：      0:null    1：wall     2：box    3：storage location    4：agent    5:box in storage   6:agent on storage
    for row in range(currMap.shape[0]):
        currStr=""
        for col in range(currMap.shape[1]):
            curr=currMap[row][col]
            if (curr == 0):
                currStr=currStr+" "
            elif(curr == 1):
                currStr=currStr+"#"
            elif(curr == 2):
                currStr=currStr+"$"
            elif(curr == 3):
                currStr=currStr+"."
            elif(curr == 4):
                currStr=currStr+"@"
            elif(curr == 5):
                currStr=currStr+"V"
            elif(curr == 6):
                currStr=currStr+"O"
            else:
                currStr=currStr+"*"
        print(currStr)
    print("")
    return "Successfully printed map."

def GenerateMap(map_width,map_height,num_of_chests,num_of_moves):
    # map width, map height, num of box, num of move step
    temp_map, temp_level_name = generate_map(map_width=map_width, map_height=map_height,
                                                         num_of_chests=num_of_chests, num_of_moves=num_of_moves)
    Sokoban_map = loadMapFromVisualRepresentationTxt(temp_level_name[:-4])
    return Sokoban_map



def Map2Png(currMap):
    #map中数值含义：      0:空白    1：墙     2：箱子位置    3：箱子目标    4：小人    5:箱子在目标上    6:小人在目标上
#map values：      0:null    1：wall     2：box    3：storage location    4：agent    5:box in storage   6:agent on storage
    TotalMap = Image.new('RGB', [45*currMap.shape[0],45*currMap.shape[1]], color=0)
    pic0 = Image.open('./picture/0'+'.png')
    pic1 = Image.open('./picture/1'+'.png')
    pic2 = Image.open('./picture/2'+'.png')
    pic3 = Image.open('./picture/3'+'.png')
    pic4 = Image.open('./picture/4'+'.png')
    pic5 = Image.open('./picture/5'+'.png')
    for row in range(currMap.shape[0]):
        currStr=""
        for col in range(currMap.shape[1]):
            curr=currMap[row][col]
            if (curr == 0):
                TotalMap.paste(pic0, [45*col,45*row], mask = None)
            elif(curr == 1):
                TotalMap.paste(pic1, [45*col,45*row], mask = None)
            elif(curr == 2):
                TotalMap.paste(pic2, [45*col,45*row], mask = None)
            elif(curr == 3):
                TotalMap.paste(pic3, [45*col,45*row], mask = None)
            elif(curr == 4):
                TotalMap.paste(pic4, [45*col,45*row], mask = None)
            elif(curr == 5):
                TotalMap.paste(pic5, [45*col,45*row], mask = None)
            else:
                TotalMap.paste(pic4, [45*col,45*row], mask = None)
            
        print(currStr)
    return TotalMap
    return "Successfully map2png."

def Png2Gif(gif_images,path):
    gif_images.append(gif_images[len(gif_images)-1])
    imageio.mimsave(path+'Sokoban.gif', gif_images, duration=1)