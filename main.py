import gc

class Frame:
    # Function to initialize the node object
    def __init__(self, id ,tagsLength, frameType, data):
        
        self.id : str = id
        self.tagsLength : str = tagsLength  #Assing id
        self.frameType : str = frameType # Assing tags
        self.tags = data  # Assign data
        self.next = None  # Initialize
        self.prev = None # Initialize

class LinkedList:
    # Function to initialize head
    def __init__(self):
        self.head : Frame = None
        self.count = 0 # number of nodes

    def push(self, frame : Frame):
        frame.next = self.head
        if self.head is not None:
             self.head.prev = frame
        self.head = frame
        self.count += 1

    def deleteNode(self, dele):
        if self.head is None or dele is None:
            return
        if self.head == dele:
            self.head = dele.next
        if dele.next is not None:
            dele.next.prev = dele.prev
        if dele.prev is not None:
            dele.prev.next = dele.next
        gc.collect()
        self.count -= 1

    def writeResultToFile(self, filePath):
        with open(filePath, 'w') as f:
            f.write(str(self.count)+"\n")
            printval = self.head
            while printval is not None:
                f.write(printval.frameType +" " + str(printval.id) + " " + " ".join(map(str, printval.tags)) + "\n")
                printval = printval.next

    # function to find the most similar node from a linkedList for a given node
    def getMostSimilarFrame(self, node : Frame, node1):
        temp : Frame = node
        percentage = 0
        while (node is not None):
            c= len(node.tags.intersection(node1.tags))
            if c != 0:
                n1 = len(node.tags)
                n2 = len(node1.tags)
                n = n1 if n1 > n2 else n2
                simalartyPercent = c/n*100
                if (percentage < simalartyPercent):
                    temp = node
                    percentage = simalartyPercent
            node = node.next
            if(percentage == 100.0):
                break
        # Simalarity percentage : make it better
        #print(percentage)
        return temp

def GetFinalGallery(Gallery : LinkedList):
    FinalGalery : LinkedList = LinkedList()
    FinalGalery.push(Frame(Gallery.head.id,Gallery.head.tagsLength, Gallery.head.frameType, Gallery.head.tags))
    Gallery.head = Gallery.head.next
    while Gallery.head is not None:
        # implement sort function to rearrange the list
        Result = Gallery.getMostSimilarFrame(Gallery.head, FinalGalery.head)
        FinalGalery.push(Frame(Result.id, Result.tagsLength, Result.frameType, Result.tags))
        Gallery.deleteNode(Result)
    return FinalGalery

def ReadFramesFromFile(filePath):
    Gallery :LinkedList = LinkedList()
    f = open(filePath, 'r')  # 'r' = read
    lines = f.readlines()
    f.close()
    count: int = int(lines[0])  # number of images
    lines.remove(lines[0])
    tempFrame: Frame = None
    imgCount = 0
    for l in lines:
        l = l.replace("\n", "")
        list = l.split(" ")
        if (list[0] == "P"):
            if (tempFrame == None):
                tempFrame = Frame(imgCount ,list[1], list[0], set(list[2:]))
            else:
                tempFrame.tags.update(set(list[2:]))
                tempFrame = Frame(str(tempFrame.id)+ " " + str(imgCount), len(tempFrame.tags), tempFrame.frameType, tempFrame.tags)
                Gallery.push(tempFrame)
                tempFrame = None
        else:
            Gallery.push(Frame(imgCount,list[1], list[0], set(list[2:])))
        imgCount += 1
    return Gallery
# Press the green button in the gutter to run the script.
if __name__ == '__main__':

    Gallery :LinkedList = ReadFramesFromFile('./inputFiles/10_computable_moments.txt')
    FinalGalery : LinkedList = GetFinalGallery(Gallery)
    filePath = "./inputFiles/10_computable_moments_output.txt"
    FinalGalery.writeResultToFile(filePath)


