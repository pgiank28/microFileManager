from __future__ import division
import os
import files
import util
import shutil

class directory:

    def __init__(self,pth,nm,par,hid):
        self.path = pth
        self.name = nm
        self.directories = dict()
        self.files = dict()
        self.parent = par
        self.hidden = hid
        self.size = 4096
        stats = os.stat(pth)
        self.mask = util.getPrivileges(stats.st_mode)
        self.lastUsed = util.convertDate(stats.st_atime)
        self.lastModified = util.convertDate(stats.st_mtime)
        self.type = 'Folder'

    def addFile(self,fle,hid):
        self.files[str(fle)] = files.files(str(fle),self.path+'/'+str(fle),hid)

    def addDirectory(self,dir,hid):
        if self.path == '/':
            self.directories[self.path+dir] = directory(self.path+dir,dir,self,hid)
        else:
            self.directories[self.path+'/'+dir] = directory(self.path+'/'+dir,dir,self,hid)

    def addDirectoryFromExternal(self,mc,dir,hid):
        if(os.access(self.path,os.W_OK)):
            self.addDirectory(dir,hid)
            if mc == 'MOVE':
                shutil.move(dir.path,self.path)
            if mc == 'COPY':
                shutil.copytree(dir.path,self.path)

    def createDirectory(self,name):
        os.mkdir(self.path+'/'+name)
        self.addDirectory(name,0)

    def createFile(self,name):
        open(self.path+'/'+name,'a').close()
        self.addFile(name,0)

    def deleteDirectory(self,dir):
        del self.directories[dir.path]

    def deleteFile(self,name):
        del self.files[name]

    def enlistContents(self):
        if(os.access(self.path,os.R_OK)):
            cd = os.listdir(self.path)
        else:
            return

        for item in cd:
            if os.path.isfile(self.path+'/'+str(item)):
                if item.startswith("."):
                    self.addFile(str(item),1)
                    continue
                self.addFile(str(item),0)
            else:
                if item.startswith("."):
                    self.addDirectory(str(item),1)
                    continue
                self.addDirectory(str(item),0)

        self.size = sum(dr.size for dr in self.directories.values()) + sum(f.size for f in self.files.values())
        self.size = "%.2f" % (self.size/(1024*1024))
        self.size = float(self.size)
        if self.parent !=None:
            self.parent.directories[self.path] = self

    def emptyDir(self):
        if len(self.directories) == 0:
            return True
        for i in self.directories.values():
            if i.hidden == 0:
                return False
        return True

    def getNumOfDirectories(self):
        return len(self.directories)

    def getFiles(self):
        return self.files

    def getPath(self):
        return self.path

    def getParentDir(self):
        return self.parent

    def getDirByModifiedDate(self):
        permanentDirs = dict()
        returnedDict =  list()
        for d,val in self.directories.items():
            permanentDirs[util.dateToLongFormat(val.lastModified)] = d
        for dr in sorted(permanentDirs.keys()):
            returnedDict.append(self.directories[permanentDirs[dr]])
        return returnedDict[::-1]

    def getFilesByModifiedDate(self):
        permanentFiles = dict()
        returnedFiles = list()
        for f,val in self.files.items():
            permanentFiles[util.dateToLongFormat(val.lastModified)] = f
        for fr in sorted(permanentFiles.keys()):
            returnedFiles.append(self.files[permanentFiles[fr]])
        return returnedFiles[::-1]

    def getFilesBySize(self):
        permanentFiles = dict()
        returnedFiles = list()
        for f,val in self.files.items():
            permanentFiles[val.size] = f
        for fr in sorted(permanentFiles.keys()):
            returnedFiles.append(self.files[permanentFiles[fr]])
        return returnedFiles[::-1]

    def getDirAlphabetically(self):
        permanentDirs = dict()
        returnedDict =  list()
        for d,val in self.directories.items():
            permanentDirs[val.name] = d
        for dr in sorted(permanentDirs.keys()):
            returnedDict.append(self.directories[permanentDirs[dr]])
        return returnedDict

    def getFilesAlphabetically(self):
        permanentFiles = dict()
        returnedFiles = list()
        for f,val in self.files.items():
            permanentFiles[val.name] = f
        for fr in sorted(permanentFiles.keys()):
            returnedFiles.append(self.files[permanentFiles[fr]])
        return returnedFiles
    def getDirsByOrder(self,ord):
        if ord == 0:
            return self.getDirAlphabetically()
        if ord == 1:
            return self.getDirAlphabetically()
        if ord == 2:
            return self.getDirByModifiedDate()

    def getFilesByOrder(self,ord):
        if ord == 0:
            return self.getFilesAlphabetically()
        if ord == 1:
            return self.getFilesBySize()
        if ord == 2:
            return self.getFilesByModifiedDate()
