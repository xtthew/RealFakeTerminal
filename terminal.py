import re
from directory import directory as _dir2
import subprocess as sp

def prompt(userName, startingDir):
    currentDir = startingDir
    gameInProgress = 1
    while gameInProgress != 0:
        userInput = input(userName.lower()+":"+currentDir+"$ ")
        cmdOutput = user_input(userInput, currentDir)
        if cmdOutput:
            if re.search(r"^cd", cmdOutput):
                currentDir = cmdOutput.split(' ')[1]
            if cmdOutput == "Bad":
                print("Invalid Operation")

def user_input(userInput, currentDir):
    #userInput = userInput.lower()
    strList = userInput.split(' ')
    #tutorial
    if userInput == "tutorial":
        tutorial()
    #help
    elif re.search(r"^help", userInput):
        helpCommand(strList[1]) if len(strList) == 2 else helpCommand("allCommands")
    #cd
    elif re.search(r"^cd", userInput):
        return cdCommand(userInput, currentDir, strList)
    #clear
    elif re.search(r"^clear", userInput) and len(userInput) == 5:
        sp.call('clear',shell=True)
    #ls
    elif re.search(r"^ls", userInput):
        return lsCommand(userInput, currentDir)
    #cat
    elif re.search(r"^cat", userInput):
        return catCommand(userInput, currentDir, strList)
    #mkdir
    elif re.search(r"^mkdir", userInput):
        return mkdirCommand(userInput, currentDir, strList)
    #printalldir
    # elif re.search(r"^printalldir", userInput): #This is just for testing. Shouldn't be here uncommented
    #     print(_dir2.folders)
    #rm
    elif re.search(r"^rm", userInput):
        return rmCommand(userInput, currentDir, strList)
    else:
        return "Bad"

def tutorial():
    print("-----TUTORIAL-----")
    
def helpCommand(command):
    print("------------")
    if command != "allCommands":
        if command == "cd":
            print("Use: cd [DIRECTORY]\n")
            print("The 'cd' command (Short for Change Directories) is a command that is used to change directories (folders). Use this command to navigate between different directories in the Operating System\n")
            print("Tips:\n\t-Go to the Root Directory with 'cd /'\n\t-Go to your User (Home) Directory with 'cd ~'\n\t-To go back/up a directory, use 'cd ..'\n\t-Your current directory is shown after your username")
            print("\n")
        elif command == "ls":
            print("Use: ls [OPTIONS(optional)]\n")
            print("The 'ls' command is used to List Directory Contents. Use this commands to see which files and folders (directories) are inside the current folder that you are in.\n")
            print("Options:\n\t-a\tShows all Files, including hidden files/folders.\n\t--all\tSimilar to '-a'")
            print("Tips:\n\t-When looking for a directory, use 'ls'.\n\t-When looking for a file, use 'ls -a'\n\t-Hidden files/folders start with a '.' \n")
        elif command == "rm":
            print(command+" - Remove Files or Folders")
        elif command == "cat":
            print("Use: cat [DIRECTORY(optional)][FILE_NAME]\n")
            print("The 'cat' command (Short for Concatenate Files) is a command that is used to access the contents of a file and to print them directly into the terminal in a standard format.\n")
            print("Tips:\n\t-To access a file in the directory you are in, just type 'cat' and the filename. (ex: 'cat file.txt')\n\t-If accessing a hidden file, make sure to include the . before the file name.\n\t-To access a file in a different folder use the full file path. (ex: 'cat /home/user/file.txt')")
        elif command == "clear":
            print(command+" - Clears the terminal screen")
        elif command == "mkdir":
            print(command+" - Make a Directory(Folder)")
        else:
            print("There is no command called '"+command+"' to help you with")
    else:
        print("Here's a list of commands you can use:")
        print("\n cd - Change Directories\n ls - List Contents in Directory\n rm - Remove File/Folder\n cat - Show Contents Of File\n clear - Clears The Terminal Screen\n rm - Remove File or Directory")
        print("\nTo get more information on a specific command type: help [command name]\n")

