from __future__ import division
import os
import util

class files:
    def __init__(self,name,path,hid):
        self.name = name
        self.path = path
        self.hidden = hid
        stats = os.stat(path)
        self.size = self.getSizeInMB(stats.st_size)
        self.mask = util.getPrivileges(stats.st_mode)
        self.lastUsed = util.convertDate(stats.st_atime)
        self.lastModified = util.convertDate(stats.st_mtime)
        self.type = self.getTypeOfFile(stats.st_mode)

    def getSizeInMB(self,sz):
        siz = sz/(1024*1024)
        return float("%.2f" % siz)

    def getTypeOfFile(self,msk):
        return bin(msk)[2:9]
