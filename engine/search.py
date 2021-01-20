"""
    在构建好的规则Trie树中，找出query所有可以匹配的组合
"""

import config
from items import *
from post_handle import apply_post, get_idx_slot, trans_by_post

class Searcher:
    """
        rule_trie: 编译好的Trie树类
        rule_info: 规则的全局信息，后处理，搜索配置等
        ac_machie: 词典和关键字的AC自动机
    """

    def __init__(self, rule_trie, rule_info, ac_machine):
        self.rule_trie = rule_trie
        self.rule_info = rule_info
        self.ac_machine = ac_machine

    def basic_set(self, dialog):
        """ 搜索前预处理: 
                1. 找出所有词
                2. 预处理需要特殊规则： plus及需要后处理的非export规则
                3. 删除用不到的tag， 排序
        """
        self.AM = self.ac_machine.match(dialog)
        special_post = self.special_preprocess(dialog)
        if len(self.rule_trie.keeped_tags) > 0:
            self.AM.delete_tag(self.rule_trie.keeped_tags)
        self.AM.sorted()
        self.AM.build_word_next_idx()
        #print(self.AM.matched)
        return special_post

    # 按照贪心策略搜索
    def max_match(self, dialog):
        special_post = self.basic_set(dialog)
        conf = config.get_conf(None, "search")
        matched_ans = self._greed_match(self.rule_trie.export_trie, conf)
        return matched_ans, special_post
        
    # 完全搜索所有可能
    def search_match(self, dialog):
        special_post = self.basic_set(dialog)
        conf = config.get_conf(None, "search")
        matched_ans = self._search_match(self.rule_trie.export_trie, conf)
        return matched_ans, special_post
        
    def _search_match(self, fingerprint, conf):
        self.AM.reset()
        all_matched = []
        has_seen = set()
        for i in range(len(self.AM.matched)):
            matched_ans = self._search_match_helper(i, fingerprint, has_seen, conf)
            all_matched.extend(matched_ans)

        return all_matched

    # 深度优先搜索    
    def _search_match_helper(self, i, fingerprint, has_seen, conf):
        self.AM.iter_init(i)
        best_ans = []
        stack = [("", self.AM.get_state(), tuple())]

        def __search_helper(new_tp, new_matched_eles, new_state):
            search_step_fingerprint = "%d&%s"%(new_state[0], new_tp)
            if search_step_fingerprint in has_seen: return
            has_seen.add(search_step_fingerprint)

            if new_tp in fingerprint:
                if fingerprint[new_tp].isLeaf():
                    best_ans.append(MatchedItem(new_tp,  new_matched_eles, fingerprint[new_tp].match_list))

                stack.append((new_tp, new_state, new_matched_eles))

        while len(stack):
            tp, state, matched_eles = stack.pop(0)
            self.AM.reset_state(state)

            if fingerprint[tp].is_next_any():
                any_list = fingerprint[tp].anys

                # 如果规则最后是__ANY__
                for any_pat in any_list:
                    new_tp = "%s#%s"%(tp, any_pat.to_pat())
                    search_step_fingerprint = "%d&%s"%(state[0], new_tp)
                    if search_step_fingerprint in has_seen: continue
                    has_seen.add(search_step_fingerprint)
                    if new_tp in fingerprint and fingerprint[new_tp].isLeaf():
                        d = any_pat.get_max_dist(state[1], self.AM.dialog_length - 1)
                        if d > 0:
                            new_matched_eles = matched_eles + ((state[1] + 1, d),)
                            best_ans.append(MatchedItem(new_tp,  new_matched_eles, fingerprint[new_tp].match_list))

                # 查询规则中间是__ANY__
                for i in range(1, 25):
                    ele = self.AM.look_next(i)
                    if ele is None: break
                    d = self.AM.get_word_dist(ele.start)
                    for any_pat in any_list:
                        if any_pat.is_valid(d):
                            new_tp = "%s#%s#%s"%(tp, any_pat.to_pat(), ele.tag)
                            new_state = (self.AM._i + i, ele.end)
                            new_matched_eles = matched_eles + ((ele.start - d, ele.start - 1), (ele.start, ele.end))
                            __search_helper(new_tp, new_matched_eles, new_state)


            while self.AM.has_next():
                ele = self.AM.get_next()

                # 大于限定距离; break
                if self.AM.get_word_dist(ele.start) > conf["max_dist"]:
                    break

                new_tp = "%s#%s"%(tp, ele.tag)
                new_matched_eles = matched_eles + ((ele.start, ele.end),)
                new_state = (self.AM._i, ele.end)
                __search_helper(new_tp, new_matched_eles, new_state)

                if new_tp not in fingerprint and len(matched_eles) > 0:
                    if conf["no_skip_atom"] and ele.tag_type in "0":
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
            matched_ans = self._greed_match_helper(i, fingerprint, conf)
            all_matched.extend(matched_ans)

        return all_matched


    # 对规则的最长匹配
    def _greed_match_helper(self, i, fingerprint, conf):
        self.AM.iter_init(i)
        best_ans = []
        stack = [("", self.AM.get_state(), tuple())]
        while len(stack):
            tp, state, matched_eles = stack.pop(0)
            self.AM.reset_state(state)
            is_accept = False
            while not is_accept and self.AM.has_next():
                ele = self.AM.get_next()
                #if self.get_word_dist(ele[0]) > self.conf.max_match_dist:
                #    break

                new_tp = "%s#%s"%(tp, ele.tag)
                if new_tp in fingerprint:
                    self.AM.accept(ele)
                    is_accept = True
                    new_matched_eles = matched_eles + ((ele.start, ele.end), )
                    # simple
                    if fingerprint[new_tp].isLeaf():
                        best_ans.append(MatchedItem(new_tp, new_matched_eles, fingerprint[new_tp].match_list))
                    stack.append((new_tp, self.AM.get_state(), new_matched_eles ))

        return best_ans

    # 特殊规则逐条匹配; 这种规则多了会影响速度， 只做特殊用途
    # plus可能是指数式复杂度， 但其在语义匹配需求中使用场景不多，大多采用贪心匹配足已
    # 为了最大化性能， plus采用贪心匹配
    def special_preprocess(self, dialog):
        special_post = {}
        _, post = self.special_atom_extract(dialog)
        special_post.update(post)

        for pname, trie in self.rule_trie.special_tries:
            conf_names = self.rule_info.config.get(pname, [])
            rule_tp = self.rule_info.get_rule_type(pname)
            base_tp = "plus" if rule_tp == "PLUS" else "search"
            conf = config.get_confs(conf_names, base_tp)
            matched_items = self._greed_match(trie, conf)
            if matched_items:
                for m in matched_items:  m.cal_match_score(dialog)
                if rule_tp == "PLUS":
                    all_plus, post = self.plus_extract(matched_items, pname, conf, special_post)
                else:
                    all_plus, post = self.special_rule_extract(matched_items, pname, conf, special_post)
                if all_plus:
                    special_post.update(post)
                    self.AM.matched.extend(all_plus)
                    self.AM.sorted()

        return special_post

    def special_atom_extract(self, dialog):
        special_atoms = self.rule_info.get_special_atoms()
        post = {}
        if not special_atoms:
            return [], post

        for ele in self.AM.matched:
            if ele.tag in special_atoms:
                slot_indexes, pfunc, _ = self.rule_info.get(ele.tag)
                idx_slot_map = {0: dialog[ele.start: ele.end+1]}
                slots = apply_post(slot_indexes, pfunc, idx_slot_map)
                if "__MATCH__" not in slots or slots["__MATCH__"] == True:
                    post[(ele.tag, ele.start, ele.end)] = slots
                else:
                    self.AM.matched.remove(ele)

        return [], post

    ## 合法性判断， 后处理
    def special_rule_extract(self, lst, rname, conf, special_post):
        tags, post = [], {}
        for c in lst:
            _, slices, perm = c.tnodes[0]
            slot_indexes, pfunc, _ = self.rule_info.get(rname)
            if slot_indexes or pfunc:
                idx_slot_map = get_idx_slot(slices, perm, c.fragments, special_post)
                slots = apply_post(slot_indexes, pfunc, idx_slot_map)
                if "__MATCH__" not in slots or slots["__MATCH__"] == True:
                    post[(rname, c.begin, c.end)] = slots
                    tags.append(AcMatchedGroup(c.begin, c.end, rname, "3"))
            else:
                tags.append(AcMatchedGroup(c.begin, c.end, rname, "3"))

        return tags, post

    def plus_extract(self, lst, tag, conf, special_post):
        ans, post = [], {}
        if not lst: return ans, post

        item = lst[0]
        i, cnt = 1, 1
        while i < len(lst):
            dist = lst[i].begin - item.end
            end_flag = False
            if dist <= 0:
                end_flag = conf["no_cover"]
                i += 1
            elif dist <= conf["max_dist"] + 1 and cnt < conf["max_N"]:
                item.concat(lst[i])
                cnt += 1
                i += 1
            else:
                end_flag = True

            if cnt >= conf["min_N"] and end_flag:
                frags, _ = trans_by_post(item.fragments, special_post)
                post[(tag, item.begin, item.end)] =  {"__OUT__": "".join(frags)}
                ans.append(AcMatchedGroup(item.begin, item.end, tag, "2"))

            if end_flag: 
                if i < len(lst):
                    item = lst[i]
                    cnt = 1
                    i += 1
                else:
                    item = None

        if cnt >= conf["min_N"] and item is not None:
            frags, _ = trans_by_post(item.fragments, special_post)
            post[(tag, item.begin, item.end)] =  {"__OUT__": "".join(frags)}
            ans.append(AcMatchedGroup(item.begin, item.end, tag, "2"))

        return ans, post
