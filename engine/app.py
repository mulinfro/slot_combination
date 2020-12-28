
from stream import stream, char_stream
import ast, parse, ac, search
from tokens import token_list
import glob, os
from syntax_check import syntax_cond_assert
import time
from selector import Selector


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


class Engine:

    def __init__(self, lex_file, dict_dir):
        self.searcher = None
        self.rule_info = None
        self.build(lex_file, dict_dir)

    def build(self, lex_file, dict_dir):
        ori_in = read_lex(lex_file)
        script = char_stream(ori_in)
        tokens = token_list(script).tokens
        ast_obj = ast.AST(stream(tokens))
        
        # 词典文件目录列表， 逗号分开
        all_slot_entity_files = []
        if dict_dir:
            dict_dirs = dict_dir.split(",")
            for dir_path in dict_dirs:
                all_slot_entity_files.extend(glob.glob(dir_path + "/*.txt"))
        print("词典文件:", all_slot_entity_files)

        # 规则中的关键词
        keywords = ast.extract_all_atoms(ast_obj)
        ac_machine = ac.AC()
        ac_machine.make(keywords, all_slot_entity_files)

        rule_graph = parse.RuleStructure(ast_obj)
        rule_trie, rule_info = rule_graph.build()
        self.searcher = search.Searcher(rule_trie, rule_info, ac_machine)
        self.rule_info = rule_info

    def apply(self, query):
        matched_items, special_post = self.searcher.search_match(query)
        sel = Selector(matched_items, special_post, self.rule_info)
        return sel.apply(query)


def run(lex_file, in_str, in_file, dict_dir):
    engine = Engine(lex_file, dict_dir)

    if in_file:
        lines = open(in_file, encoding="utf-8").readlines()
    else:
        lines = [in_str]

    nums = len(lines)
    time_start=time.time()
    for line in lines:
        query = line.strip()
        if not query: continue
        ans = engine.apply(query)
        print(query, " =>\t",  ans)

    a_time = time.time() - time_start
    print('totally cost', a_time, a_time/nums)


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
