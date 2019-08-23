
from env import Env

from stream import stream, char_stream
import ast, parse, builtin, build_ac
import random
from tokens import token_list
import glob, os, config, math
from syntax_check import syntax_cond_assert


def argmax(l):
    index, max_val = -1, -1
    for i in range(len(l)):
        if l[i] > max_val:
            index, max_val = i, l[i]
    print(index, max_val)
    return index

def read_lex(lex_file):
    if os.path.isdir(lex_file):
        files = glob.glob(lex_file + "/*.lex")
    else:
        files = lex_file.split(",")
    ori_in = ""
    for file_name in files:
        with open(file_name, encoding="utf-8") as f:
            ori_in += f.read()
    return ori_in

def run(lex_file, input_str, dict_dir):
    ori_in = read_lex(lex_file)
    script = char_stream(ori_in)
    tokens = token_list(script).tokens
    ast_tree = ast.AST(stream(tokens))

    print(ast_tree.atom)
    print(ast_tree.plus)
    """
    for k,m in ast_tree.ast.items():
        print(k, m)
    """

    all_slot_entity_files = []
    if dict_dir:
        all_slot_entity_files = glob.glob(dict_dir + "/*.txt")
    keywords = ast.extract_all_atoms(ast_tree)
    ac_machine = build_ac.AC()
    ac_machine.init(keywords, all_slot_entity_files)

    _config = config.config()
    rule_graph = parse.Rule_structure(ast, ac_machine, _config)
    parser = parse.Parse(rule_graph)
    ans = parser.match(input_str)
    print(ans)

def build_lex(lex_file, dict_dir):
    pass

if __name__ == "__main__":
    import sys
    ARGV = sys.argv[1:]
    lex_file, input_str, dict_dir= None, None, None
    for i in range(0, len(ARGV) -1):
        if ARGV[i] == "-i":
            lex_file = ARGV[i+1]
        elif ARGV[i] == "-s":
            input_str = ARGV[i+1]
        elif ARGV[i] == "-d":
            dict_dir = ARGV[i+1]

    syntax_cond_assert(lex_file is not None, "need input lex file")
    syntax_cond_assert(input_str is not None, "need input str")
    run(lex_file, input_str, dict_dir)
