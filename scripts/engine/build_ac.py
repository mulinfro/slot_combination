import ahocorasick

class AC_matched():
    def __init__(self, a, b):
        self.matched = a
        self.word_tag_index = b
        self._i = 0
        self.init_i = 0
        self.accept_endidx = -1

    def save_state(self):
        return (self._i, self.accept_endidx)

    def restore_state(self, state):
        self._i = state[0]
        self.accept_endidx = state[1]

    def iter_init_status(self):
        if self.init_i < len(self.matched):
            self.init_i += 1
            self._i = self.init_i
            keyword = self.matched[self._i - 1]
            self.accept(keyword)
            return keyword

    def get_cur(self):
        while self._i < len(self.matched) and self.matched[self._i][0] <= self.accept_endidx:
            self._i += 1
        if self._i < len(self.matched):
            return self.matched[self._i - 1]
        
    def get_typeed_next(self, tp):
        while self._i < len(self.matched):
            km = self.matched[self._i]
            if km[0] <= self.accept_endidx or km[3] != tp:
                self._i += 1
            else:
                break
        if self._i < len(self.matched):
            self._i += 1
            return self.matched[self._i - 1]

    def get_next(self):
        while self._i < len(self.matched) and self.matched[self._i][0] <= self.accept_endidx:
            self._i += 1
        if self._i < len(self.matched):
            self._i += 1
            return self.matched[self._i - 1]

    def accept(self, ele):
        self.accept_endidx = ele[1]

    def get_word_dist(self, new_dist):
        return new_dist - self.accept_endidx - 1

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
                    self.slot_ac.add_word(line, (exists_flag, len(line)))
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

    def match(self, dialog):
        print(dialog)
        matched = self.match_a_ac(self.keyword_ac, dialog, "0")
        matched_slot = self.match_a_ac(self.slot_ac, dialog, "1")
        matched.extend(matched_slot)
        matched.sort(key = lambda x: (x[0], -x[1]) )
        return AC_matched(matched, self.get_tag_idx_dict(matched))
        
    def match_a_ac(self, A, dialog, word_tp):
        ans = []
        for end_index, (tag, key_length) in A.iter(dialog):
            start_index = end_index - key_length + 1
            ans.append((start_index, end_index, tag, word_tp))
        return ans

    def get_tag_idx_dict(self, key_index):
        ans = {}
        for start_index, end_index, key, tag in key_index:
            for kk in key:
                val = ans.get(kk, [])
                val.append( (start_index, end_index, tag) )
                ans[kk] = val
        return ans
        
