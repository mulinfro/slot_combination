from syntax_check import Error
from build_ac import MatchedGroup

def get_list_product_with_slices(lst_of_lst):
    ans = [("", ())]
    for lst in lst_of_lst:
        new_ans = []
        for e, f in ans:
            for e2 in lst:
                if e2 == "": new_ans.append((e, f))
                else:        new_ans.append( (("%s#%s"%(e, e2)).strip("#"), f + (e2,) ))
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


class ExportRulesInfo():

    def __init__(self):
        self.ruleid = rid
        self.out_info = out_info

    def add(self):
        pass


class Signature():

    def __init__(self, sign, tags):
        self.sign = sign
        self.tags = tags


from collections import namedtuple
PlusInfo = namedtuple('PlusInfo', ['plus_name', 'tag_name', 'tag_type'])

class RuleStructure():

    def __init__(self, ast):
        self.rules = ast.rule
        self.plus = self.extract_plus_info(ast)
        self.plus_fingerprint = self.get_plus_sign(ast.plus)
        self.rule_conf = {}
        rules_sign = self.get_sign(ast.rule)
        self.rule_fingerprint, export_tags, self.export_info = self.build_tp_prefixes(rules_sign)
        self.need_delete_tags = self.get_need_delete_tag(export_tags, ast.atom + ast.word_refs + ast.plus)

    # 好像直接返回bd["tp"]就可以了
    def get_ast_body(self, node):
        bd = node["body"]
        return bd
        #if bd["tp"] == "VAR":
        #    return self.rule_graph.ast[bd["name"]]
        #else:
        #    return bd

    def extract_plus_info(self, ast):
        pluses = []
        for ap_name in ast.plus:
            node = self.ast.rule[ap_name]
            bd = self.get_ast_body(node)
            self.rule_conf[ap_name] = node.get("config", {})
            pinfo = PlusInfo(plus_name = ap_name, tag_name = bd["name"], tag_type = bd["tp"])
            pluses.append(pinfo)

        return pluses


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
            return self.get_ele_sign(self.rules[name])

    def get_sign(self, rules):
        all_signs = []
        for nm, bd in rules.items():
            if bd["tp"] == "EXPORT":
                proc = self.export_processer(bd.get("processer", {}))
                rule = bd["body"]
                tp = rule["tp"]
                if tp == "LIST":
                    t = [ self.get_ele_sign(ele) for ele in rule["body"]]
                    ele_sign =  get_list_product_with_slices(t)
                elif tp == "ANGLE":
                    t = [ self.get_ele_sign(ele) for ele in rule["body"]]
                    ele_sign =  get_set_product_with_slices(t)
                else:
                    ele_sign_parts = self.get_ele_sign(rule_body)
                    ele_sign = [(e, (e,)) for e in ele_sign_parts ]

                all_signs.append((ele_sign, proc))

        return all_signs
                
    def get_plus_sign(self, plus):
        all_signs = {}
        for nm in plus:
            signparts = self.get_ele_sign(self.rules[nm]["body"])
            sign = [(e, (e,)) for e in signparts]
            all_signs[nm], _, _ = self.build_tp_prefixes([(sign, None)])

        return all_signs

    def build_tp_prefixes(self, rules):
        export_info = ExportRulesInfo()
        ans, all_tags = {}, set()
        rule_id = 0
        for rs, proc in rules:
            for r, slices in rs:
                rule_id += 1
                eles = r.strip("#").split("#")
                sub_ele = ""
                for ele in eles:
                    all_tags.add(ele.lstrip("012345"))
                    sub_ele += "#" + ele
                    if sub_ele not in ans:
                        ans[sub_ele] = (0, slices)
                # 多个rule有相同的tag序列，会覆盖
                ans[sub_ele] = (rule_id, slices)
                export_info.add(rule_id, proc)

        return ans, all_tags, export_info


