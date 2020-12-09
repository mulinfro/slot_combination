from syntax_check import Error
from build_ac import AcMatchedGroup
import config

from collections import namedtuple

RuleMatched = namedtuple('RuleMatched', ['tagkey', 'fragments', 'tnodes'])

def count_tag_num(e):
    if not e: t = 0
    else:     t = e.count("#") + 1
    return t

def get_list_product_with_slices(lst_of_lst):
    ans = [("", ())]
    for lst in lst_of_lst:
        new_ans = []
        for e, f in ans:
            for e2 in lst:
                if e2 == "": new_ans.append((e, f))
                else:        new_ans.append((("%s#%s"%(e, e2)).strip("#"), f + (count_tag_num(e2),) ))
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

def get_set_product(lst_of_lst):
    from itertools import permutations
    ans = []
    for p_lst in permutations(lst_of_lst):
        ans.extend(get_list_product(p_lst))

    return list(set(ans))

def get_set_product_with_slices(lst_of_lst):
    from itertools import permutations
    ans = []
    for p_lst in permutations(lst_of_lst):
        ans.extend(get_list_product_with_slices(p_lst))

    return list(set(ans))


def join_tuple(lst, idx):
    t = [e[idx] for e in lst]
    return "".join(t)

class ExportRulesInfo():

    def __init__(self):
        self.ruleid = rid
        self.out_info = out_info

    def add(self, rid, info):
        pass


TNode = namedtuple('TNode', ['name', 'slices'])

class TrieNodeInfo():
    def __init__(self):
        self.match_list = []
        self.leafFlag = False

    def isLeaf(self):
        return leafFlag

    def setLeaf(self, flag = True):
        self.leafFlag =  flag

    def addRule(self, name, slices):
        tn = TNode(name = name, slices = slices)
        self.setLeaf()
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
        self.rule_conf = {}
        self.rule_id = 0

    def build_trie(self, names):
        rules_sign = self.get_sign(names)
        fingerprint, tags = self.build_tp_prefixes(rules_sign)
        return fingerprint, tags

    def build(self):
        plus_tries = []
        for p in self.ast.plus:
            ptrie, _ = self.build_trie([p])
            plus_tries.append(ptrie)

        export_trie, export_tags = self.build_trie(self.ast.export)
        need_delete_tags = self.get_need_delete_tag(export_tags, self.ast.atom + self.ast.word_refs + self.ast.plus)
        return RuleTrie(export_trie, plus_tries, need_delete_tags, self.ast.post_info, self.rule_conf)

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
                ele_sign =  get_list_product_with_slices(t)
            elif tp == "ANGLE":
                t = [ self.get_ele_sign(ele) for ele in rule["body"]]
                ele_sign =  get_set_product_with_slices(t)
            else:
                ele_sign_parts = self.get_ele_sign(rule)
                ele_sign = [(e, (e,)) for e in ele_sign_parts ]

            all_signs.append((ele_sign, nm))

        return all_signs
                

    def build_tp_prefixes(self, rules):
        ans, all_tags = {}, set()
        for rs, nm in rules:
            for r, slices in rs:
                self.rule_id += 1
                eles = r.strip("#").split("#")
                sub_ele = ""
                for ele in eles:
                    all_tags.add(ele.lstrip("012345"))
                    sub_ele += "#" + ele
                    if sub_ele not in ans:
                        ans[sub_ele] = TrieNodeInfo()
                # 多个rule有相同的tag序列，会覆盖
                ans[sub_ele].addRule(nm, slices)

        return ans, all_tags


