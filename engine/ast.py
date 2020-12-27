
from builtin import op_type, op_funcs
from syntax_check import *
from stream import stream
from post_register import post_modules
from items import ParamItem
import collections
from config import user_defined_config

def is_candi_op(tkn, candi):
    return tkn.tp == "OP" and tkn.val in candi

def newlines(stm):
    is_valid = lambda tkn: syntax_check(tkn, ("SEP","NEWLINE"))
    vals = ast_same_type_seq(stm, is_valid)
    return len(vals) > 0

def ast_same_type_seq(stm, is_valid):
    tps = []
    while not stm.eof() and is_valid(stm.peek()):
        tps.append(stm.next().val)
    return tps

def is_rule_end(stm, eat=False):
    if stm.eof(): return True
    tkn = stm.peek()
    if tkn.tp == "SEP" and tkn.val in ["SEMI", "NEWLINE" ]:
        if eat: stm.next()
        return True
    return False

def is_rule_body_end(stm):
    if is_rule_end(stm): return True
    tkn = stm.peek()
    return tkn.tp == "SEP" or is_candi_op(tkn, ["=>", "::"])

def skip_tkns(stm, candi):
    while not stm.eof():
        tkn = stm.next()
        if tkn.val not in candi:
            stm.back()
            break

def extract_all_atoms(ast):
    slots = {}
    for atom_name in ast.atom:
        for atom_value in ast.rules_body[atom_name]["body"]:
            tag = slots.get(atom_value, [])
            if atom_name not in tag:
                tag.append(atom_name)
            slots[atom_value] = tag

    return slots
        
def get_cross_ele(lst, all_sets, i):
    ans = []
    if i >= len(lst): return all_sets
    for e in all_sets:
        ans.append( e + lst[i])
        if i != len(lst) - 1:
            ans.append( e + lst[i][0:-1])
    return get_cross_ele(lst, ans, i + 1)


class RulesInfo():

    def __init__(self):
        self.slots = {}
        self.config = {}
        self.rule_type = collections.OrderedDict()
        self.post_func = {}

    def add(self, rule_name, slot, pf, confs, rtp):
        self.slots[rule_name] = slot
        self.post_func[rule_name] = pf
        self.config[rule_name] = confs

        # 需要特殊处理的规则： 后处理； 归一化;  特殊配置;  逻辑unit等
        need_post_handle = (slot or pf or confs)
        self.rule_type[rule_name] = (rtp, need_post_handle)

    def get(self, name):
        slot = self.slots.get(name, {})
        pfunc = self.post_func.get(name, {})
        conf = self.config.get(name, [])
        return (slot, pfunc, conf)

    def get_rule_type(self, rname):
        return self.rule_type[rname][0]

    def get_special_rules(self):
        return [k for k,v in self.rule_type.items() if v == ("RULE", True) or v[0] == "PLUS"]

    def get_special_atoms(self):
        return [k for k,v in self.rule_type.items() if v == ("ATOM", True)]

    def is_special(self, rname):
        return self.rule_type[rname][1]

    def get_rules_by_tp(self, tp):
        return [k for k,v in self.rule_type.items() if v[0] == tp]

