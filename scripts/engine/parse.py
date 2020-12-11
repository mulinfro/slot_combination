from syntax_check import Error
from build_ac import AcMatchedGroup
import config, util
from items import *

def count_tag_num(e):
    if not e: t = 0
    else:     t = e.count("#") + 1
    return t

def get_list_product_with_slices(lst_of_lst, perm = None):
    ans = [("", (), perm)]
    for lst in lst_of_lst:
        new_ans = []
        for e, f, _ in ans:
            for e2 in lst:
                if e2 == "":
                    new_ans.append((e, f + (0,), perm))
                else:
                    new_ans.append((("%s#%s"%(e, e2)).strip("#"), f + (count_tag_num(e2),), perm))
        ans = new_ans
    return ans


def get_list_product(lst_of_lst):
    ans = [""]
    for lst in lst_of_lst:
        new_ans = []
        for e in ans:
            for e2 in lst:
                if e2 == "": new_ans.append(e)
                else:        new_ans.append(("%s#%s"%(e, e2)).strip("#"))
        ans = new_ans
    return ans

def get_list_permutation(perm, lst):
    new_lst = []
    for p in perm:
        new_lst.append(lst[p - 1])
    return new_lst

def get_set_product(lst_of_lst):
    from itertools import permutations
    ans = []
    for p_lst in permutations(lst_of_lst):
        ans.extend(get_list_product(p_lst))

    return list(set(ans))

def get_set_product_with_slices(lst_of_lst):
    from itertools import permutations
    ans = []
    enum = list(range(1, len(lst_of_lst) + 1))
    for perm in permutations(enum):
        p_lst = get_list_permutation(perm, lst_of_lst)
        ans.extend(get_list_product_with_slices(p_lst, perm=perm))

    return list(set(ans))


def join_tuple(lst, idx):
    t = [e[idx] for e in lst]
    return "".join(t)


class TrieNodeInfo():
    def __init__(self):
        self.match_list = []
        self.leafFlag = False

    def isLeaf(self):
        return leafFlag

    def remove_zero(self, lst):
        ans = []
        for a,b in lst:
            if a != 0:
                ans.append((a,b))

        return tuple(ans)

    def isSameNode(self, nodel, noder):
        if nodel.name == noder.name:
            if nodel.permutation is None or noder.permutation is None:
                return nodel.permutation == noder.permutation and nodel.slices == noder.slices
            else:
                lft = self.remove_zero(zip(nodel.slices, nodel.permutation))
                rht = self.remove_zero(zip(noder.slices, noder.permutation))
                return lft == rht

        return False

    def setLeaf(self, flag = True):
        self.leafFlag =  flag

    def addRule(self, name, slices, permutation):
        tn = TNode(name = name, slices = slices, permutation = permutation)
        self.setLeaf()
        for n in self.match_list:
            if self.isSameNode(n, tn):
                return

        self.match_list.append(tn)

# Trie implement by hashtable
class RuleTrie():
    def __init__(self, export_trie, plus_tries, to_dele_tags, post_info, conf):
        self.export_trie = export_trie
        self.plus_tries = plus_tries
        self.need_delete_tags = to_dele_tags
        self.rule_conf = conf
        self.post_info = post_info


