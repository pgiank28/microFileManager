from __future__ import division
import os
import util
import subprocess
import magic

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

    def getSizeInMB(self,sz):
        siz = sz/(1024*1024)
        return float("%.2f" % siz)

    def getTypeOfFile(self,name):
        if(os.access(self.path,os.R_OK)):
            mime = magic.Magic(mime=True)
            return mime.from_file(self.path).split('/')[1]
        else:
            return "Permission denied"

    def execute(self):
        args = ('/usr/bin/xdg-open',self.path)
        popen = subprocess.Popen(args, stdout=subprocess.PIPE)

    def access(self):
        if(os.access(self.path,os.W_OK)):
            return 1
        else:
            return 0
