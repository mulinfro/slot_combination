
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
    print(ori_in)
    return ori_in

def run(lex_file, in_str, in_file, dict_dir):
    _config = config.Config()
    ori_in = read_lex(lex_file)
    script = char_stream(ori_in)
    tokens = token_list(script).tokens
    ast_obj = ast.AST(stream(tokens), _config)

    print(ast_obj.atom)
    print(ast_obj.plus)
    """
    for k,m in ast_obj.ast.items():
        print(k, m)
    """

    # 词典文件目录列表， 逗号分开
    all_slot_entity_files = []
    if dict_dir:
        dict_dirs = dict_dir.split(",")
        for dir_path in dict_dirs:
            all_slot_entity_files.extend(glob.glob(dir_path + "/*.txt"))
    print(all_slot_entity_files)

    # 规则中的关键词
    keywords = ast.extract_all_atoms(ast_obj)
    ac_machine = build_ac.AC()
    ac_machine.make(keywords, all_slot_entity_files)

    rule_graph = parse.RuleStructure(ast_obj, ac_machine)
    #print("PLUS_FINGERPRINT", rule_graph.plus_fingerprint)
    parser = parse.Parse(rule_graph, ac_machine, _config)
    time_start=time.time()
    time_ori = time_start
    nums = 1
    if in_file:
        lines = open(in_file, encoding="utf-8").readlines()
        nums = len(lines)
        for in_str in lines:
            in_str = in_str.strip()
            if not in_str: continue
            #ans = parser.max_match(in_str.strip())
            ans = parser.search_match(in_str.strip())
            #time_end=time.time()
            #a_time = time_end-time_start
            #print( a_time)
            #time_start = time_end
            print(in_str, ans)
    else:
        #ans = parser.max_match(in_str.strip())
        #print("\nMAX", ans)
        ans = parser.search_match(in_str.strip())
        print("\nSEARCH", ans)
    time_end=time.time()
    a_time = time_end-time_ori
    print('totally cost', a_time, a_time/nums)

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
