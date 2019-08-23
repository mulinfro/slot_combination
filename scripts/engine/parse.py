


class Rule_structure():

    def __init__(self, ast, ac_machine, config):
        self.ast = ast.ast
        self.plus = ast.plus
        self.rule_fingerprint = self.build_tp_prefixes(ast)
        self.ac_machine = ac_machine
        self.config = config

    """
    def build_atom_plus(self, ast):
        ans = []
        for nm in ast.atom_plus:
            atom_plus_body = ast.ast[nm]["val"]
            tag = atom_plus_body["val"]
            ans.append( (nm, tag))
        return ans

    """

    def get_one_rule_sign(self, rule):
        tp = rule["tp"]
        body = rule["body"]
        if body["tp"] == "LIST":
            return self.get_rule_list_sign(rule)

        return ""
             
    def get_rule_list_sign(self, rule):
        ans = []
        for ele in rule["body"]:
            t = self.get_rule_ele_sign(ele)
            ans.append(t)
        return "_".join(ans)

    def get_rule_ele_sign(self, rule):
        tp = rule["tp"]
        if tp == "ATOM":
            return "0" + tp["name"]
        elif tp == "REF":
            return "1" + tp["name"]
        elif tp == "PLUS":
            return "2" + tp["name"]
        elif tp == "RULE":
            body = tp["body"]
            return self.get_rule_ele_sign(body)
        elif tp == "LIST":
            return self.get_rule_list_sign(rule)
        elif tp == "VAR":
            name = tp["name"]
            return self.get_rule_ele_sign(self.ast[name])

    def get_rule_sign(self, ast):
        all_signs = []
        for nm, bd in ast.ast.items():
            if bd["tp"] == "EXPORT":
                ele_names = []
                for ele in bd["body"]:
                    if ele["tp"] == "REF":
                        ele_names.append( "1" + ele["name"] )
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

    def __init__(self, rule_graph):
        self.rule_graph = rule_graph

    def score(self, matched):
        pass

    def select(self, matched):
        pass

    def basic_set(self, dialog):
        self.dialog = dialog
        self.AM = self.rule_graph.ac_machine.match(dialog)
        self.plus_preprocess(dialog, self.AM)

    def match(self, dialog):
        self.basic_set(dialog)

        all_matched = []
        while True:
            ele = ac_matched_ans.iter_init_status()
            if ele is None: break
            tp = "%s_%s%s"%(tp, tag_type[-1], ele_tp)
            if tp in self.rule_fingerprint:
                head_ele = ((ele[0], ele[1]), )
                matched_ans = self.max_match(tp, head_ele)
                if best_ans:
                    all_matched.extend( matched_ans)
                elif self.rule_fingerprint[tp]:
                    all_matched.append( (tp, head_ele ))

        return self.select(all_matched)


    # 对规则的最长匹配
    def max_match(self, tp, matched_eles):
        best_ans = []
        stack = [(tp, self.AM.save_state(), matched_eles)]
        while len(stack):
            tp, state, matched_eles = stack.pop(0)
            self.AM.restore_state(state)
            is_accept = False
            while not is_accept:
                tag_type, ele = self.AM.get_next()
                #if self.get_word_dist(ele[0]) > self.conf.max_match_dist:
                #    break
                if tag_type is None: break

                for ele_tp in ele[3]:
                    new_tp = "%s_%s%s"%(tp, tag_type, ele_tp)
                    if new_tp in self.rule_fingerprint:
                        self.AM.accept(ele)
                        is_accept = True
                        new_matched_eles = matched_eles + ((ele[0], ele[1]) , )
                        if self.rule_fingerprint[new_tp]:
                            best_ans.append( (new_tp,  new_matched_eles) )
                        stack.append((new_tp, self.AM.save_state(), new_matched_eles ) )

        return best_ans


    # 递归实现
    def max_match_rec(self, tp, matched_eles):
        pass

    def search_match(self, dialog):
        pass

    def plus_preprocess(self):
        for ap_name in self.rule_graph.plus:
            node = self.ast[ap_name]
            tp = node["body"]["tp"]
            if tp == "ATOM":
                self.atom_plus_preprocess(node, "keyword")
            elif  tp == "REF":
                self.atom_plus_preprocess(node, "slot")
            else:
                self.var_plus_preprocess(node)

        self.AM.matched.sort(key = lambda x: (x[0], -x[1]) )
        
    def atom_plus_preprocess(self, node, tp = "keyword"):
        if tp == "keyword":
            tag_index = self.AM.keyword_tag_index
        else:
            tag_index = self.AM.slot_tag_index
        ap_name, ap_tag = node["name"], node["body"]["name"]
        if ap_tag not in tag_index or len(tag_index[ap_tag]) <= 1:
            continue

        ids_of_tag = tag_index[ap_tag]
        # 找到所有的atom plus
        pre_tag_idx = beg_tag_idx = 0
        for i in range(1, len(tag_index[ap_tag])):
            start, end, key = ids_of_tag[i]
            pre_end= ids_of_tag[pre_tag_idx][1] + 1
            if start < pre_end:
                pass
            elif start == pre_end:
                pre_tag_idx = i
            else:

                if i - beg_tag_idx > 1:
                    ss_index, _, _ = ids_of_tag[beg_tag_idx]
                    _, se_index, _ = ids_of_tag[pre_tag_idx]
                    self.AM.matched.append( (ss_index, se_index, ap_name, "2") )

                pre_tag_idx = i
                beg_tag_idx = i

    def var_plus_preprocess(self, node):
        ans = []
        mm = self.S_match_plus(node)
        if mm:
            ans.extend(mm)
        self.AM.matched_keyword.append( (ss_index, se_index, ap_name, "2") )


    def S_match_atom(self, rule):
        while True:
            mc = self.AM.get_next_keyword()
            if not mc: break
            dist = self.AM.get_word_dist(mc[0])
            if dist > CONF.maxdist: break
            if rule["name"] in mc[2]:
                self.AM.accept(mc)
                return (mc, dist)

        return (None, None)

    # 可能需要考虑所有匹配到的, 然后动态规划; 
    # 目前先优先选择候选集合中长的
    def S_match_ref(self, rule):
        candi = []
        while True:
            mc = self.AM.get_next_slot()
            if not mc: break
            dist = self.AM.get_word_dist(mc[0])
            if dist > CONF.maxdist: break
            if mc[2] == e["name"]:
                candi.append(mc)

        return select_max_length(candi)

    def S_match_plus(self, rule):
        ans = []
        p_rule = rule["body"]
        while True:
            _m, _d = S_match(p_rule)
            if _m: ans.append(_m)
            else: break

        return ans

    def S_match(self, rule):
        tp = rule["tp"]
        if tp == "ATOM":
            _m, _d = self.S_match_atom(rule)
        elif tp == "REF":
            _m, _d = self.S_match_ref(rule)
        elif tp == "VAR":
            _m, _d = self.S_match( self.rule_graph.ast.ast[rule["body"]] )
        elif tp == "PLUS":
            _m, _d = self.S_match_plus(rule)
        elif tp == "RULE":
            _m, _d = slef.S_match_one_rule(rule)

        return _m, _d

    def merge_ele(self, lst ):
        return (lst[0][0], lst[-1][1], tag, "2")

    def S_match_one_rule(self, rule):
        tp = rule["tp"]
        total_dis = 0
        if tp == "LIST":
            ans = []
            for e in rule["body"]:
                _m, _d = self.S_match()
                total_dis += _d
                if _m: ans.append(_m)
                else: return []
            return ans, total_dis
        elif tp == "OR":
            pass
        else:
            _m = None

        return (None, None)