class AST():

    def __init__(self, stm):
        self.word_refs = []
        self.rules_body = {}
        self.all_rules_info = RulesInfo()
        self.build_ast(stm)
        self.atom = self.all_rules_info.get_rules_by_tp("ATOM")

    def is_special_handle_rule(self, rname):
        return self.all_rules_info.is_special(rname)

    def get_special_rules(self):
        return self.all_rules_info.get_special_rules()

    def get_export(self):
        return self.all_rules_info.get_rules_by_tp("EXPORT")

    def build_ast(self, stm):
        while True:
            newlines(stm)
            if stm.eof(): break
            tkn = stm.peek()
            if tkn.tp == 'EXPORT':
                val = self.ast_export(stm)
            elif tkn.tp == 'RULE':
                val = self.ast_rule(stm)
            elif tkn.tp == 'ATOM':
                val = self.ast_atom(stm)
            elif tkn.tp == 'PLUS':
                val = self.ast_plus(stm)
            else:
                Error("Unexpeted begining token %s"%tkn.val)
            if val["name"] in self.rules_body:
                Error("conflict rule names: " + val["name"])

            self.rules_body[val["name"]] = val

    def ast_export(self, stm):
        ans = self.ast_rule(stm, "EXPORT")
        ans["tp"] = "EXPORT"
        return ans

    def ast_rule(self, stm, rtp = "RULE"):
        stm.next()
        rule = self.ast_rule_helper(stm)
        post_func, slots, conf_name = self.ast_post(stm)
        self.all_rules_info.add(rule["rule_name"], slots, post_func, conf_name, rtp)
        syntax_cond_assert(is_rule_end(stm, True), "expected rule end")

        ans = {"tp": "RULE", "name":rule["rule_name"], "body": rule["body"]}
        return ans

    def ast_atom(self, stm):
        stm.next()
        syntax_assert(stm.peek(), "STR", stm.peek().tp)
        rule_name = stm.next().val
        syntax_assert(stm.next(), ("OP", "="), "%s need = here"%rule_name)
        body = self.ast_atom_body(stm)
        post_func, slots, conf_name = self.ast_post(stm)
        self.all_rules_info.add(rule_name, slots, post_func, conf_name, "ATOM")
        syntax_cond_assert(is_rule_end(stm, True), "expected rule end")
        #ast_same_type_seq(stm, lambda tkn: syntax_check(tkn, ("SEP","SEMI")))
        return {"tp": "ATOM", "name": rule_name, "body": body }

    def ast_plus(self, stm):
        stm.next()
        rule_name = stm.next().val
        syntax_assert(stm.next(), ("OP", "="), "%s need = here"%rule_name)
        body = self.ast_rule_body(stm)
        post_func, slots, conf_name = self.ast_post(stm)
        self.all_rules_info.add(rule_name, slots, post_func, conf_name, "PLUS")

        ans = {"tp": "PLUS", "name":rule_name, "body": body }
        return ans
        
    def ast_rule_helper(self, stm):
        syntax_assert(stm.peek(), "STR", stm.peek().tp)
        rule_name = stm.next().val
        syntax_assert(stm.next(), ("OP", "="), "%s need = here"%rule_name)
        body = self.ast_rule_body(stm)
        return {"tp": "RULE_BODY", "rule_name": rule_name, "body": body }

    def ast_list_helper(self, stm, tp):
        body = []
        while not stm.eof():
            ele = self.ast_rule_body(stm)
            body.append(ele)
            if not stm.eof():
                syntax_check(stm.next(), ("SEP", "COMMA"))
            if stm.eof(): break
        syntax_cond_assert(len(body) >= 1, "empty parn")
        return {"tp":tp, "body": body }

    def ast_dict_ele(self, stm):
        tkn = stm.next()
        is_ref = False
        if tkn.val == ".":
            is_ref = True
            tkn = stm.next()
        name = tkn.val
        if not stm.eof():
            syntax_assert(stm.next(), ("OP", "::"), "expected ::")

        if is_ref:
            if name not in self.word_refs:
                self.word_refs.append(name)
            return {"tp":"REF", "name": name}
        else:
            if name not in self.rules_body: Error("Undefined %s"%name)
            return {"tp":"VAR", "name": name} #self.ast[name]

    def ast_try_or_ele(self, stm):
        eles = [self.ast_dict_ele(stream(stm.next().val)) ]
        while not stm.eof():
            tkn = stm.next()
            if tkn == ("OP", "|"):
                n_tkn = stm.next()
                syntax_assert(n_tkn, "DICT", "expected dict")
                eles.append(self.ast_dict_ele(stream(n_tkn.val)))
            elif tkn == ("OP", "?"): 
                return {"tp": "OR_?", "body": eles[0] }
            else:
                stm.back()
                break
                
        if len(eles) > 1:
            return {"tp": "OR", "body": eles }
        else:
            return eles[0]

    def ast_builtin_pattern(self, stm):
        tkn = stm.next()
        if tkn.tp == "__ANY__":
            syntax_cond_assert(not stm.eof() and stm.peek().tp == "PARN", "__ANY__ need range, eg: __ANY__(1,5)")
            p_stm = stream(stm.next().val)
            paras = self.get_processer_paras(p_stm)
            syntax_cond_assert(len(paras) == 2, "__ANY__ need min_span and max_span, eg: __ANY__(1,5)")
            return {"tp": "__ANY__", "min_span": paras[0].val, "max_span": paras[1].val}
        else:
            Error("Unsuppoert builtin pattern: %s"%tkn.tp)

    def ast_rule_body(self, stm):
        tp = stm.peek().tp
        if tp == "LIST":
            tkn = stm.next()
            return self.ast_list_helper(stream(tkn.val), tp)
        elif tp == "ANGLE":
            tkn = stm.next()
            return self.ast_list_helper(stream(tkn.val), tp)
        elif tp == "DICT":
            return self.ast_try_or_ele(stm)
        elif tp.sartswith("__"):
            return self.ast_builtin_pattern(stm)
        else:
            Error("undefined rule body type %s"%str(stm.peek()))

    def ast_atom_body(self, stm):
        eles = []
        while True:
            sub_eles = []
            while not stm.eof():
                tkn = stm.next()
                if tkn.tp == "STR":
                    sub_eles.append(tkn.val)
                elif is_candi_op(tkn, "?"):
                    continue
                elif is_candi_op(tkn, "|"):
                    if stm.lookahead(2) == ("OP", "?"): sub_eles.append("")
                    break
                else:
                    if stm.lookahead(2) == ("OP", "?"): sub_eles.append("")
                    stm.back()
                    break
            eles.extend(get_cross_ele(sub_eles, [""], 0))
            if is_rule_body_end(stm): break

        return eles

    def ast_processer_para(self, stm):
        tkn = stm.next()
        if tkn.tp in ["STRING", "NUM"]:
            return ParamItem(tkn.tp, tkn.val)
        elif tkn == ("OP", "$"):
            t = stm.next()
            #syntax_assert(t, "STR", "expected num")
            syntax_cond_assert(t.tp == "NUM", "expected num")
            return ParamItem("VAR", int(t.val))
        else:
            Error("processer error %s"%(str(tkn)))

    def get_processer_paras(self, stm):
        paras = []
        while not stm.eof():
            p = self.ast_processer_para(stm)
            paras.append(p)
            if not stm.eof():
                syntax_assert(stm.next(), ("SEP", "COMMA"), "")

        return paras

    def ast_post_element(self, stm):
        tkn = stm.peek()
        if tkn == ("OP", "@"):
            stm.next()
            key = stm.next()
            syntax_assert(key, "STR", "")
            if not stm.eof() and stm.peek().tp == "PARN":
                p_stm = stream(stm.next().val)
                paras = self.get_processer_paras(p_stm)
                syntax_cond_assert(key.val in post_modules,  key.val + " not in post libs")
                return {"tp": "FUNC", "val": key.val, "paras": paras}
            else:
                syntax_cond_assert(key.val in user_defined_config,  key.val + " not in user_defined_config")
                return {"tp": "CONF", "val": key.val}
        else:
            val = self.ast_processer_para(stm)
            return {"tp":val.tp , "val": val.val}

    """
        1. intent = "first", slot_int = 1, slot = $1
        2. @post($1, 2)
    """
    def ast_post(self, stm):
        post_func = collections.OrderedDict()
        slots = collections.OrderedDict()
        conf_names = []
        if not stm.eof() and stm.peek().val == "=>":
            stm.next()
            tkn = stm.next()
            syntax_assert(tkn, "DICT", "")

            nstm = stream(tkn.val)
            while not nstm.eof():
                tkn = nstm.peek()
                if tkn.tp == "STR":
                    nstm.next()
                    syntax_assert(nstm.next(), ("OP", "="), "")
                    ele = self.ast_post_element(nstm)
                    syntax_cond_assert(ele["tp"] != "CONF", "syntax error, unexpected config in slots")
                    slots[tkn.val] = ele
                elif tkn == ("OP", "@"):
                    ele = self.ast_post_element(nstm)
                    if ele["tp"] == "FUNC":
                        post_func[ele["val"]] = ele["paras"]
                    else:
                        conf_names.append(ele["val"])
                else:
                    Error("Unexpected %s in line %d, col %d"%(tkn.val, tkn.line, tkn.col))

                if not nstm.eof():
                    syntax_assert(nstm.next(), ("SEP", "COMMA"), "")


        return post_func, slots, conf_names
            

