


class Rule_structure():

    def __init__(self, ast):
        self.rule_fingerprint = {}
        self.atom_plus = []
            atom_plus_body = ast.ast[nm]["val"]
            tag = atom_plus_body["val"]

    def get_rule_sign(self, ast):
        all_signs = []
        for nm, bd in ast.items():
            if bd["tp"] == "EXPORT":
                ele_names = []
                for ele in bd["body"]:
                    if ele["tp"] == "REF":
                        ele_names.append( "$" + ele["name"] )
                    else:
                        ele_names.append( ele["name"] )
                    
            all_signs.append( "_".join(ele_names) )
        return all_signs
                

    def build_tp_prefixes(rules):
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

    def match(dialog):
        ac_matched_ans = self.ac_machine.match(dialog)
        self.atom_plus_preprocess(dialog, ac_matched_ans)
        self.var_plus_preprocess(dialog, ac_matched_ans)
        while True:
            self.max_match(dialog, begin_idx ac_matched_ans)

    # 对规则的最长匹配
    def max_match(dialog, begin_idx, AM):
        tp, matched_idx, matched_tp = "", 0, ""
        while True:
            ele_tp, ele = AM.get_valid_keyword_or_slot()
            tp += "_" + ele_tp
            if tp in self.rule_fingerprint:
                if self.rule_fingerprint[tp]:
                    matched_idx = i + 1
                    matched_tp = tp
            else:
                break
        return matched_tp, eles[0:matched_idx], eles[matched_idx:]

    def atom_plus_preprocess(dialog, AM):
        tag_index = AM.keyword_tag_index
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
                    AM.matched_keyword.append( (ss_index, se_index, dialog[ss_index: se_index+1], nm) )

                pre_tag_idx = i
                beg_tag_idx = i

        AM.matched_keyword.sort(key = lambda x: (x[0], -x[1]) )
                    

    def var_plus_preprocess(dialog, AM):
        for vp_name, vp_tag in self.rule_graph.var_plus:
            mm = find_all_vars(AM, vp_tag)
            if not mm: continue

        


