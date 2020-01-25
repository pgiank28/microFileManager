from __future__ import division
import os
import util
import subprocess

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
        self.type = self.getTypeOfFile(name)
        self.opensWith = list()

    def getSizeInMB(self,sz):
        siz = sz/(1024*1024)
        return float("%.2f" % siz)

    def getTypeOfFile(self,name):
        ftype = name.split('.')
        if len(ftype) == 1:
            return "Binary file"

        if ftype[-1] in util.fileTypes:
            return util.fileTypes[ftype[-1]]
        else:
            return "Unknown type"

    def execute(self):
        args = ('/usr/bin/evince',self.path)
        popen = subprocess.Popen(args, stdout=subprocess.PIPE)
