


class rule_structure():

    def __init__(self, ast):
        self.rule_fingerprint = 


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

    def __init__(self, ast, ):
        self.ast = ast

    def parse(key_index, tag_index):
        ast.

    # 对规则的最长匹配
    def max_match(eles, rules, eat_noise=True):
        tp, matched_idx, matched_tp = "", 0, ""
        for i in range(len(eles)):
            tp += "_" + eles[i]["tp"]
            if tp in rules:
                if rules[tp]:
                    matched_idx = i + 1
                    matched_tp = tp
            else:
                break
        return matched_tp, eles[0:matched_idx], eles[matched_idx:]

    def atom_plus_preprocess(ast, key_index, tag_index, dialog):
        for nm in ast.atom_plus:
            atom_plus_body = ast.ast[nm]["val"]
            tag = atom_plus_body["val"]
            if tag not in tag_index or len(tag_index[tag]) <= 1:
                continue

            the_tag = tag_index[tag]
            # 找到所有的atom plus
            pre_tag_idx = beg_tag_idx = 0
            for i in range(1, len(tag_index[tag])):
                start, end, key = the_tag[i]
                pre_end= the_tag[pre_tag_idx][1] + 1
                if start < pre_end:
                    continue
                elif start == pre_end:
                    pre_tag_idx = i
                    continue

                if i - beg_tag_idx > 1:
                    ss_index, _, _ = the_tag[beg_tag_idx]
                    _, se_index, _ = the_tag[pre_tag_idx]
                    key_index.append( (ss_index, se_index, dialog[ss_index: se_index+1], nm) )

                pre_tag_idx = i
                beg_tag_idx = i

        key_index.sort(key = lambda x: (x[0], -x[1]) )
                    

    def var_plus_preprocess(var_plus, key_index):
        pass


