
from builtin import op_type, op_funcs
from syntax_check import *
from stream import stream

def is_candi_op(tkn, candi):
    return tkn.tp == "OP" and tkn.val in candi

class AST():
    def __init__(self, tokens):
        self.ast = []
        self.build_ast(tokens)

    def newlines(self, stm):
        is_valid = lambda tkn: syntax_check(tkn, ("SEP","NEWLINE"))
        vals = self.ast_same_type_seq(stm, is_valid)
        return len(vals) > 0

    def ast_same_type_seq(self, stm, is_valid):
        tps = []
        while not stm.eof() and is_valid(stm.peek()):
            tps.append(stm.next().val)
        return tps

    def is_rule_end(self, stm):
        if stm.eof(): return True
        tkn = stm.peek()
        if tkn.tp == "SEP" and tkn.val in ["SEMI", "NEWLINE" ]:
            stm.next()
            return True
        return False

    def is_rule_body_end(self, stm):
        if self.is_rule_end(stm): return True
        tkn = stm.peek()
        return tkn.tp == "SEP" or is_candi_op(tkn, ["=>", "::"])

    def build_ast(self, stm):
        while True:
            self.newlines(stm)
            if stm.eof(): break
            tkn = stm.peek()
            if tkn.tp == 'EXPORT':
                val = self.ast_export(stm)
            elif tkn.tp == 'VAR':
                val = self.ast_rule(stm)
            elif tkn.tp == 'ATOM':
                val = self.ast_atom(stm)
            else:
                Error("Unexpeted begining token %s"%tkn.val)
            self.ast.append(val)

    def ast_export(self, stm):
        stm.next()
        rule = self.ast_rule_helper(stm, True)
        params = self.ast_params(stm)
        intent_slot = self.ast_intent_slot(stm)
        weight = self.ast_weight(stm)
        syntax_cond_assert(self.is_rule_end(stm), "expected rule end")

        return {"tp": "EXPORT", "name": body["rule_name"], "body": rule["body"], 
                    "params":params, "intent_slot":intent_slot, "weight":weight}

    def ast_rule(self, stm):
        stm.next()
        rule = self.ast_rule_helper(stm, False)
        post_func = self.ast_rule_post_func(stm)
        syntax_cond_assert(self.is_rule_end(stm), "expected rule end")
        return {"tp": "RULE", "name":rule["rule_name"], "body": rule["body"], "post_func": post_func }

    def ast_atom(self, stm):
        stm.next()
        rule = self.ast_atom_helper(stm, True)
        return {"tp": "ATOM", "val": rule }


    def ast_rule_helper(self, stm, is_export=False):
        syntax_assert(stm.peek(), "STR", stm.peek().tp)
        rule_name = stm.next().val
        syntax_assert(stm.next(), ("OP", "="), "%s need = here"%rule_name)
        body = self.ast_rule_body(stm)
        return {"tp": "RULE_BODY", "rule_name": rule_name, "body": body }

    def ast_rule_parn_helper(self, stm):
        body = []
        while True:
            ele = self.ast_rule_body(stm)
            body.append(ele)
            if not stm.eof():
                syntax_check(stm.next(), ("SEP", "SEMI"))
            if stm.eof(): break
        syntax_cond_assert(len(body) >= 1, "empty parn")
        return body

    def ast_rule_body(self, stm):
        vals, op = [], None
        while True:
            ele = self.ast_compose_rule_ele(stm)
            vals.append(ele)
            if self.is_rule_body_end(stm): break
            if syntax_check(stm.peek(), ("SEP", "SEMI")): break
            syntax_cond_assert(stm.next(), ("OP", "|"), "need | here") 
        if len(vals) == 1: return vals[0]
        return {"tp":"OR_ELE", "val":vals}

    def ast_rule_ele(self, stm):
        tkn = stm.next()
        if tkn.tp in ["PARN", "LIST", "DICT"]:
            parn_body = self.ast_rule_parn_helper(stream(tkn.val))
            if len(parn_body) == 1:
                return parn_body[0]
            else:
                return {"tp":tkn.tp, "val":parn_body }
        elif is_candi_op(tkn, "$"):
            t = self.ast_try_ref(stm)
            if t: return t
            else: return {"tp": op_type[tkn.val], "val": tkn.val }
        elif is_candi_op(tkn, "|"):
            return {"tp": op_type[tkn.val], "val": tkn.val }
        elif tkn.tp == "OP" and tkn.val == ".":
            return {"tp":"RE_DOT" }
        else:
            syntax_assert(tkn, "STR", "Unexpected %s"%str(tkn.val) )
            return {"tp":"CONSTANT", "val": tkn.val }

    def ast_compose_rule_ele(self, stm):
        v = self.ast_rule_ele(stm)
        if not stm.eof():
            if is_candi_op(stm.peek(), "+*?"):
                suf = stm.next()
                return { "tp": "COMP", "val": v, "op_tkn": suf.val, "op": op_funcs[suf.val] }
            elif stm.peek().tp == "DICT":
                dict_para = stm.next().val
                syntax_cond_assert( len(dict_para) <= 3, "unexpected length %d"%len(v) )
                a = int(dict_para[0].val)
                if len(dict_para) < 3:
                    b = a
                else:
                    b = int(dict_para[2].val)
                return { "tp": "COMP", "val": v, "op_tkn": "a_b_times", "op": op_funcs["a_b_times"] , "range":(a,b)}
            elif stm.peek().tp == "ANGLE":
                suf = stm.next()
                return v
        return v
            
    def ast_atom_body(self, stm):
        eles = []
        while True:
            eles.append(self.ast_atom_ele(stm))
            if self.is_rule_end(stm): break
            syntax_assert(stm.next(), ("OP", "|"), "need |")

        return eles

    def ast_atom_helper(self, stm):
        syntax_assert(stm.peek(), "STR", stm.peek().tp)
        rule_name = stm.next().val
        syntax_assert(stm.next(), ("OP", "="), "%s need = here"%rule_name)
        body = self.ast_atom_body(stm)
        self.ast_same_type_seq(stm, lambda tkn: syntax_check(tkn, ("SEP","SEMI")))

        return body

    def skip_tkns(self, stm, candi):
        while not stm.eof():
            tkn = stm.next()
            if tkn.val not in candi:
                stm.back()
                break

    def ast_intent_slot_helper(self, stm):
        intents, slots = {}, {}
        while not stm.eof(): 
            syntax_cond_assert("STR" in stm.peek().tp, str(stm.peek()) + " in intent parse")
            var_name = stm.next().val
            syntax_assert(stm.next(), ("OP", "="), "%s need = here"%var_name)
            syntax_assert(stm.peek(), "STRING")
            val = stm.next().val
            if "$" in val:
                idx_val = int(val.strip("$"))
                slots[idx_val] = var_name
            else:
                intents[var_name] = val
            # 跳过，
            if not stm.eof(): stm.next()
        return { "intent": intents,  "slot": slots }

    def ast_rule_post_func(self, ori_stm):
        self.skip_tkns(ori_stm, ["=>", "request"])
        i_s_tuple = ori_stm.peek()
        post_func = {"params":{} }
        if i_s_tuple.tp != "PARN": return {}
        ori_stm.next()
        stm = stream(i_s_tuple.val)
        while not stm.eof(): 
            syntax_cond_assert("STR" in stm.peek().tp, str(stm.peek()) + " in post func parse")
            var_name = stm.next().val
            if stm.eof(): break
            if syntax_check(stm.peek(),  ("SEP", "COMMA")):
                post_func["func"] = var_name
                stm.next()
            else:
                syntax_assert(stm.next(), ("OP", "="), "%s need = here"%var_name)
                syntax_assert(stm.peek(), "STRING")
                val = stm.next().val
                if "$" in val:
                    idx_val = int(val.strip("$"))
                    post_func["params"][var_name] = idx_val
                else:
                    post_func["params"][var_name] = val

                if not stm.eof(): stm.next()

        return post_func
                
    def ast_intent_slot(self, stm):
        self.skip_tkns(stm, ["=>", "request"])
        i_s_tuple = stm.next()
        if i_s_tuple.tp == "PARN":
            return self.ast_intent_slot_helper(stream(i_s_tuple.val))
        return {}
    
    def ast_try_ref(self, stm):
        if not stm.eof() and stm.peek().tp == "DICT":
            rval = stm.next().val
            if len(rval) == 1:
                return {"tp": "VAR", "val": rval[0].val }
            else:
                assert rval[0].val == ".", "need ."
                return {"tp": "REF", "val": rval[1].val }

        return None

    def ast_atom_ele(self, stm):
        tkn = stm.next()
        if tkn.tp == "STR":
            return {"tp":"CONSTANT", "val": tkn.val }
        elif is_candi_op(tkn, "$"):
            t = self.ast_try_ref(stm)
            if t and t["tp"] == "REF":
                return t
        Error("Unexpected %s"%tkn.val, tkn.line, tkn.col)
        
    def ast_weight(self, stm):
        while not stm.eof():
            tkn = stm.next()
            if tkn.tp == "SEP" and tkn.val in ["SEMI", "NEWLINE" ]:
                break
            elif tkn.tp == "ANGLE":
                av = "".join( [ t.val for t in tkn.val ])
                return float(av)

        return 1.0

    def ast_params(self, stm):
        if stm.eof() or not syntax_check(stm.peek(), ("OP", "::")): return []
        stm.next()
        params = []
        while not is_rule_body_end(stm):
            tkn = stm.next()
            syntax_assert(tkn, "STR")
            params.append(tkn.val)
            if self.is_rule_body_end(stm): break
            syntax_assert(stm.next(), ("SEP", "SEMI") )

        return params
        
