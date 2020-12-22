import config
from items import *

class Searcher():

    def __init__(self, rule_trie, rule_info, ac_machine):
        self.rule_trie = rule_trie
        self.rule_info = rule_info
        self.ac_machine = ac_machine

    def basic_set(self, dialog):
        self.dialog = dialog
        self.AM = self.ac_machine.match(dialog)
        self.plus_preprocess()
        self.AM.sorted()
        if len(self.rule_trie.need_delete_tags) > 0:
            self.AM.delete_tag(self.rule_trie.need_delete_tags)
        #self.AM.build_word_next_idx(len(dialog))

    def max_match(self, dialog):
        self.basic_set(dialog)
        conf = config.get_conf(None, "search")
        return self._greed_match(self.rule_trie.export_trie, conf)
        
    def search_match(self, dialog):
        self.basic_set(dialog)
        conf = config.get_conf(None, "search")
        return self._search_match(self.rule_trie.export_trie, conf)
        
    def _search_match(self, fingerprint, conf):
        self.AM.reset()
        all_matched = []
        has_seen = set()
        for i in range(len(self.AM.matched)):
            ele = self.AM.iter_init_status(i)
            tp = "%s#%s%s"%("", ele.tag_type, ele.tag)
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

                new_tp = "%s#%s%s"%(tp, ele.tag_type, ele.tag)
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
            tp = "%s#%s%s"%("", ele.tag_type, ele.tag)
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

                new_tp = "%s#%s%s"%(tp, ele.tag_type, ele.tag)
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
            conf_names = self.rule_info.config.get(pname, [])
            conf = config.get_confs(conf_names, "plus")
            matched_items = self._greed_match(trie, conf)
            if matched_items:
                for m in matched_items:  m.cal_index()
                all_plus = self.plus_extract(matched_items, pname, conf)
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


