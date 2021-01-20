
from items import TNode, AnyPat

def count_tag_num(e):
    if not e: t = 0
    else:     t = e.strip("#").count("#") + 1
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

# 笛卡尔积
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


# 无序列表的笛卡尔积
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


class TrieNodeInfo:
    """
        Trie树节点信息
            match_list:  匹配到的规则信息 TNode
            leafFlag:  是否是叶子节点
            anys: 后面接着有__ANY__
    """
    def __init__(self):
        self.match_list = []
        self.leafFlag = False
        self.anys = []

    def isLeaf(self):
        return self.leafFlag

    def remove_zero(self, lst):
        ans = []
        for a,b in lst:
            if a != 0:
                ans.append((a,b))

        return tuple(ans)

    # 判别是否是一样的Node， 去重
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

    def addAny(self, min_span, max_span):
        # 去重， 重复的不用添加
        if not any(map(lambda a: a.equal(min_span, max_span), self.anys)):
            self.anys.append(AnyPat(min_span, max_span))

    def is_next_any(self):
        return len(self.anys) > 0

    def addRule(self, name, slices, permutation):
        tn = TNode(name=name, slices=slices, permutation=permutation)
        self.setLeaf()
        for n in self.match_list:
            if self.isSameNode(n, tn):
                return

        self.match_list.append(tn)

# Trie implement by hashtable
class RuleTrie:
    def __init__(self, export_trie, special_tries, keeped_tags):
        self.export_trie = export_trie
        self.special_tries = special_tries
        self.keeped_tags = keeped_tags

class RuleStructure:
    """
        将规则ast编译成Trie树
            注：这里的Trie树是用hash表实现的
    """

    def __init__(self, ast):
        self.ast = ast
        self.rules_body = ast.rules_body
        self.rule_id = 0

    # 将names对应的规则集编译成一个Trie树
    # tags是Trie树中的所有tag列表
    def build_trie(self, names):
        rules_sign = self.get_sign(names)
        fingerprint, tags = self.build_tp_prefixes(rules_sign)
        return fingerprint, tags

    def build(self):
        """
            1. 构建特殊规则的Trie树, 特殊规则包含： plus， 非export的含有后处理的rule, atom
            2. 构建export规则的Trie树
        """
        special_tries = []
        for p in self.ast.get_special_rules():
            ptrie, _ = self.build_trie([p])
            special_tries.append((p, ptrie))

        export_trie, export_tags = self.build_trie(self.ast.get_export())
        return RuleTrie(export_trie, special_tries, export_tags), self.ast.all_rules_info

    # 将规则转换成 “#”连接的tag字符串列表
    # 比如: #aa#bb#cc 相当于Trie树中的一个路径;  #aa#bb#cc就是Trie中路径的一个唯一签名
    def get_ele_sign(self, rule):
        tp = rule["tp"]
        rname = rule.get("name", None)
        if tp == "PLUS":
            return [rname]
        elif tp == "ATOM":
            return [rname]
        elif tp == "REF":
            return [rname]
        elif tp == "__ANY__":
            tag = "%s:%d:%d"%(rule["tp"], rule["min_span"], rule["max_span"])
            return [tag]
        elif tp == "RULE":
            if self.ast.is_special_handle_rule(rname):
                return [rname]
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

    # 将规则扩展成tag路径的字符串
    def get_sign(self, names):
        all_signs = []
        for nm in names:
            rule = self.rules_body[nm]["body"]
            tp = rule["tp"]
            if tp == "LIST":
                t = [self.get_ele_sign(ele) for ele in rule["body"]]
                ele_sign = get_list_product_with_slices(t)
            elif tp == "ANGLE":
                t = [self.get_ele_sign(ele) for ele in rule["body"]]
                ele_sign = get_set_product_with_slices(t)
            else:
                ele_sign_parts = self.get_ele_sign(rule)
                ele_sign = [(e, (count_tag_num(e), ), None) for e in ele_sign_parts ]

            all_signs.append((ele_sign, nm))

        return all_signs
                

    # 构建Trie树; 这里是用hash表是实现的
    def build_tp_prefixes(self, rules):
        ans, all_tags = {}, set()
        ans[""] = TrieNodeInfo()
        for rs, nm in rules:
            for r, slices, permutation in rs:
                eles = r.strip("#").split("#")
                sub_ele = ""
                for ele in eles:
                    all_tags.add(ele)
                    # 处理通配符
                    if ele.startswith("__ANY__"):
                        any_sp = ele.split(":")
                        ans[sub_ele].addAny(int(any_sp[1]), int(any_sp[2]))
                    sub_ele += "#" + ele
                    if sub_ele not in ans:
                        ans[sub_ele] = TrieNodeInfo()

                ans[sub_ele].addRule(nm, slices, permutation)

        return ans, all_tags



