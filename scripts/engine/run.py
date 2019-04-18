
from env import Env

from stream import stream, char_stream
import ast, parse, builtin, parse_rule_count
import random
from tokens import token_list
import glob, os, config, math
from syntax_check import syntax_cond_assert

def num2weight(k,v, tp="sum"):
    if tp == "log":
        return math.log(k + v)
    else:
        return k + v

def argmax(l):
    index, max_val = -1, -1
    for i in range(len(l)):
        if l[i] > max_val:
            index, max_val = i, l[i]
    print(index, max_val)
    return index

def gen_rule_weight_use_rule_weight(min_rate, rules):
    return gen_rule_weight_use_pattern_num(min_rate, [ [0,wt] for nm, rule, wt in rules])

def gen_rule_weight_uniform(rules):
    n = len(rules)
    return [1/n ] * n

def gen_rule_weight_use_pattern_num(min_rate, pattern_num, tp="sum"):
    ans, s_all = [], 0
    for k,v in pattern_num:
        s_all += num2weight(k + v, tp)
    less_than_min_rate_num, large_than_min_rate_sum = 0, 0
    for k,v in pattern_num:
        rate = num2weight(k + v, tp) / s_all
        if rate <= min_rate:
            less_than_min_rate_num += 1
        else:
            large_than_min_rate_sum += rate
        decay_rate = (1 - less_than_min_rate_num * min_rate ) / large_than_min_rate_sum
    for k,v in pattern_num:
        rate = num2weight(k + v, tp) / s_all
        if rate <= min_rate:
            ans.append( min_rate )
        else:
            ans.append( decay_rate * rate )

    return ans

def gen_a_distribution(rules, pattern_num, min_rate):
    if config.rule_select_strategy == "uniform":
        distribution = gen_rule_weight_uniform(rules)
    elif config.rule_select_strategy == "pattern_num":
        distribution = gen_rule_weight_use_pattern_num(min_rate, pattern_num)
    else:
        distribution = gen_rule_weight_use_rule_weight(min_rate, rules)
    return distribution, sum(distribution)

def random_select_a_rule(distribution, total):
    ra = random.uniform(0, total)
    curr_sum = 0
    for i, wt in enumerate(distribution):
        curr_sum += wt
        if ra <= curr_sum:
            return i

def read_a_slot_txt(filename):
    return open(filename).read().splitlines()

def load_slot_txt(dict_dir):
    dict_pathes = glob.glob(dict_dir + "/*.txt")
    slot_txt_addrs = {}
    for d in dict_pathes:
        name = d.split("/")[-1].split(".")[0]
        slot_txt_addrs[name] = d

    all_slots = {}
    for name, filepath in slot_txt_addrs.items():
        all_slots[name] = read_a_slot_txt(filepath)
    return all_slots

def run(lex_file, N, out_file, dict_dir, min_num):
    #slots = builtin.load_slot_txt()
    env = Env(( "__EXPORT__","__RULE__", "__SLOT_WORDS__","__CNT__", "__EXPORT_CNT_BODY__") , ( [], {}, None, {}, []) )
    if os.path.isdir(lex_file):
        files = glob.glob(lex_file + "/*.lex")
    else:
        files = lex_file.split(",")
    ori_in = ""
    for file_name in files:
        with open(file_name, encoding="utf-8") as f:
            ori_in += f.read()
    script = char_stream(ori_in)
    tokens = token_list(script).tokens
    ast_tree = ast.AST(stream(tokens))

    if dict_dir:
        env["__SLOT_WORDS__"] = load_slot_txt(dict_dir)

    for node in ast_tree.ast:
        parse.parse(node)(env)
        parse_rule_count.parse(node)(env)
        
    parse_rule_count.gen_export_cnt(env)
    patern_nums = list(zip(env["__EXPORT_SLOT_CNT__"], env["__EXPORT_PATTERN_CNT__"]))
    #max_idx = argmax( env["__EXPORT_PATTERN_CNT__"])
    #print(ast_tree.ast[max_idx])
    #print(sum( env["__EXPORT_SLOT_CNT__"]),  sum(env["__EXPORT_PATTERN_CNT__"]) )

    if config.syntax_check_mode:
        print("DONE: syntext right!!!")
        return

    out_handler = None
    if out_file: out_handler = open(out_file, "w", encoding="utf-8")

    min_rate = min_num / N
    rules = env["__EXPORT__"]
    distribution, total = gen_a_distribution(rules, patern_nums, min_rate)
    for i in range(N):
        idx = random_select_a_rule(distribution, total)
        a_sample = rules[idx][1](env)
        if out_handler == None:
            print(a_sample)
        else:
            out_handler.write(a_sample + "\n")

    if out_handler:
        out_handler.close()

if __name__ == "__main__":
    import sys
    ARGV = sys.argv[1:]
    lex_file, out_file, N, dict_dir, min_num  = None, None, None, None, 0
    for i in range(0, len(ARGV) -1):
        if ARGV[i] == "-i":
            lex_file = ARGV[i+1]
        elif ARGV[i] == "-o":
            out_file = ARGV[i+1]
        elif ARGV[i] == "-n":
            N = int(ARGV[i+1])
        elif ARGV[i] == "-mn":
            min_num = int(ARGV[i+1])
        elif ARGV[i] == "-d":
            dict_dir = ARGV[i+1]

    syntax_cond_assert(lex_file is not None, "need input lex file")
    syntax_cond_assert(N is not None, "need output samples number")
    run(lex_file, N, out_file, dict_dir, min_num)
