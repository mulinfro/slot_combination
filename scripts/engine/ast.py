
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
        for atom_value in ast.ast[atom_name]:
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


class AST():

    def __init__(self, stm):
        self.word_refs = []
        self.atom = []
        self.plus = []
        self.ast = {}
        self.build_ast(stm)

    def build_ast(self, stm):
        ast = []
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
                self.atom.append(val["name"])
            elif tkn.tp == 'PLUS':
                val = self.ast_plus(stm)
                self.plus.append(val["name"])
            else:
                Error("Unexpeted begining token %s"%tkn.val)
            if val["name"] in self.ast:
                Error("conflict rule names: " + val["name"])

            self.ast[val["name"]] = val

    def ast_export(self, stm):
        stm.next()
        rule = self.ast_rule_helper(stm)
        post_processer = self.ast_post_process(stm)
        syntax_cond_assert(is_rule_end(stm, True), "expected rule end")

        return {"tp": "EXPORT", "name": rule["rule_name"], "body": rule["body"], 
                    "post":post_processer}

    def ast_rule(self, stm):
        stm.next()
        rule = self.ast_rule_helper(stm)
        post_func = self.ast_post_process(stm)
        syntax_cond_assert(is_rule_end(stm, True), "expected rule end")
        return {"tp": "RULE", "name":rule["rule_name"], "body": rule["body"], "post_func": post_func }

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
        tkn = stm.next()
        syntax_assert(tkn, "DICT", "%s need { here"%rule_name)
        var = self.ast_dict_ele(stream(tkn.val))
        return {"tp": "PLUS", "name":rule_name, "body": var }
        
    def ast_rule_helper(self, stm):
        syntax_assert(stm.peek(), "STR", stm.peek().tp)
        rule_name = stm.next().val
        syntax_assert(stm.next(), ("OP", "="), "%s need = here"%rule_name)
        body = self.ast_rule_body(stm)
        return {"tp": "RULE_BODY", "rule_name": rule_name, "body": body }

    def ast_list_helper(self, stm):
        body = []
        while True:
            tkn = stm.next()
            syntax_assert(tkn, "DICT", "%s need { here"%tkn.val)
            ele = self.ast_dict_ele(stream(tkn.val))
            body.append(ele)
            if not stm.eof():
                syntax_check(stm.next(), ("SEP", "COMMA"))
            if stm.eof(): break
        syntax_cond_assert(len(body) >= 1, "empty parn")
        return {"tp":"LIST", "body": body }

    #还没有支持
    def try_ast_or(self, stm):
        pass

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
            self.word_refs.append(name)
            return {"tp":"REF", "name": name}
        else:
            if name not in self.ast: Error("Undefined %s"%name)
            return self.ast[name]

    def ast_rule_body(self, stm):
        tkn = stm.next()
        if tkn.tp == "LIST":
            return self.ast_list_helper(stream(tkn.val))
        elif tkn.tp == "DICT":
            return self.ast_dict_ele(stream(tkn.val))
        else:
            Error("undefined rule body type")

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
                    if stm.lookahead(2).val == "?": sub_eles.append("")
                    break
                else:
                    stm.back()
                    syntax_assert(tkn, "SEP")
                    break
            eles.extend(get_cross_ele(sub_eles, [""], 0) )
            if is_rule_end(stm): break

        return eles

    def ast_post_process(self, stm):
        while not is_rule_end(stm):
            stm.next()

        return {}

