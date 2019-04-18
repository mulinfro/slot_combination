
import builtin, config
import random
from syntax_check import Error

def get_mul_size(objs):
    ans = 1
    for obj in objs:
        ans *= obj.get("size", 1)

def random_a_slot(env, fname):
    if env["__SLOT_WORDS__"]:
        slots = env["__SLOT_WORDS__"][fname]
        return random.choice(slots)
    return "${%s}"%fname

def parse(node):
    if  node["tp"] == 'EXPORT': 
        val = parse_export(node)
    else: 
        val = parse_rule(node)

    return val

def parse_rule_helper(node):
    name = node["rule_name"]
    body = parse_rule_body(node["body"], node["intent"], node["slot"])
    return (name, body)

def parse_rule(node):
    name, body = parse_rule_helper(node)

    def _get_a_rule(env):
        env["__RULE__"][name] = body
    return _get_a_rule

def parse_export(node):
    name, body = parse_rule_helper(node["val"])
    weight = node["weight"]
    def _get_a_export_rule(env):
        env["__EXPORT__"].append( (name, body, weight) )

    return _get_a_export_rule

def parse_rule_body(node, intent, slot):
    if node["tp"] == "JOINT_RULE_BODY":
        ans = parse_joint_body(node, slot, intent)
    elif node["tp"] == "BIN_RULE_BODY":
        ans = parse_bin_body(node)
    else:
        Error("Unexpected body type %s"%node["tp"] )
        
    if config.show_intent and intent:
        intent_out = [ k + "-" + v for k,v in intent.items() if not k.startswith("__") and v ]
        if "__act__" in intent and "__tgt__" in intent and intent["__tgt__"] not in slot.values():
            intent_out.append(intent["__act__"] + '-' + intent["__tgt__"])
        def _warp(env):
            return ans(env) + " => " + ",".join(intent_out)
        return _warp
    return ans

def get_slot_index(node, slot):
    slot_indexes = {}
    j = 1
    for i, ele in enumerate(node):
        if ele["tp"] == "PARN" or (ele["tp"] == "COMP" and ele["val"]["tp"] == "PARN"):
            if j in slot:
                slot_indexes[i] = slot[j]
            j = j + 1
    return slot_indexes

def parse_joint_body(node, slot, intent):
    ele_funcs = [ parse_rule_ele(ele) for ele in node["val"] ]
    slot_indexes = get_slot_index(node["val"], slot)
    def _gen(env):
        parts = []
        for i, ele in enumerate(ele_funcs):
            v = ele(env)
            if v and config.show_slot and i in slot_indexes:
                act = "inform"
                if "__tgt__" in intent and slot_indexes[i] == intent["__tgt__"]:
                    act = intent.get("__act__", "inform")
                v = "{%s:%s:%s}"%(act, v, slot_indexes[i])
            parts.append(v)

        return "".join(parts)
    return _gen

def parse_bin_body_helper(ele, slot):
    if ele["tp"] == "JOINT_RULE_BODY":
        ans = parse_joint_body(ele, slot, {})
    else:
        ans = parse_rule_ele(ele)
    return ans

def parse_bin_body(node):
    ele_funcs = [ parse_bin_body_helper(ele, {}) for ele in node["val"] ]
    def _gen(env):
        parts = [ele(env) for ele in ele_funcs]
        return random.choice(parts)
    return _gen

def parse_comp_ele(node):
    val, op_f = node["val"], node["op"]
    #op_f = builtin.op_funcs[op]
    if val["tp"] in ["PARN", "REF", "VAR", "RE_DOT"]:
        bval = parse_rule_ele(val)
        return op_f(bval)
    elif val["tp"] == "CONSTANT":
        r_val = val["val"]
        pre = "".join(r_val[0:-1])
        bval = lambda env: r_val[-1]
        return lambda env: pre + op_f(bval)(env)
    else:
        Error("comp ele type %s"%val["tp"])

def gen_a_pre_or_suf(env):
    return ""

def get_env_var(env, val):
    if val not in env:
        print(env.keys())
    return env["__RULE__"][val]

def get_a_dot(env):
    if env["__SLOT_WORDS__"] and "__RE_DOT__" in env["__SLOT_WORDS__"]:
        return random.choice(env["__SLOT_WORDS__"]["__RE_DOT__"])
    return ""

def parse_rule_ele(node):
    if node["tp"] == "PARN":
        return parse_rule_body(node["val"], None, {})
    elif node["tp"] == "FANG":
        return lambda env: ""
    elif node["tp"] == "CONSTANT":
        val = node["val"]
        return lambda env: val
    elif node["tp"] == "VAR":
        val = node["val"]
        return lambda env: env["__RULE__"][val](env)
        #return lambda env: get_env_var(env, val)
    elif node["tp"] == "REF":
        val = node["val"]
        return lambda env: random_a_slot(env, val)
        #return lambda env: "${%s}"%val
    elif node["tp"] == "COMP":
        return parse_comp_ele(node)
    elif node["tp"] == "RE_DOT":
        return get_a_dot
    elif node["tp"] == "P0":
        return lambda env: ""
    else:
        Error("rule ele type %s"%node["tp"])
