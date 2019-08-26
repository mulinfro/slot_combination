from syntax_check import Error


def get_list_product(lst_of_lst):
    ans = [""]
    for lst in lst_of_lst:
        new_ans = []
        for e in ans:
            for e2 in lst:
                if e2 == "": new_ans.append(e)
                else:     new_ans.append( ("%s_%s"%(e, e2)).strip("_") )
        ans = new_ans
    return ans

class Rule_structure():

    def __init__(self, ast, ac_machine, conf):
        self.ast = ast.ast
        self.conf = conf
        self.plus_fingerprint = self.get_plus_sign(ast.plus)
        rules_sign = self.get_sign(ast.ast)
        self.rule_fingerprint, export_tags = self.build_tp_prefixes(rules_sign)
        self.ac_machine = ac_machine
        self.need_delete_tags = self.get_need_delete_tag(export_tags, ast.atom + ast.word_refs + ast.plus)
        print("DELETE_TAG", self.need_delete_tags, )

    def get_need_delete_tag(self, export_tags, all_tags):
        ans = set()
        for t in all_tags:
            if t not in export_tags:
                ans.add(t)

        return ans

    def get_ele_sign(self, rule):
        tp = rule["tp"]
        if tp == "ATOM":
            return [ "0" + rule["name"] ]
        elif tp == "REF":
            return [ "1" + rule["name"] ]
        elif tp == "PLUS":
            return [ "2" + rule["name"] ]
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
        elif tp == "VAR":
            name = rule["name"]
            return self.get_ele_sign(self.ast[name])

    def get_sign(self, ast):
        all_signs = []
        for nm, bd in ast.items():
            if bd["tp"] == "EXPORT":
                ele_sign = self.get_ele_sign(bd["body"])
                all_signs.extend(ele_sign)

        print("ALL_SIGNS")
        print(all_signs)
        return all_signs
                
    def get_plus_sign(self, plus):
        all_signs = {}
        for nm in plus:
            sign = self.get_ele_sign(self.ast[nm]["body"])
            all_signs[nm], _ = self.build_tp_prefixes(sign)

        return all_signs

    def build_tp_prefixes(self, rules):
        ans, all_tags = {}, set()
        for r in rules:
            eles = r.strip("_").split("_")
            sub_ele = ""
            for ele in eles:
                all_tags.add(ele.lstrip("012345"))
                sub_ele += "_" + ele
                if sub_ele not in ans:
                    ans[sub_ele] = 0
            ans[sub_ele] = 1
        return ans, all_tags


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
        self.plus_preprocess()
        if len(self.rule_graph.need_delete_tags) > 0:
            self.delete_tag()

    def delete_tag(self):
        new_AM = []
        for (a,b,tag,c) in self.AM.matched:
            new_tag = [ t for t in tag if t not in self.rule_graph.need_delete_tags]
            if new_tag:
                new_AM.append( (a,b,new_tag, c) )
            
        self.AM.matched = new_AM

    def max_match(self, dialog):
        self.basic_set(dialog)
        print(self.AM.matched)

        print("begining match ...")
        ans = self._greed_match(self.rule_graph.rule_fingerprint, {})
        return ans

    def search_macth(self):
        pass

    def _double_greed_macth(self):
        pass

    def _greed_match(self, fingerprint, conf):
        self.AM.reset()
        all_matched = []
        print(fingerprint)
        while not self.AM.iter_end():
            ele = self.AM.iter_init_status()
            for ele_tp in ele[2]:
                tp = "%s_%s%s"%("", ele[-1], ele_tp)
                #print("GG", tp, ele)
                if tp in fingerprint:
                    #print("GG2", tp)
                    head_ele = ((ele[0], ele[1]), )
                    matched_ans = self._greed_match_helper(tp, head_ele, fingerprint, conf)
                    if matched_ans:
                        all_matched.extend(matched_ans)
                    elif fingerprint[tp]:
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

                for ele_tp in ele[2]:
                    new_tp = "%s_%s%s"%(tp, ele[-1], ele_tp)
                    if new_tp in fingerprint:
                        self.AM.accept(ele)
                        is_accept = True
                        new_matched_eles = matched_eles + ((ele[0], ele[1]) , )
                        # simple
                        # new_matched_eles = self.merge_ele(matched_eles, ele[0], ele[1] )
                        if fingerprint[new_tp]:
                            best_ans.append( (new_tp,  new_matched_eles) )
                        stack.append((new_tp, self.AM.save_state(), new_matched_eles ) )

        return best_ans


    # 递归实现
    def max_match_rec(self, tp, matched_eles):
        pass

    def search_match(self, dialog):
        pass


    def plus_preprocess(self):
        for ap_name in self.rule_graph.plus_fingerprint:
            node = self.rule_graph.ast[ap_name]
            bd = self.get_ast_body(node)
            conf = node.get("config", {})
            if bd["tp"] == "ATOM":
                self.atom_plus_preprocess(bd, [ap_name], "keyword")
            elif  bd["tp"] == "REF":
                self.atom_plus_preprocess(bd, [ap_name], "slot")
            else:
                self.var_plus_preprocess(ap_name, conf)

            self.AM.matched.sort(key = lambda x: (x[0], -x[1]) )
        
    def atom_plus_preprocess(self, node, tag, tp = "keyword"):
        tag_index = self.AM.word_tag_index
        ap_tag = node["name"]
        conf = node["config"]
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
                    self.AM.matched.append( (ss_index, se_index, tag, "2") )

                pre_tag_idx = i
                beg_tag_idx = i
                cnt = 1

        if cnt >= conf["min_N"]:
            self.AM.matched.append((ids_of_tag[beg_tag_idx][0], ids_of_tag[pre_tag_idx][1], tag, "2") )

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
                if cnt > conf["min_N"]:
                    ans.append( (lst[b_i][0], lst[p_i][1], tag, "2")  )

                p_i = b_i =  i
                cnt = 1

        if cnt > conf["min_N"]:
            ans.append( (lst[b_i][0], lst[p_i][1], tag, "2")  )

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
        print("ALL_PLUS", all_plus, all_matched, figerprint)
        self.AM.matched.extend(all_plus)

    def get_ast_body(self, node):
        bd = node["body"]
        if bd["tp"] == "VAR":
            return self.rule_graph.ast[bd["name"]]
        else:
            return bd


##########################################################

    def S_match_atom(self, rule):
        while True:
            mc = self.AM.get_typeed_next("0")
            if not mc: break
            dist = self.AM.get_word_dist(mc[0])
            if dist > self.rule_graph.config.VAR_PLUS_MAX_DIST: break
            if rule["name"] in mc[2]:
                self.AM.accept(mc)
                return (mc, dist)

        return (None, None)

    # 可能需要考虑所有匹配到的, 然后动态规划; 
    # 目前先优先选择候选集合中长的
    def S_match_ref(self, rule):
        candi = []
        while True:
            mc = self.AM.get_typeed_next("1")
            if not mc: break
            dist = self.AM.get_word_dist(mc[0])
            if dist > self.rule_graph.config.VAR_PLUS_MAX_DIST: break
            if mc[2] == e["name"]:
                candi.append(mc)

        return select_max_length(candi)
