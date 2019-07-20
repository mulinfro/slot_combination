
import builtin, config
from syntax_check import Error

all_nessary_set, all_rules = {}, {}
all_word_rule_tag = {}
all_word_dicts = []

def parse(nodes):
    global all_nessary_set, all_rules
    for node in nodes:
        name = node["name"]
        all_rules[name] = node["body"]

    for name, body in all_rules.items():
        if name in all_nessary_set: continue
        all_nessary_set[name] = parse_a_rule(body)

def parse_a_rule(node):
    if  node["tp"] == 'EXPORT': 
        val = parse_export(node)
    elif  node["tp"] == 'ATOM': 
        val = parse_atom(node)
    else: 
        val = parse_rule(node)

    return set(val)

def parse_atom(node):
    ans = []
    for ele in node["val"]:
        if ele["tp"] == "CONSTANT":
            ans.append(ele["val"])

    return ans

def parse_rule(node):
    return parse_rule_body(node)

def parse_export(node):
    return parse_rule_body(node)

def parse_rule_ele(node):
    if node["tp"] == "CONSTANT":
        return [node["val"] ]
    elif node["tp"] in ["PARN", "LIST", "DICT"]:
        return parse_rule_body(node["val"])
    elif node["tp"] == "VAR":
        return rule_cache_run(node["val"])
    elif node["tp"] == "REF":
        global all_word_dicts
        all_word_dicts.append(node["val"])
        return []
    elif node["tp"] == "COMP":
        return parse_comp_ele(node)
    elif node["tp"] == "P0":
        return []
    else:
        Error("rule ele type %s"%node["tp"])

def parse_rule_body(node):
    if node["tp"] == "OR_ELE":
        ans = parse_joint_body(node)
    else:
        ans = parse_rule_ele(node)
    return ans

def parse_joint_body(node):
    ans = []
    for ele in node["val"]:
        ans.extend( parse_rule_ele(ele))
    return ans

def parse_comp_ele(node):
    val, op_f = node["val"], node["op_tkn"]
    bval = parse_rule_ele(val)
    if op_f == "+":
        return bval
    elif op_f == "a_b_times" and node["range"][0] > 0:
        return bval
    else:
        return []

def rule_cache_run(name):
    if name in all_nessary_set:
        return all_nessary_set[name]
    else:
        return parse_a_rule(all_rules[name])