def wgetCommand(userInput, currentDir):
    if re.search(r"^wget\s", userInput):
        print("Using wget")
    else:
        helpCommand("wget")

def lsCommand(userInput, currentDir):
    lsOptions = userInput.split(" ")[1] if re.search(r"^ls\s", userInput) else ''
    currentDir = "/home/user" if currentDir == "~" else currentDir
    currentDir = "/root" if currentDir == "/" else currentDir
    files = []
    folders = []
    #getFiles
    for x in _dir2.files:
        if _dir2.files[x]["folder"] == currentDir:
            if not re.search(r"^\.", _dir2.files[x]["name"]):
                files.append(_dir2.files[x]["name"])
            else:
                if re.search(r"^\-a$|^\-\-all$", lsOptions):
                    files.append(_dir2.files[x]["name"])
    #getDirs
    dirs = currentDir.split('/')
    if currentDir == "/root":
        dirs = dirs[1:]
    else:
        dirs[0] = "root"
    def listDirs(di=None):
        for k in di:
            folders.append("\033[1;32;40m"+k+"\033[0m ")
    def getDirs(di=None, index=0):
        for k in di:
            if k == dirs[index]:
                index += 1
                if index == len(dirs):
                    listDirs(di[k])
                    break
                if di[k]:
                    return getDirs(di[k], index)
    getDirs(_dir2.folders)
    if len(dirs) != 0:
        files.extend(folders)
    files.sort()
    for x in files:
        print(x, end =" ")
    print("") # End Line

def cdCommand(userInput, currentDir, strList):
    if re.search(r"^cd\s", userInput):
        toDirectory = strList[1]
        if toDirectory == "/": #if going to root, just go.
            return userInput
        elif re.search(r"^/", toDirectory): #if start with /
            if re.search(r"/$", toDirectory):
                userInput = userInput[:-1]
                toDirectory = toDirectory[:-1]
            dirs = toDirectory.split('/')
            dirs[0] = "root"
            def checkDirs(di=None, index=0, pathGood=None):
                for k in di:
                    if k == dirs[index]:
                        index += 1
                        pathGood = True
                        if index == len(dirs):
                            return pathGood
                        if di[k]:
                            return checkDirs(di[k], index, pathGood)
            cdPath = userInput if checkDirs(_dir2.folders) else "Bad"
            return cdPath
        elif re.search(r"^\.\.", toDirectory): # if ..
            if currentDir == "/":
                return "Bad"
            currentDir = "/home/user" if currentDir == "~" else currentDir
            dirs = currentDir.split("/")[1:-1]
            newDir = "/"
            for i in dirs:
                newDir = newDir+i+"/"
            return "cd /" if newDir == "/" else "cd "+re.sub(r"/$", '', newDir)
        else: #go from current dir
            currentDir = "/home/user" if currentDir == "~" else currentDir
            if re.search(r"/$", strList[1]): #remove ending / if exists
                toDirectory = toDirectory[:-1]
            dirs = (currentDir.split('/')+toDirectory.split('/'))[1:] #create directory
            if currentDir == "/":
                dirs[0] = "root"
            else:
                r = ["root"]
                dirs = r + dirs
            def checkDirs(di=None, index=0, pathGood=None):
                for k in di:
                    if k == dirs[index]:
                        index += 1
                        pathGood = True
                        if index == len(dirs):
                            return pathGood
                        if di[k]:
                            return checkDirs(di[k], index, pathGood)
            cdPath = "cd /"+toDirectory if currentDir == "/" else "cd "+currentDir+"/"+toDirectory
            cdPath = cdPath if checkDirs(_dir2.folders) else "Bad"
            return cdPath
    else:
        helpCommand(userInput)
