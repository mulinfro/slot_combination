
from collections import namedtuple
ParamItem = namedtuple('ParamItem', ['tp', 'val'])
# Trie树的叶子节点信息
# name:   匹配到的规则名  
# slices: 槽位占据的tag个数,  一个槽位可以是多个tag值组合而成
# permutation: 槽位位置信息， 主要用于 <> 这种无序规则的位置信息
TNode = namedtuple('TNode', ['name', 'slices', 'permutation'])

# SpecialRulePost = namedtuple('SpecialRulePost', ['tag', 'start', 'end'])

"""
tag_type: str
   0: atom
   1: ref
   2: plus
   3: 需要特殊处理的atom或变量
"""
AcMatchedGroup = namedtuple('AcMatchedGroup', ['start', 'end', 'tag', 'tag_type'])

class AnyPat:

    def __init__(self, min_span, max_span):
        self.min_span = min_span
        self.max_span = max_span

    def is_valid(self, n):
        if n >= self.min_span:
            if self.max_span < 0:
                return True
            else:
                return n <= self.max_span

    def to_pat(self):
        return "__ANY__:%d:%d"%(self.min_span, self.max_span)

    def equal(self, min_s, max_s):
        return self.min_span == min_s and self.max_span == max_s

    def get_max_dist(self, cur, maxl):
        idx = -1
        if self.max_span < 0:
            idx = maxl
        else:
            idx = min(cur + self.max_span, maxl)
        if idx - cur < self.min_span:
            return -1
        return idx 


class MatchedItem:
    """
        匹配到的完整规则ITEM
        包含一些必要信息

        例子:
            tagkey  =>  #num#op#num#多少 
            fragments =>  ((0, 0), (1, 1), (2, 2), (4, 5))
            tnodes  =>  [TNode(name='expr1', slices=(1, 1, 1, 1), permutation=None),
                        TNode(name='expr2', slices=(1, 1, 1, 1), permutation=None), 
                        TNode(name='calculator1', slices=(3, 0, 1), permutation=None)]
    """

    def __init__(self, tagkey, fragments, tnodes):
        self.tagkey = tagkey
        self.fragments = fragments
        self.tnodes = tnodes
        self.matched = ""
        self.match_score = 0
        self.fuzzy_degree = 0
        self.begin = 0
        self.end = 0

    def concat(self, item):
        self.end = item.end
        self.tagkey += "#" + item.tagkey
        self.fragments += item.fragments

    def __repr__(self):
        return "(%s,%d,%d)"%(self.matched, self.begin, self.end)

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
        # 匹配到的字符长度占整个query的比例; 越大越好
        self.match_score = sv[0] / len(dialog)
        # 模糊匹配的长度占匹配的pattern的比例
        # {听} 额额 {刘德华} 的 {歌}  =  3 / (1 + 2 + 3 + 1 + 1)
        self.fuzzy_degree = sv[1] / sv[0]
