
from items import TNode

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
    def __init__(self, export_trie, plus_tries, to_dele_tags):
        self.export_trie = export_trie
        self.plus_tries = plus_tries
        self.need_delete_tags = to_dele_tags

class RulesInfo():

    def __init__(self):
        self.slots = {}
        self.config = {}
        self.rule_type = {}
        self.post_func = {}

    def add(self, rule_name, slot, pf, confs, rtp):
        self.slots[rule_name] = slot
        self.post_func[rule_name] = pf
        self.config[rule_name] = confs
        self.rule_type[rule_name] = rtp

    def get(self, name):
        slot = self.slots.get(name, {})
        pfunc = self.post_func.get(name, {})
        conf = self.config.get(name, [])
        return (slot, pfunc, conf)

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
        return RuleTrie(export_trie, plus_tries, need_delete_tags), self.ast.all_rules_info

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


