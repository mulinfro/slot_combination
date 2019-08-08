import ahocorasick

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
        matched_keyword = self.match_a_ac(self.keyword_ac, dialog)
        matched_slot = self.match_a_ac(self.slot_ac, dialog)
        return (matched_keyword, matched_slot, get_tag_idx_dict(matched_keyword), get_tag_idx_dict(matched_slot))
        
    def match_a_ac(self, A, dialog):
        ans = []
        for end_index, (tag, key_length) in A.iter(t):
            start_index = end_index - key_length + 1
            ans.append((start_index, end_index, dialog[start_index: end_index+1], tag))
        ans.sort(key = lambda x: (x[0], -x[1]) )
        return ans

    def get_tag_idx_dict(self, key_index):
        ans = {}
        for start_index, end_index, key, tag in key_index:
            val = ans.get(tag, [])
            val.append( (start_index, end_index, key) )
        return ans
        