class RuleStructure():

    def __init__(self, ast):
        self.ast = ast
        self.rules_body = ast.rules_body
        self.rule_id = 0

    def build_trie(self, names):
        rules_sign = self.get_sign(names)
        fingerprint, tags = self.build_tp_prefixes(rules_sign)
        return fingerprint, tags

    def build(self):
        plus_tries = []
        for p in self.ast.plus:
            ptrie, _ = self.build_trie([p])
            plus_tries.append((p, ptrie))

        export_trie, export_tags = self.build_trie(self.ast.export)
        need_delete_tags = self.get_need_delete_tag(export_tags, self.ast.atom + self.ast.word_refs + self.ast.plus)
        return RuleTrie(export_trie, plus_tries, need_delete_tags, self.ast.post_info, self.ast.config)

    def get_need_delete_tag(self, export_tags, all_tags):
        ans = set()
        for t in all_tags:
            if t not in export_tags:
                ans.add(t)

        return ans

    def get_ele_sign(self, rule):
        tp = rule["tp"]
        if tp == "ATOM":
            return ["0" + rule["name"]]
        elif tp == "REF":
            return ["1" + rule["name"]]
        elif tp == "PLUS":
            return ["2" + rule["name"]]
        elif tp == "RULE":
            return self.get_ele_sign(rule["body"])
        elif tp == "OR":
            t = []
            for ele in rule["body"]:
                t.extend(self.get_ele_sign(ele))
            return t
        elif tp == "OR_?":
            t =  self.get_ele_sign(rule["body"])
            t.append("")
            return t
        elif tp == "LIST":
            t = [ self.get_ele_sign(ele) for ele in rule["body"]]
            return get_list_product(t)
        elif tp == "ANGLE":
            t = [ self.get_ele_sign(ele) for ele in rule["body"]]
            return get_set_product(t)
        elif tp == "VAR":
            name = rule["name"]
            return self.get_ele_sign(self.rules_body[name])

    def get_sign(self, names):
        all_signs = []
        for nm in names:
            rule = self.rules_body[nm]["body"]
            tp = rule["tp"]
            if tp == "LIST":
                t = [ self.get_ele_sign(ele) for ele in rule["body"]]
                ele_sign = get_list_product_with_slices(t)
            elif tp == "ANGLE":
                t = [ self.get_ele_sign(ele) for ele in rule["body"]]
                ele_sign = get_set_product_with_slices(t)
            else:
                ele_sign_parts = self.get_ele_sign(rule)
                ele_sign = [(e, (count_tag_num(e), ), None) for e in ele_sign_parts ]

            all_signs.append((ele_sign, nm))

        return all_signs
                

    def build_tp_prefixes(self, rules):
        ans, all_tags = {}, set()
        for rs, nm in rules:
            for r, slices, permutation in rs:
                self.rule_id += 1
                eles = r.strip("#").split("#")
                sub_ele = ""
                for ele in eles:
                    all_tags.add(ele.lstrip("012345"))
                    sub_ele += "#" + ele
                    if sub_ele not in ans:
                        ans[sub_ele] = TrieNodeInfo()
                # 多个rule有相同的tag序列，会覆盖
                ans[sub_ele].addRule(nm, slices, permutation)

        return ans, all_tags


