def get_list_product(lst_of_lst):
    ans = [""]
    for lst in lst_of_lst:
        new_ans = []
        for e in ans:
            for e2 in lst:
                if e2 == "": new_ans.append(e)
                else:     new_ans.append( ("%s_%s"%(e, e2)).strip("_") )
        ans = new_ans
    return ans

class Rule():

    def __init__(self, line, words_dict):
        self.intent = {}
        self.rule_body = []
        self.words_dict = words_dict
        self.parse_rule(line)

    def parse_rule_body(self, rb):
        eles = rb.split(" ")
        for ele in eles:
            if "{" not in ele: continue
                sub_eles = ele.strip("}").split("{")
                val = sub_eles[0].strip()
                tps = sub_eles[1].split(":")
                sym_words = self.words_dict.find_synm(val)
                self.rule_body.append((val, tps[0], tps[1], sym_words))

    def gen_pattern(self):
        lst_of_lst = []
        for pat in self.rule_body:
            if pat[3] is None:
                lst_of_lst.append(["domian"])
            else:
                lst_of_lst.append(pat[3])

        return set(get_list_product(lst_of_lst))

    def parse_rule_intent(self, it):
        intent = eval(it.strip())
        for key in intent:
            if "$" in intent[key]:
                eles = intent[key].split("+")
                new_eles = []
                for e in eles:
                    new_eles.append( int(e.strip("$")) )

                self.intent[key] = new_eles
            else:
                self.intent[key] = intent[key]

    def parse_rule(self, line):
        eles = line.split("=>") 
        self.parse_rule_body(eles[0]) 
        self.parse_rule_intent(eles[1])


def read_all_words(path, rev_dic):
    ans = {}
    for filename in os.listdir(path):
        ans[filename] = []
        new_path = os.path.join(path,filename)
        lines = open(new_path).readlines()
        for line in lines:
            line =  line.strip()
            if not line: continue
            ans[filename].append(line)
            if rev_dic is None: continue
            if line not in rev_dic:
                rev_dic[line] = []
            rev_dic[line].append(filename)

    return ans


class WordDatabase():

    def __init__(self):
        self.word2dicname = {}
        self.general_words = {}
        self.domain_words = {}
        self.general_patterns = {}
        self.patterns2dictname = {}
        self.build_databases()

    def build_databases(self):
        path = "../lexicon/general"
        self.general_words = read_all_words(path, self.word2dicname)
        self.domain_words = read_all_words(path, None)

        path = "../sentence_pattern/general"
        self.general_patterns = read_all_words(path, self.patterns2dictname)

    def find_synm(self, val):
        ans = []
        if val in self.word2dicname:
            for word_name in self.word2dicname[val]:
                ans.extend(self.domain_words[word_name])
        return ans

    def find_similar_patterns(self, pat):
        ans = []
        if pat in self.patterns2dictname:
            for patname in self.patterns2dictname[pat]:
                ans.extend(self.general_patterns[patname])

        return set(ans)
        


def gen_new_rule(pat, rules):
    rules_size = len(rules)
    has_seen = [ False ] * rules_size
    pat_eles = pat.split("_")
    new_rule = []
    for pat in pat_eles:
        for i in range(rules_size + 1):
            if i >= rules_size:
                new_rule.append(("", "", "none", [pat ]) )
            else:
                if has_seen[i]: continue
                if (pat == "domian" and rules[i][1] == "_domian") or \
                    (rules[i][3] and pat in rules[i][3] and rules[i][1] != "_domian"):
                    new_rule.append(rules[i])
                    has_seen[i] = True

    return new_rule


class Model():

    def __init__(self, samples):
        self.samples_file = samples
        self.words_dict = WordDatabase()
        self.rules = []
        self.extend_rules = []


    #读入样本
    # 开通{_act:none}  手机{_domian:d1}  流量{_domian:d2} 业务{_noun:none}  =>  { "intend": "开通业务", "业务": "$2+$3" }
    def read_simples(self):
        lines = open("../projects/" + self.samples_file).readlines()
        for line in lines:
            line = line.strip()
            if line.startswith("#"): continue
                rule = Rule(line, self.words_dict)
                self.rules.append(rule)


    # 搜索&构建同义词词库
    def build_synonyms(self, raw_rules):
        pass


    #搜索&构建句式
    def build_patterns(self):
        has_seen = set()
        for rule in self.rules:
            pats = rule.gen_pattern()
            has_seen.update(pats)
            for pat in pats:
                extend_pats = self.words_dict.find_similar_patterns(pat)
                for e_pat in extend_pats:
                    if e_pat in has_seen: continue
                    new_rule = gen_new_rule(e_pat, rule)
                    self.extend_rules.append(new_rule)
                    has_seen.add(e_pat)
        

    #生成规则
    # export poetry7_4=[{poe操作}, {量词}?, {.古诗_作者}?, {c1}?, {.poe古诗_类别} ]
    def generate_rules(self, rules):
        atoms = []
        new_rules = []
        for rule in self.rules + self.extend_rules:
            new_rule_parts = []
            for ele in rule:
                if ele[3] is None:
                    atoms.append(ele[0])
                    new_rule_parts.append("{}"%ele[0])
                else:
                    t = "|".join(["{.%s}"%ee for ee in ele[3] ])
                    new_rule_parts.append(t)

            new_rules.appen( "[" + ",".join(new_rule_parts) + "]" )

        return (atoms, new_rules)

    #输出规则
    def write2file(self, atoms, new_rules):
        samples_lex_out_file = "../projects/" + self.samples_file + ".lex"
        with open(samples_lex_out_file, "w") as f:
            for atom in atoms:
                f.write( "atom %s = %s"%(atom, atom) + "\n" )

            i = 0
            for rule in new_rules:
                i = i + 1
                f.write( "export rule%d = %s"%(i, rule) + "\n" )

        

    #生成模型
    def generate_stages(self):
        self.read_simples()
        self.build_synonyms()
        self.build_patterns()
        atoms, rules = self.generate_rules()
        self.write2file(atoms, rules)

