
import builtin, config
import random
from syntax_check import Error

def get_ref_cnt(fname):
    def _helper(env):
        if env["__SLOT_WORDS__"]:
            slots = env["__SLOT_WORDS__"][fname]
            idx = env["__IDX__"]
            env["__EXPORT_SLOT_CNT__"][idx] += len(slots)
        return 1
    return _helper

def parse(node):
    if  node["tp"] == 'EXPORT': 
        val = parse_export(node)
    else: 
        val = parse_rule(node)

    return val

def parse_rule_helper(node):
    name = node["rule_name"]
    body = parse_rule_body(node["body"], node.get("intent", {}), node.get("slot", {}))
    return (name, body)

def gen_export_cnt(env):
    i = 0
    env["__EXPORT_SLOT_CNT__"] = [0] * len(env["__EXPORT_CNT_BODY__"])
    env["__EXPORT_PATTERN_CNT__"] = [0] * len(env["__EXPORT_CNT_BODY__"])
    for name, body in env["__EXPORT_CNT_BODY__"]:
        env["__IDX__"] = i
        env["__EXPORT_PATTERN_CNT__"][i] = body(env) 
        i += 1

    

def parse_rule(node):
    name, body = parse_rule_helper(node)

    def _get_a_rule(env):
        env["__CNT__"][name] = body
    return _get_a_rule

def parse_export(node):
    name, body = parse_rule_helper(node["val"])
    def _get_a_export_rule(env):
        env["__EXPORT_CNT_BODY__"].append( (name, body) )

    return _get_a_export_rule

def parse_rule_body(node, intent=None, slot={}):
    if node["tp"] == "JOINT_RULE_BODY":
        ans = parse_joint_body(node, slot, intent)
    elif node["tp"] == "BIN_RULE_BODY":
        ans = parse_bin_body(node)
    else:
        Error("Unexpected body type %s"%node["tp"] )
    return ans

def parse_joint_body(node, slot, intent):
    ele_funcs = [ parse_rule_ele(ele) for ele in node["val"] ]
    def _gen(env):
        ans = 1
        for ele in ele_funcs:
            ans *= ele(env)
        return ans
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
        return sum([ele(env) for ele in ele_funcs])
    return _gen

def parse_comp_ele(node):
    val, op_f = node["val"], node["op"]
    #op_f = builtin.op_funcs[op]
    if val["tp"] in ["PARN", "REF", "VAR", "RE_DOT"]:
        bval = parse_rule_ele(val)
        if op_f is builtin.op_funcs["?"]: 
            return lambda env: 2 * bval(env)
        else:
            return lambda env: 3 * bval(env)
    elif val["tp"] == "CONSTANT":
        return lambda env: 2 * 1
    else:
        Error("comp ele type %s"%val["tp"])

def get_env_var(env, val):
    if val not in env:
        print(env.keys())
    return env["__CNT__"][val]

def rule_cache_run(name):
    def _run(env):
        ev = env["__CNT__"][name]
        if type(ev) == int:
            return env["__CNT__"][name]
        else:
            iev = ev(env)
            env["__CNT__"][name] = iev
            return iev

    return _run

def parse_rule_ele(node):
    if node["tp"] == "PARN":
        return parse_rule_body(node["val"])
    elif node["tp"] in ["CONSTANT", "FANG", "RE_DOT"]:
        return lambda env: 1
    elif node["tp"] == "VAR":
        val = node["val"]
        return rule_cache_run(val)
        #return lambda env: get_env_var(env, val)
    elif node["tp"] == "REF":
        val = node["val"]
        return get_ref_cnt(val)
        #return lambda env: "${%s}"%val
    elif node["tp"] == "COMP":
        return parse_comp_ele(node)
    elif node["tp"] == "P0":
        return lambda env: 1
    else:
        Error("rule ele type %s"%node["tp"])
