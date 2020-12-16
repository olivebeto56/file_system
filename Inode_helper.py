
# INODE STRUCTURE
# status,id,date,datablocks

#status = {0 -> free, d -> dir, f -> file}
#id = int
#date = pending
#datablocks = {blockId;blockId; ...}


from Hard_drive_helper import Hard_drive_helper
from Block_helper import Block_helper
import math

class Inode_helper:
    LIL = []
    hard_drive_helper = Hard_drive_helper()
    block_helper = Block_helper()

    def __init__(self):
        global hard_drive_helper
        global LIL

        hard_drive_helper = Hard_drive_helper()
        
        # borrar
        # hard_drive_helper.initDisk()
        
        LIL = hard_drive_helper.getFreeInodes()[0:64]

    def getInodeDirs(self, inodeId):
        inode = hard_drive_helper.getInode(inodeId)
        arrayBlocks = inode['blocks'].replace('{', '').replace('}', '').split(';')
        
        content = hard_drive_helper.getBlock(int(arrayBlocks[0]))
        result = {}
        content = content.split(',')[:-1]

        for dirs in content:
            entities = dirs.split(':')
            result[entities[1]] = entities[0] 

        return result

    def getInodeContent(self, inodeId):
        inode = hard_drive_helper.getInode(inodeId)
        arrayBlocks = inode['blocks'].replace('{', '').replace('}', '').split(';')

        if(inode['status'] == 'd'):
            content = hard_drive_helper.getBlock(int(arrayBlocks[0]))
            result = ''
            content = content.split(',')[:-1]
            for dirs in content:
                entities = dirs.split(':')
                result += entities[0] + '  ' + entities[1] + '\n'

            return result
            
        elif(inode['status'] == 'f'):
            content = ''
            for i in arrayBlocks:
                content += hard_drive_helper.getBlock(int(i))
            return content
        else:
            return ''
       
    def getInode(self):
        global LIL
        inodeId = LIL[0]

        del LIL[0]

        if(len(LIL)==0):
            LIL = hard_drive_helper.getFreeInodes()[hard_drive_helper.getFreeInodes().index(inodeId)+1:hard_drive_helper.getFreeInodes().index(inodeId)+1+64]
            
        return inodeId
    
    def freeAnInode(self, inodeId):
        global LIL

        if(len(LIL) == 64):
            if(inodeId < LIL[len(LIL)]):
                del LIL[len(LIL)]
                LIL.append(inodeId)            
        else:
            LIL.insert(0,inodeId)
    
    def deleteFile(self, inodeId, parentInode):
        global hard_drive_helper

        inodeStructure = {}
        inodeStructure["status"] = '0'
        inodeStructure["id"] = inodeId
        inodeStructure["date"] = 'date'
        inodeStructure["blocks"] = '{}'
        hard_drive_helper.updateInode(inodeStructure)

        parentInode = hard_drive_helper.getInode(parentInode)

        blockId = parentInode["blocks"].replace('{','').replace('}','')

        dirFiles = hard_drive_helper.getBlock(int(blockId)).split(',')[:-1]
        blockContent = ''
        for dirFile in dirFiles:
            if int(dirFile.split(':')[0]) != inodeId:
                blockContent += dirFile+','
        
        hard_drive_helper.updateBlock(int(blockId), blockContent)

        self.freeAnInode(inodeId)



    def createFile(self, inodeId, name, content):
        global hard_drive_helper

        newInodeId = self.getInode()

        nBlocks =  math.ceil(len(content)/1024)


        blockInfoSeparated = [content[i:i+1024] for i in range(0, len(content), 1024)]

        blocks = ''
        for i in range(nBlocks):
            newBlockId = self.block_helper.getBlock()

            hard_drive_helper.updateBlock(newBlockId,blockInfoSeparated[i])

            if(blocks != ''):
                blocks += ';'
            blocks += str(newBlockId)
        
        inodeStructure = {}
        inodeStructure["status"] = 'f'
        inodeStructure["id"] = newInodeId
        inodeStructure["date"] = hard_drive_helper.getDateStr()
        inodeStructure["blocks"] = '{'+blocks+'}'

        hard_drive_helper.updateInode(inodeStructure)


        # aqui_beto -> agregar en el directorio padre 'inodeId'
        parentInode = hard_drive_helper.getInode(inodeId)
        blockId = parentInode["blocks"].replace('{','').replace('}','')
        
        parentBlock = hard_drive_helper.getBlock(int(blockId))
        parentBlock = parentBlock[:1+parentBlock.rfind(',')]+str(newInodeId)+":"+name+','
        
        hard_drive_helper.updateBlock(int(blockId), parentBlock)



    def createDir(self, name, inodeId):
        global hard_drive_helper

        newInodeId = self.getInode()
        newBlockId = self.block_helper.getBlock()

        inodeStructure = {}
        inodeStructure["status"] = 'd'
        inodeStructure["id"] = newInodeId
        inodeStructure["date"] = hard_drive_helper.getDateStr()
        inodeStructure["blocks"] = '{'+str(newBlockId)+'}'


        hard_drive_helper.updateInode(inodeStructure)

        blockRoot = str(newInodeId)+":.,"+str(inodeId)+":..,"
        hard_drive_helper.updateBlock(newBlockId,blockRoot)

        # aqui_beto -> agregar en el directorio padre 'inodeId'
        parentInode = hard_drive_helper.getInode(inodeId)
        blockId = parentInode["blocks"].replace('{','').replace('}','')

        parentBlock = hard_drive_helper.getBlock(int(blockId))
        parentBlock = parentBlock[:1+parentBlock.rfind(',')]+str(newInodeId)+":"+name+','
        
        hard_drive_helper.updateBlock(int(blockId), parentBlock)


    
def main():
    pass
    #some test
    # inode_helper = Inode_helper()
    # print(inode_helper.getInodeContent(3))
  


if __name__ == "__main__":
    main()