from Inode_helper import Inode_helper
path = ''
currentInodeId = 3

def main():
    global path
    global currentInodeId

    inode_helper = Inode_helper()
    
    while(True):
        command = input(path+'/ % ').split(' ')
        
        if(command[0] == 'exit'):
            break
        
        if(command[0] == 'ls'):
            print(inode_helper.getInodeContent(currentInodeId))
            
        if(command[0] == 'pwd'):
            print(path)

        if(command[0] == 'mkdir'):
            inode_helper.createDir(command[1], currentInodeId)

        if(command[0] == 'mkfile'):
            content = ' '.join(command[2:])
            inode_helper.createFile(currentInodeId , command[1], content)

        if(command[0] == 'openfile'):
            fileName = command[1]
            dirs = inode_helper.getInodeDirs(currentInodeId)
            if fileName in dirs:
                fileInodeId = int(dirs[fileName])

                print(inode_helper.getInodeContent(fileInodeId))
            else:
                print('File does not exist')

            pass
        if(command[0] == 'rmfile'):
            fileName = command[1]
            dirs = inode_helper.getInodeDirs(currentInodeId)
            if fileName in dirs:
                fileInodeId = int(dirs[fileName])

                inode_helper.deleteFile(fileInodeId, currentInodeId)
            else:
                print('File does not exist')

            pass
        if(command[0] == 'cd'):
            dirName = command[1]
            dirs = inode_helper.getInodeDirs(currentInodeId)
            if dirName in dirs:
                # aqui_beto -> si tienes tiempo verificar que sea un directorio
                if(dirName == '..'):
                    path = path[:path.rfind('/')]
                elif(dirName != '.'):
                    path += '/'+dirName
                
                currentInodeId = int(dirs[dirName])
            else:
                print('Directory does not exist')

            pass
        
        elif(command[0] == 'help'):
            print("""
    exit     -   exit                           ->    Close progam
    ls       -   ls                             ->    Print directories and files with their inode id
    pwd      -   pwd                            ->    Print current path
    mkdir    -   mkdir {dir_name}               ->    Create new directory
    mkfile   -   mkfile {file_name} {content}   ->    Create file
    openfile -   openfile {file_name}           ->    Open file
    rmfile   -   rmfile {file_name}             ->    Delete file
    cd       -   cd {dir_name}                  ->    Move between directories 

            """)



if __name__ == "__main__":
    main()