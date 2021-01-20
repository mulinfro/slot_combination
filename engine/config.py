
""" 
    引擎默认参数定义, 以及用户自定义参数配置项

 PLUS: plus规则的相关参数
 -- min_N:   最少匹配的个数
 -- max_N:   最大匹配个数， 默认无限制
 -- no_cover  搜索时是否不能覆盖, 覆盖就截断
 -- max_dist  元素间最大间隔
 SEARCH: 搜索过程中的相关参数
 -- no_skip_atom
 -- no_skip_any
 -- max_dist
"""

MULTI_INTENT = True

# 全局基础配置
__plus   = {"min_N":1, "max_N": 1000, "no_cover":False, "max_dist": 0 }
__search = {"no_skip_atom": False, "no_skip_any": False, "max_dist": 3}
__export = {}
__atom = {}
__rule = {}

# 用户自定义配置
user_defined_config = {
    "atom_plus": {"max_dist": 0},
    "var_plus" : {"max_dist": 3},
}


def get_base_conf(tp):
    tp = tp.lower()
    if tp == "plus":
        return __plus
    elif tp == "search":
        return __search
    else:
        return None


def get_conf(name, tp):
    """ 
        tp: 规则类型，   name: 配置名
        根据规则类型和配置名，获取参数列表
        先根据tp获取系统默认配置，  再根据name获取用户自定义的配置
        用户自定义的项会覆盖默认配置
    """
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
