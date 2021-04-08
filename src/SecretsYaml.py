import os

class SecretsYaml:
    def __init__(self, relativeFilePath):
        self.workingFolder = os.path.dirname(os.path.abspath(__file__))
        print(f"({relativeFilePath}) dir:", self.workingFolder)
        self.relativeFilePath = relativeFilePath
        print(f"({relativeFilePath}) name:", self.relativeFilePath)
        self.absoluteFilePath = os.path.join(self.workingFolder, self.relativeFilePath)
        print(f"({relativeFilePath}) path:", self.absoluteFilePath)
        self.dictionary = {}
        self.load()
        print(f"({relativeFilePath}) loaded:", self.dictionary)


    def load(self):
        self.dictionary = {}
        f = open(self.absoluteFilePath, "r")
        raw = f.read()
        f.close()
        lines = raw.split('\n')
        for l in lines:
            if l:
                split = l.split(":", 1)
                key = split[0].strip()
                val = split[1].strip()
                self.dictionary[key] = val


    def find(self, key):
        try:
            return self.dictionary[key]
        except:
            return None
