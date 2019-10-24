import ahocorasick

class AC_matched():
    def __init__(self, a, b, c):
        self.matched = a
        self.word_tag_index = b
        self.word_next_idx = c
        self._i = 0
        self.accept_endidx = -1

    def save_state(self):
        return self.accept_endidx

    def restore_state(self, state):
        self.accept_endidx = state
        self.skip_unaccept()

    def reset(self):
        self._i = 0
        self.accept_endidx = -1

    def has_next(self):
        self.skip_unaccept()
        return self._i < len(self.matched)

    def iter_init_status(self, init_i):
        keyword = self.matched[init_i]
        self.accept(keyword)
        self.skip_unaccept()
        return keyword

    def skip_unaccept(self):
        self._i = self.word_next_idx[ self.accept_endidx + 1 ]
        #while self._i < len(self.matched) and self.matched[self._i][0] <= self.accept_endidx:
        #    self._i += 1

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
        self.keyword_ac = ahocorasick.Automaton()
        self.slot_ac = ahocorasick.Automaton()

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
        self.init_slot_ac(files)
        self.init_keyword_ac(all_keywords)
        self.slot_ac.make_automaton()
        self.keyword_ac.make_automaton()
        print("MAKE AUTOMATON SUCCESS")

    def match(self, query):
        matched = self.match_a_ac(self.keyword_ac, query, "0")
        matched_slot = self.match_a_ac(self.slot_ac, query, "1")
        matched.extend(matched_slot)
        matched.sort(key = lambda x: (x[0], -x[1]) )
        return AC_matched(matched, self.get_tag_idx_dict(matched), self.build_word_next_idx(matched, query))
        
    def match_a_ac(self, A, query, word_tp):
        ans = []
        for end_index, (tag, key_length) in A.iter(query):
            start_index = end_index - key_length + 1
            ans.append((start_index, end_index, tag, word_tp))
        return ans

    def get_tag_idx_dict(self, key_index):
        ans = {}
        for start_index, end_index, tags, tp in key_index:
            for kk in tags:
                #if type(kk) is list: print(kk, key, tag)
                val = ans.get(kk, [])
                val.append( (start_index, end_index, tp) )
                ans[kk] = val
        return ans
        
    # 每个位置的下一个合法位置的索引
    def build_word_next_idx(self, key_index, query):
        ans = [-1] * len(query)
        for j, (start_index, end_index, tags, tp) in enumerate(key_index):
            if ans[start_index] < 0:
                ans[start_index] = j

        pre = len(key_index)
        ans.append(pre)
        for j in range(len(ans) -1, -1, -1):
            if ans[j] < 0:
                ans[j] = pre
            else:
                pre = ans[j]

        return ans
