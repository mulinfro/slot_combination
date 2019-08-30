
from stream import stream, char_stream
import ast, parse, build_ac
from tokens import token_list
import glob, os, config
from syntax_check import syntax_cond_assert
import time


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

def run(lex_file, in_str, in_file, dict_dir):

    _config = config.config()
    ori_in = read_lex(lex_file)
    script = char_stream(ori_in)
    tokens = token_list(script).tokens
    ast_tree = ast.AST(stream(tokens), _config)

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
    ac_machine.make(keywords, all_slot_entity_files)

    rule_graph = parse.Rule_structure(ast_tree, ac_machine, _config)
    #print("PLUS_FINGERPRINT", rule_graph.plus_fingerprint)
    parser = parse.Parse(rule_graph)
    if in_file:
        time_start=time.time()
        lines = open(in_file, encoding="utf-8").readlines()
        for in_str in lines:
            #ans = parser.max_match(in_str.strip())
            ans = parser.search_match(in_str.strip())
            print(in_str, ans)
        time_end=time.time()
        a_time = time_end-time_start
        print('totally cost', a_time, a_time/len(lines))
    else:
        ans = parser.max_match(in_str.strip())
        print("\nMAX", ans)
        ans = parser.search_match(in_str.strip())
        print("\nSEARCH", ans)

def build_lex(lex_file, dict_dir):
    pass

if __name__ == "__main__":
    import sys
    ARGV = sys.argv[1:]
    lex_file, in_str, in_file, dict_dir= None, None, None, None
    for i in range(0, len(ARGV) -1):
        if ARGV[i] == "-i":
            lex_file = ARGV[i+1]
        elif ARGV[i] == "-f":
            in_file = ARGV[i+1]
        elif ARGV[i] == "-s":
            in_str = ARGV[i+1]
        elif ARGV[i] == "-d":
            dict_dir = ARGV[i+1]

    syntax_cond_assert(lex_file is not None, "need input lex file")
    syntax_cond_assert(in_str or in_file, "need input str")
    run(lex_file, in_str, in_file, dict_dir)
