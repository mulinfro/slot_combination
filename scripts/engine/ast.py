
from builtin import op_type, op_funcs
from syntax_check import *
from stream import stream

def is_candi_op(tkn, candi):
    return tkn.tp == "OP" and tkn.val in candi

class AST():
    def __init__(self, tokens):
        self.ast = []
        self.build_ast(tokens)

    def build_ast(self, stm):
        while True:
            self.newlines(stm)
            if stm.eof(): break
            tkn = stm.peek()
            if tkn.tp == 'EXPORT':
                val = self.ast_export(stm)
            else:
                val = self.ast_rule(stm)
            self.ast.append(val)

    def newlines(self, stm):
        is_valid = lambda tkn: syntax_check(tkn, ("SEP","NEWLINE"))
        vals = self.ast_same_type_seq(stm, is_valid)
        return len(vals) > 0

    def ast_same_type_seq(self, stm, is_valid):
        tps = []
        while not stm.eof() and is_valid(stm.peek()):
            tps.append(stm.next().val)
        return tps

    def ast_rule(self, stm, is_export=False):
        syntax_assert(stm.peek(), "STR", stm.peek().tp)
        rule_name = stm.next().val
        syntax_assert(stm.next(), ("OP", "="), "%s need = here"%rule_name)
        body = self.ast_rule_body(stm)
        intent_slot = self.ast_intent_slot(stm, is_export)
        weight = self.ast_weight(stm)
        self.ast_same_type_seq(stm, lambda tkn: syntax_check(tkn, ("SEP","SEMI")))

        return {"tp": "RULE", "rule_name": rule_name, "body": body, "weight": weight,
                "intent":intent_slot.get("intents", {}), "slot":intent_slot.get("slots", {})}

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
                val = int(val.strip("$"))
                slots[val] = var_name
            else:
                intents[var_name] = val
            # 跳过，
            if not stm.eof(): stm.next()
        return { "intents": intents,  "slots": slots }

    def ast_intent_slot(self, stm, is_export):
        if not is_export: return {}
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

    def ast_joint_ele_helper(self, stm):
        vals , op = [], None
        while not stm.eof():
            tkn = stm.peek()
            if tkn.tp == "SEP" or is_candi_op(tkn, ["=>"]): break
            ele = self.ast_compose_rule_ele(stm)
            if ele["tp"] == "BIN":
                op = ele
                break
            else:
                vals.append(ele)

        joint_ele = {"tp": "JOINT_RULE_BODY", "val": vals}
        return joint_ele, op

        
    # 1. 连续的eles， 2. “|” 可选的eles
    def ast_rule_body(self, stm):
        joint_eles, bin_ops = [], []
        while True:
            joint_ele, op = self.ast_joint_ele_helper(stm)
            if not joint_ele: break
            joint_eles.append(joint_ele)
            if op is None: break
            bin_ops.append(op)

        if len(joint_eles) == 1:
            return joint_eles[0]
        else:
            return {"tp": "BIN_RULE_BODY", "val": joint_eles, "op": bin_ops }

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
                return { "tp": "COMP", "val": v, "op_tkn": "a_b_times", "op": op_funcs["a_b_times"](a, b) }
            elif stm.peek().tp == "ANGLE":
                suf = stm.next()
                return v
        return v
            
    def ast_rule_ele(self, stm):
        tkn = stm.next()
        if tkn.tp == "PARN":
            parn_body = self.ast_rule_body(stream(tkn.val))
            return {"tp":"PARN", "val":parn_body }
        elif is_candi_op(tkn, "$"):
            t = self.ast_try_ref(stm)
            if t: return t
            else: return {"tp": op_type[tkn.val], "val": tkn.val }
        elif is_candi_op(tkn, "^|"):
            return {"tp": op_type[tkn.val], "val": tkn.val }
        elif tkn.tp == "FANG":
            return {"tp":"FANG" }
        elif tkn.tp == "OP" and tkn.val == ".":
            return {"tp":"RE_DOT" }
        else:
            syntax_assert(tkn, "STR", "Unexpected %s"%str(tkn.val) )
            return {"tp":"CONSTANT", "val": tkn.val }

    def ast_weight(self, stm):
        while not stm.eof():
            tkn = stm.next()
            if tkn.tp == "SEP" and tkn.val in ["SEMI", "NEWLINE" ]:
                break
            elif tkn.tp == "ANGLE":
                av = "".join( [ t.val for t in tkn.val ])
                return float(av)

        return 1.0

    def ast_export(self, stm):
        stm.next()
        rule = self.ast_rule(stm, True)
        return {"tp": "EXPORT", "val": rule, "weight": rule["weight"] }
