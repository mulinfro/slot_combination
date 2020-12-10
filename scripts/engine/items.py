

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

    def score(self):
        matched_length = len(self.fragments)
        for t in self.fragments:
            matched_length += t[1] - t[0]
        miss_length = self.end - self.begin + 1 - matched_length
        return (matched_length, miss_length)

    def cal_match_score(self, dialog):
        eles = self.tagkey.strip("#").split("#")
        assert len(eles) == len(self.fragments), "Need match"
        frags = []
        for i, idx in enumerate(self.fragments):
            bi, ei = idx[0], idx[1]
            frags.append((dialog[bi: ei + 1], eles[i], bi, ei))

        self.begin =  self.fragments[0][0] 
        self.end   =  self.fragments[-1][1] 
        self.matched = dialog[m.fragments[0][0]: m.fragments[-1][1]+1]
        sv = self.score(self.fragments)
        self.match_score = sv[0] / len(dialog)
        self.miss_score = sv[1] / sv[0]
        self.fragments = frags

    def extract_slots(self, slot_indexes, tnode):
        if not slot_indexes:  return {}
        pre = 0
        idx_slot_map = {}
        print("SLICES", self.tnodes.slices, perm)
        for i in range(len(slices)):
            slot_val = join_tuple(matched_frags[pre: pre + slices[i]], 0)
            pre += slices[i]
            ni = perm[i] if perm else i + 1
            idx_slot_map[ni] = slot_val

        ex_slots = {}
        for slot_name, idx in slot_indexes.items():
            if type(idx) == int:
                ex_slots[slot_name] = idx_slot_map[idx]
            else:
                ex_slots[slot_name] = idx

        return ex_slots
