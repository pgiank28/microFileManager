import os
import directory
import random

class filesystem:
    mainDir = directory.directory('/','root')

    def __init__(self):
        self.enlistRoot()

    def enlistRoot(self):
        dc = os.listdir('/')

        for i in dc:
            if os.path.isfile('/'+str(i)):
                self.mainDir.addFile(str(i))
            else:
                self.mainDir.addDirectory(directory.directory('/'+str(i),str(i)))

    def getRootDirs(self):
        keys = self.mainDir.directories.keys()

        return keys

    def getRootFiles(self):
        return self.mainDir.files

    def enlistDir(self,path):
        if(os.access(path,os.R_OK)):
            print 'true'
        else:
            return
        print "path is "+path
        pfind = path.split('/')
        cd = directory.directory(path,pfind[-1])

        cv = os.listdir(self.path)
        for d in cv:
            if os.path.isfile(self.path+'/'+str(d)):
                cd.addFile(str(d))
            else:
                cd.addDirectory(directory.directory(self.path+'/'+str(d),d))

        return cd
