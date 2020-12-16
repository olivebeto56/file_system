import datetime


class Hard_drive_helper:
    inodeStarByte = 3072
    inodeSize = 64

    datablockStarByte = 19456
    blockSize = 1024

    def __init__(self):
        pass

    # This method restore and clean all data
    def initDisk(self):
        f = open("HARD_DRIVE", "w")

        #Init BootBlock
        f.write("Start boot block ")
        f.seek(1010)
        f.write("End boot block")

        #Init SuperBlock
        f.write("Start super block ")
        f.seek(3057)
        f.write("End super block")

        #Init inodeList
        f.seek(self.inodeStarByte)
       
        for i in range(256):
            if(i == 0 or i == 1):
                inode = f.write("f,"+str(i+1)+",date,{},")
            else:
                inode = f.write("0,"+str(i+1)+",date,{},")

            f.seek(self.inodeStarByte+((i+1)*self.inodeSize))

        
        #Init data block
        f.seek(self.datablockStarByte)
       
        inode = f.write(''.ljust(self.blockSize*256, chr(0)))

        #create root folder
        inodeRoot = {}
        inodeRoot["status"] = 'd'
        inodeRoot["id"] = 3
        inodeRoot["date"] = self.getDateStr()
        inodeRoot["blocks"] = '{1}'

        blockRoot = "3:.,3:..,4:home,"

        self.updateInode(inodeRoot)
        self.updateBlock(1,blockRoot)

        # create home folder
        inodeHome = {}
        inodeHome["status"] = 'd'
        inodeHome["id"] = 4
        inodeHome["date"] = self.getDateStr()
        inodeHome["blocks"] = '{2}'

        blockHome = "4:.,3:..,"

        self.updateInode(inodeHome)
        self.updateBlock(2,blockHome)

        f.close()

    def getDateStr(self):
        now = datetime.datetime.now()
        return now.strftime("%Y-%m-%d %H:%M:%S")

    def printBootBlock(self):
        f = open("HARD_DRIVE", "r")
        print(f.read(1024))
        f.close()

    def printSuperBlock(self):
        f = open("HARD_DRIVE", "r")
        f.seek(1024)
        print(f.read(2048))
        f.close()


    def getBlock(self,blockId):
        offsetStart = self.datablockStarByte+ ((blockId-1)*self.blockSize)
        f = open("HARD_DRIVE", "r")
        
        f.seek(offsetStart)
        block = f.read(self.blockSize)
        return block

    def updateBlock(self,blockId, data):
        offsetStart = self.datablockStarByte+ ((blockId-1)*self.blockSize)
        f = open("HARD_DRIVE", "r+")
        
        f.seek(offsetStart)
        blockText = data.ljust(self.blockSize, chr(0))
        block = f.write(blockText)

    def getInode(self,inodeId):
        offsetStart = self.inodeStarByte+ ((inodeId-1)*self.inodeSize)
        f = open("HARD_DRIVE", "r")
        
        f.seek(offsetStart)
        inode = f.read(self.inodeSize)

        inode = inode.split(',')
        inodeObject = {}
        inodeObject["status"] = inode[0]
        inodeObject["id"] = int(inode[1])
        inodeObject["date"] = inode[2]
        inodeObject["blocks"] = inode[3]


        return inodeObject

    def updateInode(self, inodeObject):
        inodeId = inodeObject['id']
        offsetStart = self.inodeStarByte+ ((inodeId-1)*self.inodeSize)
        
        f = open("HARD_DRIVE", "r+")
        f.seek(offsetStart)
        
        inodeText = inodeObject['status']+","+str(inodeId)+","+inodeObject['date']+","+inodeObject['blocks']+","

        inodeText = inodeText.ljust(self.inodeSize, chr(0))
        inode = f.write(inodeText)

    def getFreeInodes(self):
        inodesFree = []
        f = open("HARD_DRIVE", "r")
        f.seek(self.inodeStarByte)
        for i in range(256):
            inode = f.read(self.inodeSize)
            if(inode[0] == "0"):
                inodesFree.append(i+1)
        f.close()

        return inodesFree
    
    def getBusyInodes(self):
        inodesBusy = []
        f = open("HARD_DRIVE", "r")
        f.seek(self.inodeStarByte)
        for i in range(256):
            inode = f.read(self.inodeSize)
            if(inode[0] != "0"):
                inodesBusy.append(i+1)
        f.close()

        return inodesBusy

    def getBusyBlock(self):
        blockBusy = []
        f = open("HARD_DRIVE", "r")
        f.seek(self.inodeStarByte)
        for i in range(256):
            inode = f.read(self.inodeSize)
            
            indexl = inode.find("{")+1
            indexr = inode.rfind("}")
            blocks = inode[indexl:indexr]
            blocksArray = blocks.split(";")
            if(blocksArray[0] != ''):
                for v in blocksArray:
                    blockBusy.append(v)
        f.close()

        return blockBusy
    
    def getFreeBlock(self):
        busyBlock = self.getBusyBlock()

        blocks = [i+1 for i in range(256)]

        for v in busyBlock:
            index = blocks.index(int(v))
            del blocks[index]
        
        
        return blocks

def main():
    #Clean disk
    hard_drive_helper = Hard_drive_helper()
    hard_drive_helper.initDisk()

if __name__ == "__main__":
    main()