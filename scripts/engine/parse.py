


class Rule_structure():

    def __init__(self, ast):
        self.rule_fingerprint = self.build_tp_prefixes(ast)
        self.atom_plus = self.build_atom_plus(ast)

    def build_atom_plus(self, ast):
        ans = []
        for nm in ast.atom_plus:
            atom_plus_body = ast.ast[nm]["val"]
            tag = atom_plus_body["val"]
            ans.append( (nm, tag))
        return ans

    def get_rule_sign(self, ast):
        all_signs = []
        for nm, bd in ast.ast.items():
            if bd["tp"] == "EXPORT":
                ele_names = []
                for ele in bd["body"]:
                    if ele["tp"] == "REF":
                        ele_names.append( "$" + ele["name"] )
                    else:
                        ele_names.append( ele["name"] )
                    
            all_signs.append( "_".join(ele_names) )
        return all_signs
                

    def build_tp_prefixes(self, ast):
        rules = self.get_rule_sign(ast)
        ans = {}
        for r in rules:
            eles = r.split("_")
            sub_ele = ""
            for ele in eles:
                sub_ele += "_" + ele
                if sub_ele not in ans:
                    ans[sub_ele] = 0
            ans[sub_ele] = 1
        return ans


class Parse():

    def __init__(self, rule_graph, ac_machine, config):
        self.rule_graph = rule_graph
        self.ac_machine = ac_machine
        self.config = config

    def score(self, matched):
        pass

    def select(self, matched):
        pass

    def match(self, dialog):
        ac_matched_ans = self.ac_machine.match(dialog)
        self.plus_preprocess(dialog, ac_matched_ans)
        #self.atom_plus_preprocess(dialog, ac_matched_ans)
        #self.var_plus_preprocess(dialog, ac_matched_ans)
        all_matched = []
        while True:
            tp, ele = ac_matched_ans.iter_init_status()
            if tp is None: break
            if tp in self.rule_fingerprint:
                if self.rule_fingerprint[tp]:
                    all_matched.append( (tp, ele))
                matched_tp, best_ans = self.max_match(dialog, ac_matched_ans)
                if best_ans is not None:
                    all_matched.append( (matched_tp, best_ans))

        return self.select(all_matched)

    # 对规则的最长匹配
    def max_match(self, dialog, AM):
        tp, matched_eles, matched_tp = "", [], ""
        best_ans = None
        while True:
            tag_type, ele = AM.get_next_keyword_or_slot()
            if tag_type is None: break
            if len(ele[3]) == 1: ""
            for ele_tp in ele[3]:
                new_tp = "%s_%s%s"%(tp, tag_type, ele_tp)
                if new_tp in self.rule_fingerprint:
                    matched_eles.append(ele)
                    tp = new_tp
                    AM.accept(ele)
                    if self.rule_fingerprint[new_tp]:
                        matched_tp = new_tp
                        best_ans = matched_eles[0:]

        return matched_tp, best_ans

    def greed_match(self, dialog):
        pass

    def plus_preprocess(self, dialog, AM, tp = "keyword"):
        for ap_name in self.rule_graph.plus:
            node = self.ast[ap_name]
            tp = node["body"]["tp"]
            if tp == "ATOM":
                self.atom_plus_preprocess(dialog, AM, "keyword")
            elif  tp == "REF":
                self.ref_plus_preprocess(dialog, AM, "slot")
            else:
                self.var_plus_preprocess(dialog, AM)

        AM.matched_keyword.sort(key = lambda x: (x[0], -x[1]) )
        
    def atom_plus_preprocess(self, dialog, AM, tp = "keyword"):
        if tp == "keyword":
            tag_index = AM.keyword_tag_index
        else:
            tag_index = AM.slot_tag_index
        for ap_name, ap_tag in self.rule_graph.atom_plus:
            if ap_tag not in tag_index or len(tag_index[ap_tag]) <= 1:
                continue

            ids_of_tag = tag_index[ap_tag]
            # 找到所有的atom plus
            pre_tag_idx = beg_tag_idx = 0
            for i in range(1, len(tag_index[ap_tag])):
                start, end, key = ids_of_tag[i]
                pre_end= ids_of_tag[pre_tag_idx][1] + 1
                if start < pre_end:
                    continue
                elif start == pre_end:
                    pre_tag_idx = i
                    continue

                if i - beg_tag_idx > 1:
                    ss_index, _, _ = ids_of_tag[beg_tag_idx]
                    _, se_index, _ = ids_of_tag[pre_tag_idx]
                    AM.matched_keyword.append( (ss_index, se_index, dialog[ss_index: se_index+1],ap_name) )

                pre_tag_idx = i
                beg_tag_idx = i

    def var_plus_preprocess(self, dialog, AM, rule_name):
        ans = []
        mm = self.match_plus(AM, rule_name)
        if mm:
            ans.extend(mm)
        AM.matched_keyword.append( (ss_index, se_index, dialog[ss_index: se_index+1],ap_name) )

    def match_atom(self, AM, ele):
        while True:
            mc = AM.get_next_keyword()
            if not mc: break
            dist = Am.get_word_dist(mc[0])
            if dist > CONF.maxdist: break
            if mc[3] == e["name"]:
                AM.accept(mc)
                return (mc, dist)

        return (None, None)

    # 可能需要考虑所有匹配到的, 然后动态规划; 
    # 目前先优先选择候选集合中长的
    def match_ref(self, AM, ele):
        candi = []
        while True:
            mc = AM.get_next_slot()
            if not mc: break
            dist = Am.get_word_dist(mc[0])
            if dist > CONF.maxdist: break
            if mc[3] == e["name"]:
                candi.append(mc)

        return select_max_length(candi)

    def match_plus(self, AM, ele):
        ans = []
        while True:
            _m = match_one_rule()
            if _m: ans.append(_m)
            else: break

        return ans
        
    def match_one_rule(self, AM, rule_name):
        rule = self.rule_graph.ast[rule_name]
        tp = rule["tp"]
        if tp == "PLUS":
            elif
        total_dis = 0
        ans = []
        for e in rlue_body:
            if e["tp"] == "ATOM":
                _m = self.match_atom(AM, e)
            elif e["tp"] == "REF":
                _m = self.match_ref(AM, e)
            elif e["tp"] == "PLUS":
                _m = self.match_plus()
            elif e["tp"] == "RULE":
                _m = self.match_one_rule()
            else:
                _m = None

            if _m: ans.append(_m)
            else: return []
        return ans