class Parse():

    def __init__(self, rule_trie, ac_machine, conf):
        self.rule_trie = rule_trie
        self.conf = conf
        self.ac_machine = ac_machine

    def score(self, _m):
        matched_length = len(_m)
        for t in _m:
            matched_length += t[1] - t[0]

        miss_length = _m[-1][1] - _m[0][0] + 1 - matched_length
        return (matched_length, miss_length)

    def get_match_group(self, m, dialog):
        eles = m.tagkey.strip("#").split("#")
        sv = self.score(m.fragments)
        assert len(eles) == len(m.fragments), "Need match"
        frags = []
        for i, idx in enumerate(m.fragments):
            bi, ei = idx[0], idx[1] + 1
            frags.append((dialog[bi: ei], eles[i]))

        m_d = dialog[m.fragments[0][0]: m.fragments[-1][1]+1]

        return (m_d, sv[0]/len(dialog), sv[1]/sv[0], frags, m.tnodes)


    def extract_slots(self, slot_indexes, slices, matched_frags):
        if not slot_indexes:  return {}
        pre = 0
        idx_slot_map = {}
        for i in range(len(slices)):
            slot_val = join_tuple(matched_frags[pre: pre + slices[i]], 0)
            pre += slices[i]
            idx_slot_map[i + 1] = slot_val

        ex_slots = {}
        for slot_name, idx in slot_indexes.items():
            if type(idx) == int:
                ex_slots[slot_name] = idx_slot_map[idx]
            else:
                ex_slots[slot_name] = idx

        return ex_slots

    def select(self, matched, dialog):
        mm = [ self.get_match_group(m, dialog) for m in matched]
        mm.sort(key = lambda x: (-x[1], x[2]))
        if len(mm) > 0:
            matched = []
            for name, slices in mm[0][4]:
                slot_indexes = self.rule_trie.post_info[name].slots
                slots = self.extract_slots(slot_indexes, slices, mm[0][3])
                matched.append((mm[0], name, slots))
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
        matched_eles = self._greed_match(self.rule_trie.export_trie, {})
        return self.select(matched_eles, dialog)

    def search_match(self, dialog):
        self.basic_set(dialog)
        conf = self.conf.search
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
                        all_matched.append(RuleMatched(tp, head_ele, fingerprint[tp].match_list))

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
                        #print(ele, new_matched_eles, new_tp)
                        if fingerprint[new_tp].isLeaf:
                            best_ans.append(RuleMatched(new_tp,  new_matched_eles, fingerprint[new_tp].match_list))
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


    def _double_greed_macth(self):
        pass

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
                        all_matched.append(RuleMatched(tp, head_ele, fingerprint[tp].match_list))

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
                        # new_matched_eles = self.merge_ele(matched_eles, ele[0], ele[1] )
                        if fingerprint[new_tp].isLeaf:
                            best_ans.append(RuleMatched(new_tp,  new_matched_eles, fingerprint[new_tp].match_list))
                        stack.append((new_tp, self.AM.save_state(), new_matched_eles ))

        return best_ans

    def plus_preprocess(self):
        for trie in self.rule_trie.plus_tries:
            #conf = self.rule_trie.rule_conf[plus_name]
            _conf = config.Config()
            conf =  _conf.atom_plus
            all_matched = self._greed_match(trie, conf)
            matched_items, tags = self.merge_eles(all_matched)
            all_plus = self.plus_extract(matched_items, [tags[0].name], conf)
            self.AM.matched.extend(all_plus)

    def plus_extract(self, lst, tag, conf):
        ans = []
        p_i = b_i = 0
        cnt = 1
        for i in range(1, len(lst)):
            start, end, _ = lst[i]
            pre_end= lst[p_i][1]
            if end <= pre_end: continue

            m_dist = start - pre_end
            if m_dist > 0 and m_dist <= conf["max_dist"] + 1:
                p_i = i
                cnt += 1
            elif m_dist > conf["max_dist"] + 1 or (m_dist <= 0 and conf["no_cover"] ):
                if cnt >= conf["min_N"]:
                    ans.append(AcMatchedGroup(lst[b_i][0], lst[p_i][1], tag, "2")  )

                p_i = b_i =  i
                cnt = 1

        if len(lst) and cnt >= conf["min_N"]:
            ans.append(AcMatchedGroup(lst[b_i][0], lst[p_i][1], tag, "2")  )

        return ans

    def merge_eles(self, lst):
        # new_tp,  new_matched_eles(), match_list
        ans = []
        match_list = []
        for tp, idxes, ml in lst:
            match_list = ml
            t = 0
            for b,e in idxes:
                t += b-e +1
            ans.append( (idxes[0][0], idxes[-1][1], idxes[-1][1] - idxes[0][0] + 1 - t ))

        return ans, match_list

    def merge_ele(self, ele, b_idx, e_idx):
        return (ele[0], e_idx, ele[2] + b_idx - ele[1] -1)

    ### plus preprocess


    def plus_preprocess_bak(self):
        for plus_name, tag_name, tag_type in self.rule_trie.plus:
            conf = self.rule_trie.rule_conf[plus_name]
            if tag_type == "ATOM":
                self.atom_plus_preprocess(tag_name, [plus_name], conf, "keyword")
            elif  tag_type == "REF":
                self.atom_plus_preprocess(tag_name, [plus_name], conf, "slot")
            else:
                self.var_plus_preprocess(plus_name, conf)

    def atom_plus_preprocess(self, ap_tag, tag, conf, tp = "keyword"):
        tag_index = self.AM.word_tag_index
        if ap_tag not in tag_index or len(tag_index[ap_tag]) < conf["min_N"]:
            return None

        ids_of_tag = tag_index[ap_tag]
        # 找到所有的atom plus
        pre_tag_idx = beg_tag_idx = 0
        cnt = 1
        for i in range(1, len(ids_of_tag)):
            start, end, _ = ids_of_tag[i]
            pre_end= ids_of_tag[pre_tag_idx][1]
            if end <= pre_end:
                continue

            m_dist = start - pre_end
            if m_dist > 0 and m_dist <= conf["max_dist"] + 1:
                pre_tag_idx = i
                cnt += 1
            elif m_dist > conf["max_dist"] + 1 or (m_dist <= 0 and conf["no_cover"] ) :
                if cnt >= conf["min_N"]:
                    ss_index, _, _ = ids_of_tag[beg_tag_idx]
                    _, se_index, _ = ids_of_tag[pre_tag_idx]
                    self.AM.matched.append(AcMatchedGroup(ss_index, se_index, tag, "2") )

                pre_tag_idx = i
                beg_tag_idx = i
                cnt = 1

        if cnt >= conf["min_N"]:
            self.AM.matched.append(AcMatchedGroup(ids_of_tag[beg_tag_idx][0], ids_of_tag[pre_tag_idx][1], tag, "2") )

