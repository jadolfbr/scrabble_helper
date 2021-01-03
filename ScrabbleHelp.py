from Tkinter import *
import tkFileDialog
import tkSimpleDialog
import tkMessageBox
import os
import re
from operator import itemgetter
#This will become a GUI based program to beat IAN in scrabble for the first time in 15 years.

class ScrabbleGUI:
    def __init__(self):
        '''
        Sets up the GUI
        '''
        self.main = Tk()
        self.main.title('Intelligent Scrabble Help')
        
        #Varibles Used:
        self.LetterPoints = dict(); #Dictionary of letter points.
        self.LetterPoints = {'e':1,'a':1,'i':1,'o':1,'t':1,'r':1,'s':1,
                             'd':2,'n':2,'l':2,'u':2,
                             'h':3,'g':3,'y':3,
                             'b':4,'c':4,'f':4,'m':4,'p':4,'w':4,
                             'v':5,'k':5,
                             'x':8,
                             'j':10,'q':10,'z':10, '.':0}
        self.Letters = StringVar()
        self.LetterBuild = StringVar(); #Letters you want to build off of.
        self.kickchoice = StringVar();
        self.kickchoice.set("Check if word exists")
        self.pwd = os.getcwd()
        
        #SetTk
        self.LettersEntry = Entry(self.main, textvariable=self.Letters)
        self.LettersLabel = Label(self.main, text = "Your Letters (# = Wild):")
        
        self.LetterBuildEntry = Entry(self.main, textvariable = self.LetterBuild)
        self.LetterBuildLabel = Label(self.main, text = "Letter(s) to build off of:")
        
        self.KickCommand = Button(self.main, text = "Lets Do This:", command=lambda:self.kickCommand(self.kickchoice.get()))
        self.KickCommands = OptionMenu(self.main, self.kickchoice, "Check if word exists", "Find word using letters", "Find word using base", "Find word with split base (W...X)", "Find word using additional constraints")
        
        EngPhoto =PhotoImage(file = (self.pwd+"/Media/Beat_Ian.gif"))
        self.Photo = Label(self.main, image=EngPhoto)
        self.Photo.image = EngPhoto
        self.Photo.grid(row =0, column = 2, rowspan = 6)
        
        #shoTk
        self.LettersEntry.grid(row =0, column=1)
        self.LettersLabel.grid(row = 0, column=0)
        self.LetterBuildLabel.grid(row=1, column=0)
        self.LetterBuildEntry.grid(row=1, column=1)
        
        self.KickCommand.grid(row=2, column=0)
        self.KickCommands.grid(row=2, column=1)
        
        #Sets up list of words#
        FILE = open(self.pwd+"/ScrabbleDictionary.txt", 'r')
        self.ScrabbleWordsList = []
        for line in FILE:
            lineSP = line.split("\n")
            self.ScrabbleWordsList.append(lineSP[0])
        
        
        #Here, I will try to put in a 'textframe' widget.
        self.frame = Frame(self.main)
        
        self.text = Text(self.frame, height=30,width=40, background='white')
        scroll = Scrollbar(self.main)
        self.text.configure(yscrollcommand=scroll.set)
        scroll.config(command = self.text.yview)
        
        self.text.grid(row=0, column=3, columnspan=3, rowspan=6, sticky=W+E)
        scroll.grid(row=0, column=6, rowspan=6)
        self.frame.grid(row = 0, column=3, columnspan =3, rowspan=6)
        #Main Loop
        
        self.textPlace = 1.0
        self.text.insert(1.0, "\nHello :)")
        self.text.insert(1.0, "\nReady to beat Ian?")
        self.main.mainloop()
        
    def kickCommand(self, command):
        #This is the bad way to do wilds.  I should have put them in from the beginning.

        #This controls splits.
        #Fixes any wild cards.
        #self.textPlace = 0.0
        yourLetters = self.Letters.get()
        yourLetters = yourLetters.replace("#", ".")
        yourLetters = yourLetters.replace("-", ".")
        self.Letters.set(yourLetters)
        
        #self.textPlace = self.textPlace+1.0
        self.text.insert(self.textPlace, "\nReturning New Command: "+ self.Letters.get()+ " : "+self.LetterBuild.get()+"\n")
        if re.search("\.", self.LetterBuild.get()) and command=="Find word using base":
            command = "Find word with split base (W...X)"
        if command=="Check if word exists":
            #print "Finding word in list..."
            #self.textPlace+1.0
            self.text.insert(self.textPlace, "\nFinding word in list...\n")
            word = tkSimpleDialog.askstring(title = "Word", prompt = "Please enter word(s) you wish to look up (word,word,word)")
            self.text.insert(self.textPlace, "\n"+word)
            self.checkIfWordExists(word)
            return
        elif command =="Find word using letters":
            #Find a word using the combination of letters
            #self.textPlace = self.textPlace+1.0
            self.text.insert(self.textPlace, "\nFinding word using letter combinations...\n")
            #Tosort = tkMessageBox.askquestion(title="Sort", message = "Sort by word length?", default='no')
            
            Tosort = "points"
            self.makeWords(self.Letters.get(), Tosort)
            return
        elif command == "Find word using base":
            #Find a word using these letters as a base
            #Ask if this starts the word.
            start = tkMessageBox.askyesno(message = "Will this start the word?", default = 'no')
            self.maxLength="0"
            self.maxConstraints = StringVar()
            self.maxConstraints.set("0x0")
            self.startWord = False
            if start ==True:
                self.startWord = True
                self.maxLength= tkSimpleDialog.askinteger(title = "Length", prompt = "What is the maximum length of the word (0 = Wild)?", initialvalue=self.maxLength)
            else:

                sides = tkSimpleDialog.askstring(title = "Constraints", prompt = "Please enter max Left and max Right of word (2x4) (0x0 = Wild)", initialvalue=self.maxConstraints.get())
                self.maxConstraints.set(sides)
            #more = tkMessageBox.askyesno(message = "Do you wish to specify Special Tiles?", default = 'no')
            
            constraintDic = dict()
            constraintDic['length']=self.maxLength
            constraintDic['start']=self.startWord
            constraintDic['sides']=self.maxConstraints.get()
            #if more==True:
                #Launch Special Tile dialog box.
                #pass
            #If yes, ask the maximum length of word required:
            buildSP = self.LetterBuild.get().split(",")
            if re.search(",", self.LetterBuild.get()):
                for build in buildSP:
                    
                    self.makeWordBase(self.Letters.get(),build, constraintDic)
                    self.text.insert(1.0, "\nNext Build is: "+build+"\n")
            else:
                self.makeWordBase(self.Letters.get(), self.LetterBuild.get(), constraintDic)
            return
        elif command =="Find word with split base (W...X)":
            #self.textPlace = self.textPlace+1.0
            self.text.insert(self.textPlace, "\nUsing split base...")
            constraintDic=dict()
            constraintDic['start']=False
            constraintDic['sides']="0x0"
            self.makeWordBase(self.Letters.get(), self.LetterBuild.get(), constraintDic)
            return
    def checkIfWordExists(self, letters):
        '''
        This simply returns all words that contain the letters in order.
        Can pass multiple words by word,word,word
        '''
        
        letters = letters.lower()
        letterSP = letters.split(",")
        wordsDic = dict()
        if len(letterSP)==1:
            path = self.pwd+"/ScrabbleDictionary.txt"
            FILE = open(path, 'r')
            all = FILE.readlines()
            
            for l in self.ScrabbleWordsList:
                if re.search(letters, l):
                    points = 0
                    for let in l:
                        points = points +self.LetterPoints[let]
                    #self.textPlace = self.textPlace+1.0
                    wordsDic[l]=dict()
                    wordsDic[l]['points']=points
                    #self.text.insert(self.textPlace,  "\nFound: "+ l+" : "+repr(points))
            sortDic = dict()
            for word in wordsDic:
                sortDic[word]=wordsDic[word]['points']
            x = sorted(sortDic.iteritems(), key=itemgetter(1), reverse=False)
            for item in x:
                #self.textPlace = self.textPlace+1.0
                self.text.insert(self.textPlace,  "\nFound: "+item[0]+" : "+repr(item[1]))
            FILE.close()
        else:
            for item in letterSP:
                self.checkIfWordExists(item)
            
        return
    
    def makeWords(self, letters, Tosort):
        '''
        Basic make words for a string of letters.
        '''
        #wordsDic[word][points]= #points
        #wordsDic[word][base]=list of letters from query making up word
        wordsDic= dict()
        letters = letters.lower()
        originalLetterString = letters
        
        for Scrabbleword in self.ScrabbleWordsList:
            letters = originalLetterString
            foundLetters = []
            found = True
            
            #This MAY deal with wild.
            for letter in Scrabbleword:
                if re.search(letter, letters):
                    foundLetters.append(letter)
                    letters = letters.replace(letter, '',1)
                    #print "found: "+letter
                else:
                    if re.search("\.", letters):
                        foundLetters.append(".")
                        letters = letters.replace(".", '', 1)
                    else:
                        found = False
            if found ==True:
                wordsDic[Scrabbleword]=dict()
                wordsDic[Scrabbleword]['base']=foundLetters
                points = 0
                for let in foundLetters:
                    points = points+self.LetterPoints[let]
                wordsDic[Scrabbleword]['points']=points
        
        #Here, is where we sort the words that have been found by points.
        #I suck at this sorting shit.
        if Tosort =="points":
            #Sort and print by points
            sortDic = dict()
            for word in wordsDic:
                sortDic[word]=wordsDic[word]['points']
            x = sorted(sortDic.iteritems(), key=itemgetter(1), reverse=False)
            for item in x:
                #self.textPlace = self.textPlace+1.0
                self.text.insert(self.textPlace,  "\n"+item[0]+" : "+repr(item[1]))
        
        elif Tosort=="length":
            sortDic = dict()
            for word in wordsDic:
                sortDic[word] = len(wordsDic[word]['base'])
            x = sorted(sortDic.iteritems(), key=itemgetter(1), reverse=False)
            for item in x:
                #self.textPlace = self.textPlace+1.0
                self.text.insert(self.textPlace,  "\n"+item[0]+" : "+repr(item[1]))
        return
    
    def makeWordBase(self, letters, build, constraintDic, ret = 0):
        letters = letters.lower()
        build = build.lower()
        wordsDic= dict()
        originalLetterString = letters
        if constraintDic['start']==True:
            #Build from start
            build = '^'+build
            constraintDic['start']=False; constraintDic['sides']="0x0"
            self.makeWordBase(letters, build, constraintDic)
            return
        elif constraintDic['start']==False:
            if constraintDic['sides']=="0x0":
                #Kicks regular make word base.
                for Scrabbleword in self.ScrabbleWordsList:
                    letters = originalLetterString
                    foundLetters = []
                    found = True
                    #First, we try to find the 'build' in word:
                    if re.search(build, Scrabbleword):
                        buildRemoved = build.replace('.', '')
                        letters = letters + buildRemoved
                    else:
                        found = False
                    for letter in Scrabbleword:
                        if found ==False:
                            continue
                        if re.search(letter, letters):
                            foundLetters.append(letter)
                            letters = letters.replace(letter, '',1)
                            #print "found: "+letter
                        else:
                            if re.search("\.", letters):
                                foundLetters.append(".")
                                letters = letters.replace(".", '', 1)
                            else:
                                found = False
                    if found ==True:
                        if not wordsDic.has_key(Scrabbleword):
                            wordsDic[Scrabbleword]=dict()
                        wordsDic[Scrabbleword]['base']=foundLetters
                        points = 0
                        for let in foundLetters:
                            points = points+self.LetterPoints[let]
                        wordsDic[Scrabbleword]['points']=points
                if ret==1:
                    return wordsDic
            else:
                side = constraintDic['sides']
                constraintDic['sides']="0x0"
                wordsDic = self.makeWordBase(letters, build, constraintDic, 1)
                sideSP = side.split("x")
                for words in wordsDic:
                    leftInd = words.index(build[0])
                    rightInd = words.index(build[len(build)-1])
                    if len(words[:leftInd])-1<=int(sideSP[0]) and len(words[rightInd:])<=int(sideSP[1]):
                        pass
                    else:
                        wordsDic.pop(words)
            sortDic = dict()
            for word in wordsDic:
                sortDic[word]=wordsDic[word]['points']
            x = sorted(sortDic.iteritems(), key=itemgetter(1), reverse=False)
            for item in x:
                #self.textPlace = self.textPlace+1.0
                self.text.insert(self.textPlace,  "\n"+item[0]+" : "+repr(item[1]))
    
        
if len(sys.argv)>1:
    if sys.argv[1]=="script":
        letters = "asdfg"
        build = "rue"
        constraintDic['start']=False
        constraintDic['sides']="0x0"
        ScrabbleGUI().makeWordBase(letters, build, constraintDic)
            
ScrabbleGUI()
