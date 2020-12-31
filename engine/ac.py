import ahocorasick
from items import AcMatchedGroup


class AcMatcher:
    def __init__(self, a, b, l):
        self.matched = a
        self.sorted()
        self.word_tag_index = b
        self.word_next_idx = []
        self._i = 0
        self.accept_endidx = -1
        self.dialog_length = l

    def sorted(self):
        self.matched.sort(key = lambda x: (x.start, -x.end))

    def delete_tag(self, keeped_tags):
        self.matched = [m for m in self.matched if m.tag in keeped_tags]

    def get_state(self):
        return (self._i, self.accept_endidx)

    def reset_state(self, state):
        self._i = state[0]
        self.accept_endidx = state[1]

    def reset(self):
        self._i = 0
        self.accept_endidx = -1

    def has_next(self):
        self.skip_unaccept()
        return self._i < len(self.matched)

    def iter_init(self, init_i):
        self._i = init_i
        keyword = self.matched[init_i]
        if init_i == 0:
            self.accept_endidx = -1
        else:
            self.accept_endidx = keyword.start - 1

    # 每个位置的下一个合法位置的索引
    def build_word_next_idx(self):
        k = 0
        for i in range(self.dialog_length):
            while k < len(self.matched) and self.matched[k].start <= i:
                k += 1
            self.word_next_idx.append(k)

    def skip_unaccept(self):
        if self.word_next_idx:
            if self.accept_endidx < 0: return 0
            self._i = max(self._i, self.word_next_idx[self.accept_endidx])
        else:
            while self._i < len(self.matched) and self.matched[self._i].start <= self.accept_endidx:
                self._i += 1

    def get_cur(self):
        self.skip_unaccept()
        if self._i < len(self.matched):
            return self.matched[self._i - 1]
        
    def get_typeed_next(self, tp):
        self.skip_unaccept()
        while self._i < len(self.matched) and self.matched[self._i].tag_type != tp:
            self._i += 1

        if self._i < len(self.matched):
            self._i += 1
            return self.matched[self._i - 1]

    def look_next(self, t):
        j = self._i + t - 1
        if j >= len(self.matched): return None
        return self.matched[j]

    def get_next(self):
        self.skip_unaccept()
        #if self._i < len(self.matched):
        self._i += 1
        return self.matched[self._i - 1]

    def accept(self, ele):
        self.accept_endidx = ele.end

    def get_word_dist(self, new_idx):
        return new_idx - self.accept_endidx - 1


class AC:
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
        return AcMatcher(matched, self.get_tag_idx_dict(matched), len(query))
        
    def match_a_ac(self, A, query, word_tp):
        ans = []
        if A is None: return ans
        for end_index, (tags, key_length) in A.iter(query):
            start_index = end_index - key_length + 1
            for tag in tags:
                ans.append(AcMatchedGroup(start_index, end_index, tag, word_tp))
        return ans

    def get_tag_idx_dict(self, matchgroups):
        ans = {}
        for start_index, end_index, tag, tp in matchgroups:
            #if type(kk) is list: print(kk, key, tag)
            if tag not in ans: ans[tag] = []
            ans[tag].append((start_index, end_index, tp))
        return ans
