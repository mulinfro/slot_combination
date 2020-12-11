import config, util

class Selector:

    def __init__(self, matched_items, rules_info):
        self.matched_items = matched_items
        self.rules_info = rules_info

    def extract_slots(self, slot_indexes, slices, perm, matched_frags):
        if not slot_indexes:  return {}
        pre = 0
        idx_slot_map = {}
        for i in range(len(slices)):
            slot_val = util.join_tuple(matched_frags[pre: pre + slices[i]], 0)
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

    def apply_select_strategy(self, items, multi):
        ans = [items[0]]
        intervals = [(items[0].begin, items[0].end)]
        if multi:
            for item in items:
                flag = True
                for interval in intervals:
                    if util.interval_cover((item.begin, item.end), intervals):
                        flag = False
                        break
                if flag:
                    ans.append(item)
                    intervals.append((item.begin, item.end)) 

        return ans

    def apply(self, dialog):
        if len(self.matched_items) == 0: return []
        for m in self.matched_items:
            m.cal_match_score(dialog)
        self.matched_items.sort(key = lambda x: (-x.match_score, x.miss_score))

        candicates = self.apply_select_strategy(self.matched_items, config.MULTI_INTENT)

        selected = []
        for c in candicates:
            diff_slots = {}
            for name, slices, perm in c.tnodes:
                slot_indexes = self.rules_info.slots[name]
                slots = self.extract_slots(slot_indexes, slices, perm, c.fragments)
                diff_slots[name] = slots
            selected.append((c.matched, c.match_score, diff_slots))
        return selected
