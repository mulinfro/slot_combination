import ahocorasick

from collections import namedtuple
MatchedGroup = namedtuple('MatchedGroup', ['start', 'end', 'tags', 'tag_type'])

class AC_matched():
    def __init__(self, a, b):
        self.matched = a
        self.sort_tags()
        self.word_tag_index = b
        self.word_next_idx = None
        self._i = 0
        self.accept_endidx = -1

    def sort_tags(self):
        self.matched.sort(key = lambda x: (x.start, -x.end))

    def delete_tag(self, need_delete_tags):
        new_AM = []
        for (a,b,tag,c) in self.matched:
            new_tag = [ t for t in tag if t not in need_delete_tags]
            if new_tag:
                new_AM.append( (a,b,new_tag, c) )
        self.matched = new_AM

    # 每个位置的下一个合法位置的索引
    def build_word_next_idx(self, n):
        ans = [-1] * n
        for j, (start_index, end_index, tags, tp) in enumerate(self.matched):
            if ans[start_index] < 0:
                ans[start_index] = j

        pre = len(self.matched)
        ans.append(pre)
        for j in range(len(ans) -1, -1, -1):
            if ans[j] < 0:
                ans[j] = pre
            else:
                pre = ans[j]

        return ans

    def save_state(self):
        return (self._i, self.accept_endidx)

    def restore_state(self, state):
        self._i = state[0]
        self.accept_endidx = state[1]

    def reset(self):
        self._i = 0
        self.accept_endidx = -1

    def has_next(self):
        self.skip_unaccept()
        return self._i < len(self.matched)

    def iter_init_status(self, init_i):
        keyword = self.matched[init_i]
        self.accept(keyword)
        self._i = init_i
        self.skip_unaccept()
        return keyword

    def skip_unaccept(self):
        if self.word_next_idx:
            self._i = max(self._i, self.word_next_idx[ self.accept_endidx + 1 ])
        else:
            while self._i < len(self.matched) and self.matched[self._i][0] <= self.accept_endidx:
                self._i += 1

    def get_cur(self):
        self.skip_unaccept()
        if self._i < len(self.matched):
            return self.matched[self._i - 1]
        
    def get_typeed_next(self, tp):
        self.skip_unaccept()
        while self._i < len(self.matched) and self.matched[self._i][3] != tp:
            self._i += 1

        if self._i < len(self.matched):
            self._i += 1
            return self.matched[self._i - 1]

    def get_next(self):
        self.skip_unaccept()
        #if self._i < len(self.matched):
        self._i += 1
        return self.matched[self._i - 1]

    def accept(self, ele):
        self.accept_endidx = ele[1]

    def get_word_dist(self, new_idx):
        return new_idx - self.accept_endidx - 1



class AC():
    def __init__(self):
        self.keyword_ac = None
        self.slot_ac = None

    def init_slot_ac(self, files):
        if not files:
            self.slot_ac.add_word("###", (["SYS"], 3))
        else:
            self.read_and_insert(files)

    def read_and_insert(self, files):
        for f in files:
            tag = f.split("/")[-1].split(".")[0]
            for line in open(f):
                line = line.strip()
                if not line: continue
                exists_flag = self.slot_ac.get(line, None)
                if exists_flag is not None:
                    if tag not in exists_flag[0]:
                        exists_flag[0].append(tag)
                        #assert type(exists_flag) == list, exists_flag
                        self.slot_ac.add_word(line, (exists_flag[0], len(line)))
                else:
                    self.slot_ac.add_word(line, ([tag], len(line)))

    def init_keyword_ac(self, all_keywords): 
        for k, v in all_keywords.items():
            self.keyword_ac.add_word(k, (v, len(k)))

    def make(self, all_keywords, files):
        if files:
            self.slot_ac = ahocorasick.Automaton()
            self.init_slot_ac(files)
            self.slot_ac.make_automaton()
        if all_keywords:
            self.keyword_ac = ahocorasick.Automaton()
            self.init_keyword_ac(all_keywords)
            self.keyword_ac.make_automaton()
        print("MAKE AUTOMATION SUCCESS", self.keyword_ac, self.slot_ac)

    def match(self, query):
        matched = self.match_a_ac(self.keyword_ac, query, "0")
        matched_slot = self.match_a_ac(self.slot_ac, query, "1")
        matched.extend(matched_slot)
        return AC_matched(matched, self.get_tag_idx_dict(matched))
        
    def match_a_ac(self, A, query, word_tp):
        ans = []
        if A is None: return ans
        for end_index, (tag, key_length) in A.iter(query):
            start_index = end_index - key_length + 1
            ans.append(MatchedGroup(start_index, end_index, tag, word_tp))
        return ans

    def get_tag_idx_dict(self, matchgroups):
        ans = {}
        for start_index, end_index, tags, tp in matchgroups:
            for kk in tags:
                #if type(kk) is list: print(kk, key, tag)
                val = ans.get(kk, [])
                val.append( (start_index, end_index, tp) )
                ans[kk] = val
        return ans
