
""" 参数
 PLUS
 -- min_N
 -- no_cover
 -- max_dist
 SEARCH
 -- no_skip_atom
 -- no_skip_any
 -- max_dist
"""

MULTI_INTENT = True

# 全局基础配置
__plus   = {"min_N":1, "no_cover":1, "max_dist": 0 }
__search = {"no_skip_atom": 0, "no_skip_any": 0, "max_dist": 3}
__export = {}
__atom = {}
__rule = {}

# 用户自定义配置
user_defined_config = {
    "atom_plus": {"max_dist": 0},
    "var_plus" : {"max_dist": 3},
}

def get_base_conf(tp):
    if tp == "plus":
        return __plus
    elif tp == "search":
        return __search
    else:
        return None

def get_conf(name, tp):
    base = get_base_conf(tp)
    ans = {}
    if base:
        ans.update(base)

    if not name:
        return ans

    nconf = user_defined_config.get(name)
    ans.update(nconf)
    return ans

def get_confs(conf_names, tp):
    base = get_base_conf(tp)
    ans = {}
    if base:
        ans.update(base)

    for cname in conf_names:
        nconf = user_defined_config.get(cname)
        ans.update(nconf)

    return ans
