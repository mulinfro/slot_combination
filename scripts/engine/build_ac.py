import ahocorasick

class AC_matched():
    def __init__(self, a, b):
        self.matched = a
        self.word_tag_index = c
        self._i = 0
        self.init_i = 0
        self.accept_endidx = -1

    def save_state(self):
        return (self._i, self.accept_endidx)

    def restore_state(self, state):
        self.keyword_i = state[0]
        self.accept_endidx = state[1]

    def iter_init_status(self):
        if self.init_keyword_i < len(self.matched_keyword):
            self.keyword_i = self.init_keyword_i
            self.init_keyword_i += 1
            keyword = self.get_next_keyword()
            self.accept(keyword)
            return ("", keyword)
        elif self.init_slot_i < len(self.matched_slot):
            self.slot_i = self.init_slot_i
            self.init_slot_i += 1
            slot = self.get_next_slot()
            self.accept(slot)
            return ("$", slot)
        else:
            return None, None
        
    def reset_keyword_i(self):
        self.keyword_i = 0

    def reset_slot_i(self):
        self.slot_i = 0

    def get_next_keyword(self):
        while self.keyword_i < len(self.matched) and self.matched[self.keyword_i][0] <= self.accept_endidx:
            self.keyword_i += 1
        if self.keyword_i < len(self.matched):
            self.keyword_i += 1
            return self.matched[self.keyword_i - 1]

    def get_next_slot(self):
        while self.slot_i < len(self.matched) and self.matched[self.slot_i][0] <= self.accept_endidx:
            self.slot_i += 1
        if self.slot_i < len(self.matched):
            self.slot_i += 1
            return self.matched[self.slot_i - 1]

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
        if files is None: return
        for f in files:
            tag = f.split("/")[-1].split(".")[0]
            self.read_and_insert(f, tag)

    def read_and_insert(self, f, tag):
        for line in open(f):
            line = line.strip()
            exists_flag = self.slot_ac.get(line, None)
            if exists_flag is None:
                if tag not in exists_flag[0]:
                exists_flag[0].append(tag)
                self.slot_ac.add_word(line, (exists_flag, len(line)))
            else:
                self.slot_ac.add_word(line, ([tag], len(line)))

    def init_keyword_ac(self, all_keywords): 
        for k, v in all_keywords.items():
            self.keyword_ac.add_word(k, (v, len(k)))

    def make(self):
        self.slot_ac.make_automaton()
        self.keyword_ac.make_automaton()

    def init(self, all_keywords, files):
        self.init_slot_ac(files)
        self.init_keyword_ac(all_keywords)
        self.make()

    def match(self, dialog):
        matched = self.match_a_ac(self.keyword_ac, dialog, "KEY")
        matched_slot = self.match_a_ac(self.slot_ac, dialog, "REF")
        matched.extend(matched_slot)
        matched.sort(key = lambda x: (x[0], -x[1]) )
        return AC_matched(matched, get_tag_idx_dict(matched))
        
    def match_a_ac(self, A, dialog, word_tp):
        ans = []
        for end_index, (tag, key_length) in A.iter(t):
            start_index = end_index - key_length + 1
            ans.append((start_index, end_index, dialog[start_index: end_index+1], tag, word_tp))
        return ans

    def get_tag_idx_dict(self, key_index):
        ans = {}
        for start_index, end_index, key, tag in key_index:
            val = ans.get(tag, [])
            val.append( (start_index, end_index, key) )
            ans[tag] = val
        return ans
        
