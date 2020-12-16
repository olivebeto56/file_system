# File system


### Hard driver structure
- Boot block - 1k
- Super block - 2k
- inode list - 16k (256 inodes, LIL len 64) 
- block list - 256k (LBL len 256)

### Usage
Just run this command:

`python3 User_interface.py`

If you want to clean all the data run:

`python3 Hard_drive_helper.py`
  

### Commands

| Command       | Parameters    | Description    |
| ------------- | ------------- | ------------- |
| exit  | exit  | Close progam  |
| ls  | ls  | Print directories and files with their inode id  |
| pwd  | pwd  | Print current path  |
| mkdir  | mkdir {dir_name}  | Create new directory  |
| mkfile  | mkfile {file_name} {content}  | Create file  |
| openfile  | openfile {file_name}  | Open file  |
| rmfile  | rmfile {file_name}  | Delete file  |
| cd  | cd {dir_name}  | Move between directories  |
| help  | help  | Print help  |