class Parse():

    def __init__(self, rule_graph, ac_machine, conf):
        self.rule_graph = rule_graph
        self.conf = conf
        self.ac_machine = ac_machine

    def score(self, _m):
        matched_length = len(_m)
        for t in _m:
            matched_length += t[1] - t[0]

        miss_length = _m[-1][1] - _m[0][0] + 1 - matched_length
        return (matched_length, miss_length)

    def get_match_group(self, tp, _m, dialog):
        eles = tp[1:].split("#")
        sv = self.score(_m)
        assert len(eles) == len(_m), "Need match"
        ans = []
        for i in range(len(_m)):
            b_i, e_i = _m[i][0], _m[i][1] + 1
            ans.append( (dialog[b_i: e_i], eles[i]))

        m_d = dialog[_m[0][0]: _m[-1][1]+1]

        return (m_d, sv[0]/len(dialog), sv[1]/sv[0], ans)


    def select(self, matched, dialog):
        mm = [ self.get_match_group(tp, _m, dialog) for tp, _m in matched]
        mm.sort(key = lambda x: (-x[1], x[2]))
        return mm[0] if mm else None

    def basic_set(self, dialog):
        self.dialog = dialog
        self.AM = self.ac_machine.match(dialog)
        self.plus_preprocess()
        self.AM.matched.sort_tags()
        if len(self.rule_graph.need_delete_tags) > 0:
            self.AM.delete_tag(self.rule_graph.need_delete_tags)
        self.AM.build_word_next_idx(len(dialog))
        #print("AM FINAL", len(self.AM.matched), self.AM.matched)

    def max_match(self, dialog):
        self.basic_set(dialog)
        #print("begining match ...")
        matched_eles = self._greed_match(self.rule_graph.rule_fingerprint, {})
        return self.select(matched_eles, dialog)

    def search_match(self, dialog):
        self.basic_set(dialog)
        conf = self.conf.search
        matched_eles = self._search_match(self.rule_graph.rule_fingerprint, conf)
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
                    elif fingerprint[tp][0] > 0:
                        all_matched.append((tp, head_ele ))

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
                        if fingerprint[new_tp][0] > 0:
                            best_ans.append( (new_tp,  new_matched_eles) )
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
        #print("fingerprint", len(fingerprint) ) 
        for i in range(len(self.AM.matched)):
            ele = self.AM.iter_init_status(i)
            for tag in ele.tags:
                tp = "%s#%s%s"%("", ele.tag_type, tag)
                if tp in fingerprint:
                    head_ele = ((ele.start, ele.end), )
                    matched_ans = self._greed_match_helper(tp, head_ele, fingerprint, conf)
                    if matched_ans:
                        all_matched.extend(matched_ans)
                    elif fingerprint[tp][0] > 0:
                        all_matched.append((tp, head_ele ))

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
                        if fingerprint[new_tp][0] > 0:
                            best_ans.append((new_tp,  new_matched_eles))
                        stack.append((new_tp, self.AM.save_state(), new_matched_eles ))

        return best_ans

    def plus_preprocess(self):
        for plus_name, tag_name, tag_type in self.rule_graph.plus:
            conf = self.rule_graph.rule_conf[plus_name]
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
                    self.AM.matched.append( MatchedGroup(ss_index, se_index, tag, "2") )

                pre_tag_idx = i
                beg_tag_idx = i
                cnt = 1

        if cnt >= conf["min_N"]:
            self.AM.matched.append(MatchedGroup(ids_of_tag[beg_tag_idx][0], ids_of_tag[pre_tag_idx][1], tag, "2") )

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
                    ans.append(MatchedGroup(lst[b_i][0], lst[p_i][1], tag, "2")  )

                p_i = b_i =  i
                cnt = 1

        if len(lst) and cnt >= conf["min_N"]:
            ans.append(MatchedGroup(lst[b_i][0], lst[p_i][1], tag, "2")  )

        return ans

    def merge_eles(self, lst):
        ans = []
        for tp, idxes in lst:
            t = 0
            for b,e in idxes:
                t += b-e +1
            ans.append( (idxes[0][0], idxes[-1][1], idxes[-1][1] - idxes[0][0] + 1 - t ))

        return ans

    def merge_ele(self, ele, b_idx, e_idx):
        return (ele[0], e_idx, ele[2] + b_idx - ele[1] -1)

    def var_plus_preprocess(self, rule_name, conf):
        figerprint = self.rule_graph.plus_fingerprint[rule_name]
        all_matched = self._greed_match(figerprint, conf)
        all_plus = self.plus_extract(self.merge_eles(all_matched), [rule_name], conf)
        self.AM.matched.extend(all_plus)


