import directory
import popularityHeap as ph
import time
from Tkinter import *

class mainWindow(Frame):

    def changeMainDirectory(self,newdir):
        nd = directory.directory(str(self.root.path)+str(newdir),str(newdir))
        nd.enlistContents()
        self.changeFrame()

    def __init__(self):
        Frame.__init__(self)
        self.t0 = time.time()
        self.master.title("Micro File Manager")
        self.master.minsize(1000, 750)
        self.grid(sticky=E+W+N+S)

        self.save_dir = None
        self.filename_open = None

        top = self.winfo_toplevel()
        top.rowconfigure(0, weight=0)

        self.recentDirs = list()
        self.root = directory.directory('/','root',None,0)
        self.root.enlistContents()
        self.popularityHeap = self.initialisePopularDirsHeap()

        self.LeftFrame = Frame()
        self.LeftFrame.grid(sticky=W+E)

        Label(self.LeftFrame,text="GENERAL",bg="#a9a9a9",font="Times 16").grid(row=0,column=0,sticky=N)
        self.drawBasicDirectoriesCanvas().grid(row=1,column=0,sticky=W+E)
        Label(self.LeftFrame,text="RECENT",bg="#a9a9a9",font="Times 16").grid(row=2,column=0,sticky=N,pady=(10,1))
        self.getRecentlyUsedDirs().grid(row=3,column=0,sticky=W+E)
        Label(self.LeftFrame,text="POPULAR",bg="#a9a9a9",font="Times 16").grid(row=4,column=0,sticky=N,pady=(10,1))
        self.getPopularDirs().grid(row=5,column=0,sticky=W+E)
        self.LeftFrame.config(bg='#a9a9a9',bd=2,padx=4,relief=GROOVE)
        self.LeftFrame.grid(row=0,column=0,sticky=W+N+E)

        self.RightFrame = Frame()
        mc = self.drawMainCanvas(self.root,0,0)
        mc[0].grid(row=0,column=1,sticky=W)
        mc[1].grid(column=1,sticky=W+N)
        self.RightFrame.grid(row=0,column=1,sticky=W+N)

    def drawBasicDirectoriesCanvas(self):
        self.basicDirCanvas = Frame(self.LeftFrame)
        self.basicDirCanvas.grid(sticky=E+N+W+S)
        self.basicDirCanvas.config(bg='#a9a9a9')
        for key,dir in self.root.directories.items():
            if key == '/home':
                Button(self.basicDirCanvas,text='HOME',font="Helvetica 10",width=33,command=(lambda dir=dir: self.changeMainCanvas(dir,0,0))).grid(row=0,column=0,sticky=W+N+E+S,padx=(4,4))
            if key == '/bin':
                Button(self.basicDirCanvas,text='BIN',font="Helvetica 10",width=33,command=(lambda dir=dir: self.changeMainCanvas(dir,0,0))).grid(row=1,column=0,sticky=W+E,padx=(4,4))
            if key == '/usr':
                Button(self.basicDirCanvas,text='USR',font="Helvetica 10",width=33,command=(lambda dir=dir: self.changeMainCanvas(dir,0,0))).grid(row=2,column=0,sticky=W+E,padx=(4,4))
            if key == '/var':
                Button(self.basicDirCanvas,text='VAR',font="Helvetica 10",width=33,command=(lambda dir=dir: self.changeMainCanvas(dir,0,0))).grid(row=3,column=0,sticky=W+E,padx=(4,4))
            if key == '/media':
                Button(self.basicDirCanvas,text='MEDIA',font="Helvetica 10",width=33,command=(lambda dir=dir: self.changeMainCanvas(dir,0,0))).grid(row=4,column=0,sticky=W+E,padx=(4,4))
            if key == '/etc':
                Button(self.basicDirCanvas,text='ETC',font="Helvetica 10",width=33,command=(lambda dir=dir: self.changeMainCanvas(dir,0,0))).grid(row=5,column=0,sticky=W+N+E+S,padx=(4,4))

        return self.basicDirCanvas

    def drawMainCanvas(self,dir,hidden,order):
        self.mainDirName = Frame(self.RightFrame)
        self.mainDirName.grid(sticky=E+N+W+S)

        Button(self.mainDirName,text="<",font="Helvetica 14",command = (lambda dir=dir: self.changeMainCanvas(dir.getParentDir(),hidden,order))).grid(row=0,column=0,sticky=W)
        Label(self.mainDirName,text=dir.path,font="Helvetica 14").grid(row=0,column=1,sticky=W)

        if hidden == 0:
            Button(self.mainDirName,text="Show hidden",font="Helvetica",bg='#fafafa',command = (lambda dir=dir: self.changeMainCanvas(dir,1,order))).grid(row=0,column=2,sticky=E,padx=(80,0))
        if hidden == 1:
            Button(self.mainDirName,text="Hide hidden",font="Helvetica",bg='#fafafa',command = (lambda dir=dir: self.changeMainCanvas(dir,0,order))).grid(row=0,column=2,sticky=E,padx=(80,0))

        Entry(self.mainDirName).grid(row=0,column=3,sticky=W+N,padx=(600,0),pady=(6,0))


        self.mainCanvas = Frame(self.RightFrame)
        self.mainCanvas.grid(sticky=E+N+W+S)

        Button(self.mainCanvas,text='SIZE(MB)',font="Helvetica 14",width=9,command = (lambda dir=dir: self.changeMainCanvas(dir,hidden,1))).grid(row=0,column=1)
        Label(self.mainCanvas,text='PRIVILEGES',font="Helvetica 14",width=11).grid(row=0,column=2)
        Button(self.mainCanvas,text='MODIFIED',font="Helvetica 14",width=11,command = (lambda dir=dir: self.changeMainCanvas(dir,hidden,2))).grid(row=0,column=3)
        Label(self.mainCanvas,text='USED',font="Helvetica 14",width=11).grid(row=0,column=4)
        Label(self.mainCanvas,text='TYPE',font="Helvetica 14",width=5).grid(row=0,column=5)



        j=1
        for direc in dir.getDirsByOrder(order):
            if hidden == 0 and direc.hidden == 1:
                continue
            Button(self.mainCanvas,text=str(direc.name),font="Helvetica 10",bg="red",width=100,command=(lambda direc=direc: self.changeMainCanvas(direc,hidden,order))).grid(row=j,column=0,sticky=W+N)
            Label(self.mainCanvas,text=str(direc.size),font="Helvetica 12").grid(row=j,column=1,sticky=N)
            Label(self.mainCanvas,text=str(direc.mask),font="Helvetica 12").grid(row=j,column=2,sticky=N)
            Label(self.mainCanvas,text=str(direc.lastModified),font="Helvetica 12").grid(row=j,column=3,sticky=N)
            Label(self.mainCanvas,text=str(direc.lastUsed),font="Helvetica 12").grid(row=j,column=4,sticky=N)
            Label(self.mainCanvas,text=str(direc.type),font="Helvetica 12").grid(row=j,column=5,sticky=N)
            j = j + 1
            if(j>14):
                break


        for filess in dir.getFilesByOrder(order):
            if hidden == 0 and filess.hidden == 1:
                continue
            Button(self.mainCanvas,text=str(filess.name),font="Helvetica 10",bg="grey55",width=100,command = (lambda f=filess: f.execute())).grid(row=j,column=0,sticky=W+N)
            Label(self.mainCanvas,text=str(filess.size),font="Helvetica 12").grid(row=j,column=1,sticky=N)
            Label(self.mainCanvas,text=str(filess.mask),font="Helvetica 12").grid(row=j,column=2,sticky=N)
            Label(self.mainCanvas,text=str(filess.lastModified),font="Helvetica 12").grid(row=j,column=3,sticky=N)
            Label(self.mainCanvas,text=str(filess.lastUsed),font="Helvetica 12").grid(row=j,column=4,sticky=N)
            Label(self.mainCanvas,text=str(filess.type),font="Helvetica 12").grid(row=j,column=5,sticky=N)
            j = j + 1
            if(j>26):
                break

        return self.mainDirName,self.mainCanvas

    def deleteMainCanvas(self):
        self.mainDirName.destroy()
        self.mainCanvas.destroy()
        self.ruFrame.destroy()

    def changeMainCanvas(self,newdir,hidden,order):
        self.deleteMainCanvas()
        newdir.enlistContents()

        nc = self.drawMainCanvas(newdir,hidden,order)
        nc[0].grid(row=0,column=1,sticky=W)
        nc[1].grid(row=1,column=1,sticky=W+N)

        self.getRecentlyUsedDirs().grid(row=3,column=0,sticky=W+E)

        self.updateRecentlyUsedDirs(newdir)
        self.updatePopularity(newdir)
        if (time.time()-self.t0) > 100:
            self.popFrame.destroy()
            self.changePopularCanvas()
            self.t0 = time.time()

    def updateRecentlyUsedDirs(self,newdir):
        j=0
        for i in self.recentDirs:
            if i.path.find(newdir.path) == 0:
                return
            if i.path == newdir.path:
                return
            if newdir.path.find(i.path) >= 0:
                self.recentDirs[j] = newdir
                return
            j=j+1

        self.recentDirs.append(newdir)
        if len(self.recentDirs)>6:
            self.recentDirs.pop(0)

    def getRecentlyUsedDirs(self):
        self.ruFrame = Frame(self.LeftFrame)
        self.ruFrame.grid(sticky=W+N+E+S)
        self.ruFrame.columnconfigure(0,weight=1)
        j=0
        for i in self.recentDirs:
            Button(self.ruFrame,text=self.cutBigPaths(i.path),width=33,font="Helvetica 10",command=(lambda i=i: self.changeMainCanvas(i,i.hidden,0))).grid(row=j,column=0,sticky=W+N+E+S)
            j=j+1
            if j>6:
                break
        return self.ruFrame

    def cutBigPaths(self,path):
        if len(path) > 30:
            path = '...'+path[-30:]
        return path

    def changePopularCanvas(self):
        self.popFrame.destroy()
        self.getPopularDirs()

    def getPopularDirs(self):
        self.popFrame = Frame(self.LeftFrame)
        self.popFrame.grid(sticky=E+N+W+S)
        self.popFrame.columnconfigure(0,weight=1)
        j=0
        for i in self.popularityHeap:
            Button(self.popFrame,text=self.cutBigPaths(i[0].path),font="Helvetica 10",command=(lambda i=i: self.changeMainCanvas(i[0],i[0].hidden,0))).grid(row=j,column=0,sticky=W+E)
            j = j+1
            if(j>10):
                break

        return self.popFrame

    def initialisePopularDirsHeap(self):
        return [(self.root,0)]

    def updatePopularity(self,ndir):
        self.popularityHeap,updatedNode = ph.increasePopularity(self.popularityHeap,ndir)
        self.popularityHeap = ph.updateHeap(self.popularityHeap,updatedNode)

if __name__ == "__main__":
    d = mainWindow()
    d.mainloop()
