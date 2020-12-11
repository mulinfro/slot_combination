
from builtin import op_type, op_funcs
from syntax_check import *
from stream import stream

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

class PostProcess():

    def __init__(self, slots, post_func):
        self.slots = slots
        self.post_func = post_func
        
class AST():

    def __init__(self, stm):
        self.word_refs = []
        self.atom = []
        self.plus = []
        self.rule = []
        self.export = []
        self.rules_body = {}
        self.post_info = {}
        self.config = {}
        self.build_ast(stm)

    def build_ast(self, stm):
        while True:
            newlines(stm)
            if stm.eof(): break
            tkn = stm.peek()
            if tkn.tp == 'EXPORT':
                val = self.ast_export(stm)
                self.export.append(val["name"])
            elif tkn.tp == 'RULE':
                val = self.ast_rule(stm)
                self.rule.append(val["name"])
            elif tkn.tp == 'ATOM':
                val = self.ast_atom(stm)
                self.atom.append(val["name"])
            elif tkn.tp == 'PLUS':
                val = self.ast_plus(stm)
                self.plus.append(val["name"])
            else:
                Error("Unexpeted begining token %s"%tkn.val)
            if val["name"] in self.rules_body:
                Error("conflict rule names: " + val["name"])

            self.rules_body[val["name"]] = val

    def ast_export(self, stm):
        ans = self.ast_rule(stm, "export")
        ans["tp"] = "EXPORT"
        return ans

    def add_extra_info(self, name, post_info, tp):
        post_func, slots, conf_name = post_info
        self.post_info[name]  = PostProcess(slots, post_func)
        self.config[name] = conf_name

    def ast_rule(self, stm, rtp = "rule"):
        stm.next()
        rule = self.ast_rule_helper(stm)
        post_info = self.ast_post(stm)
        self.add_extra_info(rule["rule_name"], post_info, rtp)
        syntax_cond_assert(is_rule_end(stm, True), "expected rule end")

        ans = {"tp": "RULE", "name":rule["rule_name"], "body": rule["body"]}
        return ans

    def ast_atom(self, stm):
        stm.next()
        syntax_assert(stm.peek(), "STR", stm.peek().tp)
        rule_name = stm.next().val
        syntax_assert(stm.next(), ("OP", "="), "%s need = here"%rule_name)
        body = self.ast_atom_body(stm)
        syntax_cond_assert(is_rule_end(stm, True), "expected rule end")
        #ast_same_type_seq(stm, lambda tkn: syntax_check(tkn, ("SEP","SEMI")))
        return {"tp": "ATOM", "name": rule_name, "body": body }

    def ast_plus(self, stm):
        stm.next()
        rule_name = stm.next().val
        syntax_assert(stm.next(), ("OP", "="), "%s need = here"%rule_name)
        body = self.ast_rule_body(stm)
        post_info = self.ast_post(stm)
        self.add_extra_info(rule_name, post_info, "plus")

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
                    stm.back()
                    syntax_assert(tkn, "SEP")
                    break
            eles.extend(get_cross_ele(sub_eles, [""], 0) )
            if is_rule_end(stm): break

        return eles

    def ast_processer_para(self, stm):
        tkn = stm.next()
        if tkn.tp == "STRING":
            return {"tp":"STRING", "val": tkn.val }
        elif tkn.tp == "NUM":
            return {"tp":"NUM", "val": str(tkn.val) }
        elif tkn == ("OP", "$"):
            t = stm.next()
            #syntax_assert(t, "STR", "expected num")
            syntax_cond_assert(t.tp == "STR" and t.val.isnumeric(), "expected num")
            return {"tp":"VAR", "val": int(t.val) }
        else:
            Error("processer error")

    def get_processer_paras(self, stm):
        paras = []
        while not stm.eof():
            p = self.ast_processer_para(stm)
            paras.append(p)
            if not stm.eof():
                syntax_assert(stm.next(), ("SEP", "COMMA"), "")

        return paras

    """
        1. intent = "first", slot_int = 1, slot = $1
        2. @post($1, 2)
    """
    def ast_post(self, stm):
        post_func, slots, conf_name = {}, {}, ""
        if not stm.eof() and stm.peek().val == "=>":
            stm.next()
            tkn = stm.next()
            syntax_assert(tkn, "DICT", "")

            nstm = stream(tkn.val)
            while not nstm.eof():
                tkn = nstm.next()
                if tkn == ("OP", "@"):
                    key = nstm.next()
                    syntax_assert(key, "STR", "")
                    paras = []
                    if not nstm.eof() and nstm.peek().tp == "PARN":
                        p_stm = stream(nstm.next().val)
                        paras = self.get_processer_paras(p_stm)
                    if paras:
                        post_func[key.val] = {"tp": "FUNC", "func_name":key.val, "paras": paras}
                    else:
                        conf_name = key.val
                else:
                    syntax_assert(tkn, "STR", "")
                    syntax_assert(nstm.next(), ("OP", "="), "")
                    val = self.ast_processer_para(nstm)["val"]
                    slots[tkn.val] = val

                if not nstm.eof():
                    syntax_assert(nstm.next(), ("SEP", "COMMA"), "")


        return post_func, slots, conf_name
            

