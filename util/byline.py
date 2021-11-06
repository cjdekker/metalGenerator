#!/usr/bin/env python3

""" read tab data from file into data structure """
import re

class TabParse:
    def __init__(self, path):
        self.path = path
        self.linez= []
        self.passages = []

    def parse(self):
        with open(self.path, 'r') as fh:
            while l := fh.readline():
                mo = re.search(r'(\|.*-+.*\|)', l)
                if mo:
                    mymatch = mo.group(1)
                    self.linez.append(mymatch)
        
        numlinez = len(self.linez)
        if numlinez % 6 == 0:
            # got six-string tab..
            for i in range(numlinez // 6):
                self.passages.append([])
                for j in range(6*i, 6*i + 6):
                    self.passages[i].append(self.linez[j])
        return self.passages
