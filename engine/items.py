
from collections import namedtuple
ParamItem = namedtuple('ParamItem', ['tp', 'val'])
TNode = namedtuple('TNode', ['name', 'slices', 'permutation'])

AcMatchedGroup = namedtuple('AcMatchedGroup', ['start', 'end', 'tag', 'tag_type'])

class MatchedItem:

    def __init__(self, tagkey, fragments, tnodes):
        self.tagkey = tagkey
        self.fragments = fragments
        self.tnodes = tnodes
        self.matched = ""
        self.match_score = 0
        self.miss_score = 0
        self.begin = 0
        self.end = 0

    def __repr__(self):
        return "%s,%d,%d"%(self.matched, self.begin, self.end)

    def score(self):
        matched_length = len(self.fragments)
        for t in self.fragments:
            matched_length += t[3] - t[2]
        miss_length = self.end - self.begin + 1 - matched_length
        return (matched_length, miss_length)

    def cal_index(self):
        self.begin =  self.fragments[0][0] 
        self.end   =  self.fragments[-1][1] 

    def cal_match_score(self, dialog):
        eles = self.tagkey.strip("#").split("#")
        assert len(eles) == len(self.fragments), "Need match"
        self.cal_index()

        frags = []
        for i, idx in enumerate(self.fragments):
            bi, ei = idx[0], idx[1]
            frags.append((dialog[bi: ei + 1], eles[i], bi, ei))
        self.fragments = frags

        self.matched = dialog[self.begin: self.end + 1]
        sv = self.score()
        self.match_score = sv[0] / len(dialog)
        self.miss_score = sv[1] / sv[0]
