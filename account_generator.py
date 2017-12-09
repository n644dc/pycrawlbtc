import pybitcoin
import sys
import os


class PassGen:
    def __init__(self):

        isLinux = sys.platform.lower().startswith('linux')

        # Init Vars
        self.workDir = '/var/www/html/bitcon' if isLinux else 'C:\\bitcon'
        self.phraseLocation = "{}/phrases/".format(self.workDir) if isLinux else "{}\\phrases\\".format(self.workDir)
        self.wordFile = 'linux.words'
        self.OneHundredK = []
        self.words = []

        # Create DIR Struct
        if not os.path.exists(self.workDir):
            os.makedirs(self.workDir)

        if not os.path.exists(self.workDir):
            os.makedirs(self.workDir)


        # read in list
        # start recording word combos separate by comma
        # create 100k entries per file

    def generatePhrases(self):
        with open(self.wordFile) as f:
            self.words = f.readlines()

        self.words = [x.strip() for x in self.words]