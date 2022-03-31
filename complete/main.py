import time
import pandas as pd

FILE_PATH= 'data/10_computable_moments.txt'
#FILE_PATH= 'data/1_binary_landscapes.txt'
# FILE_PATH= 'data/110_oily_portraits.txt'
# FILE_PATH= 'data/110_oily_portraits.txt'
#FILE_PATH= 'data/0_example.txt'
WRITE_PATH = 'output_data/answer10.txt'
NUMBER_OF_FRAMES_PER_GROUP = 1000


def readFile(filePath):
    landscapes = {}
    portraits = {}
    intid = 0
    with open(filePath, 'r') as f:
        for line in f:
            strip_lines = line.strip()
            listli = strip_lines.split()
            if listli[0] == "P":
                portraits[intid] = {'paintId': intid, 'type': listli[0], 'NumofTags': int(listli[1]),'tags': listli[2:]}
                intid = intid + 1
            elif listli[0] == "L":
                landscapes[intid] = {'paintId': intid, 'type': listli[0], 'NumofTags': int(listli[1]),'tags': listli[2:]}
                intid = intid + 1
    return landscapes,portraits

def sortPaintings(file):
    d_descending = sorted(file.items(), key=lambda kv: kv[1]['NumofTags'], reverse=True)
    landscapes = {}
    for i in d_descending:
        landscapes[i[1]["paintId"]] = {'paintId': i[1]["paintId"], 'type': i[1]["type"], 'NumofTags': i[1]["NumofTags"], 'tags': i[1]["tags"]}
    return landscapes


def mergePortraits(pPaintingsPortraits):
    mergePortrait = {}
    sortPortraits = sortPaintings(pPaintingsPortraits)
    key=[]
    for i in sortPortraits.items():
        key.append(i[1]["paintId"])

    while len(key) > 1:
        first = sortPortraits[key[0]]
        last = sortPortraits[key[-1]]
        newId = str(first["paintId"]) + " " + str(last["paintId"])

        #tags = set(first["tags"] )
        common = set(first["tags"]).intersection(set(last["tags"]))
        merge = set(first["tags"] + last["tags"])
        final =  merge-common
        df = final.union(common)


        mergePortrait[newId] = {'paintId': newId, 'type': first["type"],
                            'NumofTags': int(first["NumofTags"]) + int(last["NumofTags"]),
                            'tags': sorted(df)}

        #TODO no esta haciendo el merge de los tags eliminando los tags en comun

        key.remove(key[0])
        key.remove(key[-1])
    return mergePortrait


def subGrouping(actualDictionary):

    mydict = {}
    countGroups = 0
    curentkey = ""
    for i in actualDictionary.values():
        if countGroups == NUMBER_OF_FRAMES_PER_GROUP:
            countGroups = 0

        if countGroups == 0:
            curentkey = i["paintId"]
            mydict[curentkey] = []
            mydict[curentkey].append(i)
        else:
            mydict[curentkey].append(i)
        countGroups = countGroups + 1
    return mydict

# Function that returns the robotic satisfaction
def minvalue(set1, set2):
    common = len(set(set1).intersection(set2))
    return min(len(set1)-common, common, len(set2)-common)


# This method will sort all the frames of a key maximazing the robot satisfaction
def sortDictionary(arrayOfFrames):
    data = []
    total = 0

    data.append(arrayOfFrames[0])
    del arrayOfFrames[0]

    # Loop to search all the frames.
    for i in range(len(arrayOfFrames)):
        numMaximunIntersection = 0
        nextFrame = []

        # loop to compare the actual frame with all of the others remaining
        for j in arrayOfFrames:


            min = minvalue(set(data[i]["tags"]), set(j["tags"]))

            if numMaximunIntersection==0:
                nextFrame = j


            # Check which frame its the best to compare with
            if min > numMaximunIntersection:
                nextFrame = j
                numMaximunIntersection = min

        data.append(nextFrame)
        total = total + numMaximunIntersection
        arrayOfFrames.remove(nextFrame)

    print("Local Score", total)
    return data, total


# This method will sort all the dictionary
def sortFramesArray(frameDict,longitud):
    f = open(WRITE_PATH, "w+")
    f.write(str(longitud))
    f.write('\n')
    globalScore = 0

    # sort all the values of every key in a dictionary.
    for key in frameDict:

        print("Key", key)
        print("number of frames", len(frameDict[key]))

        answer = sortDictionary(frameDict[key])
        sortedArray = answer[0]
        globalScore = globalScore + answer[1]

        for frame in sortedArray:
            f.write(str(frame["paintId"]))
            f.write('\n')

        # we could do multitheading here.

    print("The global Score is", globalScore)
    f.close

# Press the green button in the gutter to run the script.
if __name__ == '__main__':

    start_time = time.time()
    #Read the file
    list = readFile(FILE_PATH)



    #Check if theres portraits
    # landscapes = list [0]
    # portraits = list [1]
    framesWithPortraits={}
    if len(list[1])!=0:
        # We will need to order portraits
        framesWithPortraits = mergePortraits(list[1])
        print(framesWithPortraits)

    frames = {**list[0], **framesWithPortraits}


    #Now we will divide into subgroups
    groupingElements = subGrouping(sortPaintings(frames))

    # In this part we are going to compare the output
    sortFramesArray(groupingElements,len(frames))

    print(len(list[0])+len(list[1]))
    print(len(frames))
    print("--- %s seconds ---" % (time.time() - start_time))


    dataset_raw = pd.read_csv(WRITE_PATH)
    print(dataset_raw.head(5))
    print("lenght",len(dataset_raw))
    print("Duplicates",dataset_raw.duplicated().sum())