def catCommand(userInput, currentDir, strList): 
    fileDir = currentDir
    if not re.search(r"^cat\s", userInput):
        helpCommand("cat")
    else:
        if re.search(r"/", strList[1]):
            fileName = strList[1].split('/')[-1:][0]
            if not re.search(r"^/",strList[1]):
                currentDir = "" if currentDir == "/" else currentDir
                strList[1] = currentDir+"/"+strList[1]
            dirs = strList[1].split('/')[1:-1]
            if not dirs:
                dirs.append("root")
            fileDir = ""
            for x in dirs:
                fileDir = fileDir+"/"+x
        else:
            fileDir = "/root" if fileDir== "/" else fileDir
            fileDir = "/home/user" if fileDir == "~" else fileDir
            fileName = strList[1]
        for x in _dir2.files:
            if _dir2.files[x]["folder"] == fileDir:
                if _dir2.files[x]["name"] == fileName:
                    try:
                        print(_dir2.files[x]["content"])
                    except:
                        print("")
def mkdirCommand(userInput, currentDir, strList):
    if re.search(r"^mkdir\s", userInput):
        if re.search(r"^/", strList[1]):
            strList[1] = strList[1][:-1] if re.search(r"/$", strList[1]) else strList[1]
            newDir = strList[1].split('/')[-1:]
            dirs = strList[1].split('/')[:-1]
            dirs[0] = "root"
        else:
            strList[1] = strList[1][:-1] if re.search(r"/$", strList[1]) else strList[1]
            newDir = strList[1].split('/')[-1:]
            dirs = strList[1].split('/')[:-1]
            currentDir = "/home/user" if currentDir == "~" else currentDir
            currDirs = currentDir.split('/')
            dirs = currDirs+dirs
            dirs[0] = "root"
            if currentDir == '/':
                dirs = [dirs[0]]

        def checkDirs(di=None, index=0, pathGood=None):
            for k in di:
                if k == dirs[index]:
                    index += 1
                    pathGood = True
                    if index == len(dirs):
                        return pathGood
                    if di[k]:
                        return checkDirs(di[k], index, pathGood)
        if checkDirs(_dir2.folders):
            def createDir(di=None, index=0, folderName = None):
                for k in di:
                    if k == dirs[index]:
                        index += 1
                        if index == len(dirs):
                            di[k][str(newDir[0])] = {}
                            break
                        if di[k]:
                            return createDir(di[k], index, folderName)
            createDir(_dir2.folders)
    else:
        return helpCommand("mkdir")
def rmCommand(userInput, currentDir, strList):
    if re.search(r"^rm\s", userInput):
        if len(strList) == 2: #remove file
            currentDir = "/root" if currentDir == "/" else currentDir
            currentDir = "/home/user" if currentDir == "~" else currentDir
            if strList[1].find('/') == -1: #if file in local dir
                fileName = strList[1]
                for x in _dir2.files:
                    if _dir2.files[x]["name"] == fileName and _dir2.files[x]["folder"] == currentDir:
                        _dir2.files.pop(x, None)
                        break
            elif strList[1].find('/') != -1: #if file in ANOTHER dir
                dirs = strList[1].split('/')[:-1] if re.search(r"^/", strList[1]) else currentDir.split('/')+strList[1].split('/')[:-1]
                fileName = strList[1].split('/')[-1:][0]
                dirs[0] = "root"
                dirs = dirs[1:] if dirs[1] == "root" else dirs
                def checkDirs(di=None, index=0, pathGood=None):
                    for k in di:
                        if k == dirs[index]:
                            index += 1
                            pathGood = True
                            if index == len(dirs):
                                return pathGood
                            if di[k]:
                                return checkDirs(di[k], index, pathGood)
                if checkDirs(_dir2.folders):
                    dirs = dirs[1:] if len(dirs) >= 2 else dirs
                    fileDir = ''
                    for x in dirs:
                        fileDir += "/"+x
                    for x in _dir2.files:
                        if _dir2.files[x]["name"] == fileName and _dir2.files[x]["folder"] == fileDir:
                            _dir2.files.pop(x, None)
                            break
        else:
            print("Remove Folder")
    else:
        helpCommand("rm")

def touchCommand(userInput, currentDir, strList):
    print("touch files")