class Parse():

    def __init__(self, rule_trie, ac_machine):
        self.rule_trie = rule_trie
        self.ac_machine = ac_machine

    def extract_slots(self, slot_indexes, slices, perm, matched_frags):
        if not slot_indexes:  return {}
        pre = 0
        idx_slot_map = {}
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

    def select(self, matched_items, dialog):
        if len(matched_items) == 0: return []
        for m in matched_items:
            m.cal_match_score(dialog)
        matched_items.sort(key = lambda x: (-x.match_score, x.miss_score))

        candicates = self.apply_select_strategy(matched_items, config.MULTI_INTENT)

        matched = []
        for c in candicates:
            for name, slices, perm in c.tnodes:
                slot_indexes = self.rule_trie.post_info[name].slots
                slots = self.extract_slots(slot_indexes, slices, perm, c.fragments)
                matched.append((c.matched, name, slots))
        return matched

    def basic_set(self, dialog):
        self.dialog = dialog
        self.AM = self.ac_machine.match(dialog)
        self.plus_preprocess()
        self.AM.sort_tags()
        if len(self.rule_trie.need_delete_tags) > 0:
            self.AM.delete_tag(self.rule_trie.need_delete_tags)
        self.AM.build_word_next_idx(len(dialog))

    def max_match(self, dialog):
        self.basic_set(dialog)
        conf = config.get_conf(None, "search")
        matched_eles = self._greed_match(self.rule_trie.export_trie, conf)
        return self.select(matched_eles, dialog)

    def search_match(self, dialog):
        self.basic_set(dialog)
        conf = config.get_conf(None, "search")
        matched_eles = self._search_match(self.rule_trie.export_trie, conf)
        return self.select(matched_eles, dialog)
        
    def _search_match(self, fingerprint, conf):
        self.AM.reset()
        all_matched = []
        has_seen = set()
        for i in range(len(self.AM.matched)):
            ele = self.AM.iter_init_status(i)
            for tag in ele.tags:
                tp = "%s#%s%s"%("", ele.tag_type, tag)
                if tp in fingerprint:
                    head_ele = ((ele.start, ele.end), )
                    matched_ans = self._search_match_helper(tp, head_ele, fingerprint, has_seen, conf)
                    if matched_ans:
                        all_matched.extend(matched_ans)
                    elif fingerprint[tp].isLeaf:
                        all_matched.append(MatchedItem(tp, head_ele, fingerprint[tp].match_list))

        return all_matched


    # 对规则的最长匹配
    def _search_match_helper(self, tp, matched_eles, fingerprint, has_seen, conf):
        best_ans = []
        stack = [(tp, self.AM.save_state(), matched_eles)]
        while len(stack):
            tp, state, matched_eles = stack.pop(0)
            self.AM.restore_state(state)
            is_accept = False
            while not is_accept and self.AM.has_next():
                ele = self.AM.get_next()

                # 大于限定距离; break
                if self.AM.get_word_dist(ele.start) > conf["max_dist"]:
                    break

                for tag in ele.tags:
                    new_tp = "%s#%s%s"%(tp, ele.tag_type, tag)
                    search_step_fingerprint = "%d&%s"%(self.AM._i, new_tp)
                    if search_step_fingerprint in has_seen: continue

                    has_seen.add(search_step_fingerprint)
                    if new_tp in fingerprint:
                        #self.AM.accept(ele)
                        #is_accept = True
                        new_matched_eles = matched_eles + ((ele.start, ele.end),)
                        # simple
                        # new_matched_eles = self.merge_ele(matched_eles, ele[0], ele[1] )
                        if fingerprint[new_tp].isLeaf:
                            best_ans.append(MatchedItem(new_tp,  new_matched_eles, fingerprint[new_tp].match_list))
                            # 到达最后一个且匹配到就没要再搜索下去
                            #print(ele, new_matched_eles)
                            """
                            print(ele, new_matched_eles)
                            if not self.AM.has_next():  
                                print("NO HEAS")
                                return best_ans
                            """

                        stack.append((new_tp, (self.AM._i, ele.end), new_matched_eles ) )
                    elif conf["no_skip_atom"] and ele.tag_type in "0":
                        break_flag = True
                        # 中间有atom， 且不准跨越atom
                        break
                    elif conf["no_skip_any"]:
                        break

        return best_ans

    def _greed_match(self, fingerprint, conf):
        self.AM.reset()
        all_matched = []
        for i in range(len(self.AM.matched)):
            ele = self.AM.iter_init_status(i)
            for tag in ele.tags:
                tp = "%s#%s%s"%("", ele.tag_type, tag)
                if tp in fingerprint:
                    head_ele = ((ele.start, ele.end), )
                    matched_ans = self._greed_match_helper(tp, head_ele, fingerprint, conf)
                    if matched_ans:
                        all_matched.extend(matched_ans)
                    elif fingerprint[tp].isLeaf:
                        all_matched.append(MatchedItem(tp, head_ele, fingerprint[tp].match_list))

        return all_matched


    # 对规则的最长匹配
    def _greed_match_helper(self, tp, matched_eles, fingerprint, conf):
        best_ans = []
        stack = [(tp, self.AM.save_state(), matched_eles)]
        while len(stack):
            tp, state, matched_eles = stack.pop(0)
            self.AM.restore_state(state)
            is_accept = False
            while not is_accept and self.AM.has_next():
                ele = self.AM.get_next()
                #if self.get_word_dist(ele[0]) > self.conf.max_match_dist:
                #    break

                for tag in ele.tags:
                    new_tp = "%s#%s%s"%(tp, ele.tag_type, tag)
                    if new_tp in fingerprint:
                        self.AM.accept(ele)
                        is_accept = True
                        new_matched_eles = matched_eles + ((ele.start, ele.end), )
                        # simple
                        if fingerprint[new_tp].isLeaf:
                            best_ans.append(MatchedItem(new_tp, new_matched_eles, fingerprint[new_tp].match_list))
                        stack.append((new_tp, self.AM.save_state(), new_matched_eles ))

        return best_ans

    def plus_preprocess(self):
        for pname, trie in self.rule_trie.plus_tries:
            cname = self.rule_trie.rule_conf.get(pname, "")
            conf = config.get_conf(cname, "plus")
            matched_items = self._greed_match(trie, conf)
            if matched_items:
                for m in matched_items:  m.cal_index()
                all_plus = self.plus_extract(matched_items, [pname], conf)
                self.AM.matched.extend(all_plus)

    def plus_extract(self, lst, tag, conf):
        ans = []
        p_i = b_i = 0
        cnt = 1
        for i in range(1, len(lst)):
            start, end = lst[i].begin, lst[i].end
            pre_end= lst[p_i].end
            if end <= pre_end: continue

            m_dist = start - pre_end
            if m_dist > 0 and m_dist <= conf["max_dist"] + 1:
                p_i = i
                cnt += 1
            elif m_dist > conf["max_dist"] + 1 or (m_dist <= 0 and conf["no_cover"] ):
                if cnt >= conf["min_N"]:
                    ans.append(AcMatchedGroup(lst[b_i].begin, lst[p_i].end, tag, "2")  )

                p_i = b_i =  i
                cnt = 1

        if len(lst) and cnt >= conf["min_N"]:
            ans.append(AcMatchedGroup(lst[b_i].begin, lst[p_i].end, tag, "2")  )

        return ans


