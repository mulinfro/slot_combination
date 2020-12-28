import config, util
from post_handle import apply_post, get_idx_slot


class Selector:

    def __init__(self, matched_items, special_post, rules_info):
        self.matched_items = matched_items
        self.special_post = special_post
        self.rules_info = rules_info

    def apply_select_strategy(self, items, multi):
        ans = [items[0]]
        intervals = [(items[0].begin, items[0].end)]
        if multi:
            for item in items:
                if not util.interval_cover((item.begin, item.end), intervals):
                    ans.append(item)
                    intervals.append((item.begin, item.end))

        return ans

    def apply(self, dialog):
        if len(self.matched_items) == 0: return []
        for m in self.matched_items:
            m.cal_match_score(dialog)
        self.matched_items.sort(key = lambda x: (-x.match_score, x.fuzzy_degree))

        candicates = self.apply_select_strategy(self.matched_items, config.MULTI_INTENT)

        selected = []
        for c in candicates:
            diff_slots = {}
            for name, slices, perm in c.tnodes:
                slot_indexes, pfunc, _ = self.rules_info.get(name)
                idx_slot_map = get_idx_slot(slices, perm, c.fragments, self.special_post)
                slots = apply_post(slot_indexes, pfunc, idx_slot_map)
                diff_slots[name] = slots
            selected.append((c.matched, c.match_score, diff_slots))
        return selected
