from Hard_drive_helper import Hard_drive_helper

class Block_helper:
    LBL = []
    hard_drive_helper = Hard_drive_helper()
    

    def __init__(self):
        global LBL
        hard_drive_helper = Hard_drive_helper()
        LBL = hard_drive_helper.getFreeBlock()

    def getBlock(self):
        global LBL
        idBlock = LBL[0]
        del LBL[0]
        return idBlock

    def freeABlock(self, blockId):
        global LBL
        LIL.insert(0,blockId)

    