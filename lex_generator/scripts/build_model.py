
import tokens, stream
# {我想,?} {听, _act, ?} <{一首,_qua,?} {李白, ?} {的, -} {五言绝句, ?}> {静夜思}   =>  { "intent": "背诵诗歌" }

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

    def __init__(self):
        self.intent = {}
        self.rule_body = []

    def init_with_sample(self, line, words_dict):
        self.words_dict = words_dict
        self.parse_rule(line)

    def init_with_detail(self, rule_body, intent):
        self.rule_body = rule_body
        self.intent = intent

    def parse_rule_body_old(self, rb):
        eles = rb.split(" ")
        for ele in eles:
            if "{" not in ele: continue
            sub_eles = ele.strip("}").split("{")
            val = sub_eles[0].strip()
            tps = sub_eles[1].split(":")
            sym_words = self.words_dict.find_synm_dict(val)
            self.rule_body.append((val, tps[0], tps[1], sym_words))

    def parse_body_ele(self, eles):
        val = eles[0].val
        specil_op = ()
        dict_names = self.words_dict.find_synm_dict(val)
        dict_names_udf = ()
        w_tpye = "none"
        for ee in eles[1:]:
            if ee.tp == "SPECIL_OP":
                specil_op = tuple(ee.val.split("|"))
            elif ee.tp == "TYPE":
                w_tpye = ee.val
            elif ee.tp == "VAR":
                dict_names_udf = tuple(ee.val.split("|"))

        return (val, w_tpye, dict_names, dict_names_udf, specil_op)

    def parse_rule_body_helper(self, tks):
        ans = []
        for ele in tks:
            if ele.tp == "DICT":
                t = self.parse_body_ele(ele.val)
                ans.append(("ELE", t))
            elif ele.tp == "ANGLE":
                t = self.parse_rule_body_helper(ele.val)
                ans.append(("SET", t))
        return tuple(ans)

    def parse_rule_body(self, rb):
        cstream = stream.char_stream(rb)
        tks = tokens.token_list(cstream).tokens
        t = self.parse_rule_body_helper(tks)
        self.rule_body = t
    
    def __str__(self):
        it_str = str(self.intent)
        rb_str = str(self.rule_body)
        return it_str + "\t" + rb_str + "\n"

    def __repr__(self):
        return self.__str__()

    """
    [{'intent': '背诵诗歌'}	[('ELE', ('我想', 'none', ['需求_prefix'], ['?'])), ('ELE', ('听', '_act', [], ['?'])), ('SET', [('ELE', ('一首', '_qua', [], ['?'])), ('ELE', ('李白', 'none', [], ['?'])), ('ELE', ('的', 'none', [], ['-'])), ('ELE', ('五言绝句', 'none', [], ['?']))]), ('ELE', ('静夜思', '_noun', [], []))]
    """
    def gen_pattern_abstract(self):
        lst_of_lst = []
        for pat in self.rule_body:
            if pat[0] == "ELE":
                if pat[1][1] != "none":
                    t = [pat[1][1].strip(" _")]
                    if '?' in pat[1][4]:
                        t.append("")
                    lst_of_lst.append(t)
            elif pat[0] == "SET":
                lst_of_lst.append(["set"])
        return set(get_list_product(lst_of_lst))

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
    import os
    ans = {}
    for filename in os.listdir(path):
        new_path = os.path.join(path, filename)
        if filename.endswith(".txt"):
            file_tp = filename.split(".")[0]
        else:
            file_tp = filename
        ans[file_tp] = []
        lines = open(new_path).readlines()
        for line in lines:
            line =  line.strip()
            if not line or line.startswith("#"): continue
            ans[file_tp].append(line)
            if rev_dic is None: continue
            if line not in rev_dic:
                rev_dic[line] = []
            if file_tp not in rev_dic[line]:
                rev_dic[line].append(file_tp)

    return ans


class WordDatabase():

    def __init__(self):
        self.word2dicname = {}
        self.general_words = {}
        self.domain_words = {}
        self.abstract_patterns = {}
        self.patterns2dictname = {}
        self.build_databases()

    def build_databases(self):
        path = "../lexicon/general"
        self.general_words = read_all_words(path, self.word2dicname)
        self.domain_words = read_all_words(path, None)

        path = "../sentence_pattern/abstract"
        self.abstract_patterns = read_all_words(path, self.patterns2dictname)
        print(self.abstract_patterns)

    def find_synm_words(self, val):
        ans = []
        if val in self.word2dicname:
            for word_name in self.word2dicname[val]:
                ans.extend(self.domain_words[word_name])
        return ans

    def find_synm_dict(self, val):
        return tuple(self.word2dicname.get(val, []))


    def find_similar_patterns(self, pat):
        ans = []
        if pat in self.patterns2dictname:
            for patname in self.patterns2dictname[pat]:
                ans.extend(self.abstract_patterns[patname])

        return set(ans)
        
def get_rule_ele_tp(re):
    if re[0] == "SET":
        return "set"
    elif re[0] == "ELE":
        return re[1][1].strip("_")
    return "none"

def gen_new_rule_abstract(pat, rule):
    rule_body = rule.rule_body
    rules_size = len(rule_body)
    has_seen = [ False ] * rules_size
    pat_eles = pat.split("_")
    new_rule = Rule()
    new_rule_body = []
    for pat in pat_eles:
        for i in range(rules_size):
            if has_seen[i]: continue
            r_tp = get_rule_ele_tp(rule_body[i])
            #print("R_TP", r_tp)
            if pat == r_tp:
                new_rule_body.append(rule_body[i])
                has_seen[i] = True
                break

    new_rule.init_with_detail(new_rule_body, rule.intent)
    return new_rule


def gen_new_rule(pat, rule):
    rule_body = rule.rule_body
    rules_size = len(rule_body)
    has_seen = [ False ] * rules_size
    pat_eles = pat.split("_")
    new_rule = Rule()
    new_rule_body = []
    for pat in pat_eles:
        for i in range(rules_size + 1):
            if i >= rules_size:
                new_rule_body.append(("", "", "none", [pat ]) )
            else:
                if has_seen[i]: continue
                if (pat == "domian" and rule_body[i][1] == "_domian") or \
                    (rule_body[i][3] and pat in rule_body[i][3] and rule_body[i][1] != "_domian"):
                    new_rule_body.append(rule_body[i])
                    has_seen[i] = True
                    break

    new_rule.init_with_detail(new_rule_body, rule.intent)
    #print("PAT", pat_eles)
    #print("NEW_RULE", new_rule)
    return new_rule


class Model():

    def __init__(self, samples):
        self.samples_file = samples
        self.words_dict = WordDatabase()
        self.rules = []
        self.extend_rules = []
        self.rule_cnt = 0


    #读入样本
    # 开通{_act:none}  手机{_domian:d1}  流量{_domian:d2} 业务{_noun:none}  =>  { "intend": "开通业务", "业务": "$2+$3" }
    def read_simples(self):
        lines = open("../projects/" + self.samples_file).readlines()
        for line in lines:
            line = line.strip()
            if line.startswith("#") or not line: continue
            rule = Rule()
            rule.init_with_sample(line, self.words_dict)
            self.rules.append(rule)

        #print("READ SAMPLES", self.rules)


    # 搜索&构建同义词词库
    def build_synonyms(self):
        pass


    #搜索&构建句式
    def build_patterns_abstract(self):
        for rule in self.rules:
            has_seen = set()
            pats = rule.gen_pattern_abstract()
            has_seen.update(pats)
            for pat in pats:
                extend_pats = self.words_dict.find_similar_patterns(pat)
                for e_pat in extend_pats:
                    if e_pat in has_seen: continue
                    new_rule = gen_new_rule_abstract(e_pat, rule)
                    print("PATS", rule, pats, "\n")
                    print("'NEW_RULE", new_rule)
                    self.extend_rules.append(new_rule)
                    has_seen.add(e_pat)
        print("EXTEND_RULES", self.extend_rules)
        

    #生成规则
    # export poetry7_4=[{poe操作}, {量词}?, {.古诗_作者}?, {c1}?, {.poe古诗_类别} ]
    # ('ELE', ('我想', 'none', ['需求_prefix'], ["udf"], ['?']))
    def generate_a_new_rule(self, rules, rv):
        if rv in rules:
            return rules[rv]
        else:
            new_rid = "rule_%d"%self.rule_cnt
            self.rule_cnt += 1
            rules[rv] = new_rid
            return new_rid
            
    def generate_rule_slot(self, re, atoms, rules, plus):
        tp, val = re
        if '-' in  val[4]:
            if val[0] not in atoms: atoms.append(val[0])
            dnames = "{%s}?"%val[0]
        elif val[3]:
            dnames = "|".join(["{.%s}"%ee for ee in val[3]])
        elif val[2]:
            dnames = "|".join(["{.%s}"%ee for ee in val[2]])
        else:
            if val[0] not in atoms: atoms.append(val[0])
            dnames = "{%s}"%val[0]

        if "|" in dnames:
            rule_id = self.generate_a_new_rule(rules, dnames)
            dnames = "{%s}"%rule_id

        if "+" in val[4]:
            #dnames = dnames + "+"
            dnames = "{%s}"%self.generate_a_new_rule(plus, dnames)
        if "?" in val[4]:
            dnames = dnames + "?"
        return dnames

    def generate_rule_ele(self, re, atoms, rules, plus):
        tp, val = re
        if tp == "ELE":
            return self.generate_rule_slot(re, atoms, rules, plus)
        elif tp == "SET":
            t = ",".join([self.generate_rule_ele(ee, atoms, rules, plus) for ee in re[1] ])
            dnames = "<%s>"%t
            rule_id = self.generate_a_new_rule(rules, dnames)
            dnames = "{%s}"%rule_id
            return dnames

    def generate_rules(self):
        atoms = []
        rules = {}
        plus = {}
        export_rules = []
        for rule in self.rules + self.extend_rules:
            new_rule_parts = []
            for ele in rule.rule_body:
                new_rule_parts.append(self.generate_rule_ele(ele, atoms, rules, plus))

            if len(new_rule_parts) > 1:
                export_rules.append( "[" + ",".join(new_rule_parts) + "]" )
            else:
                export_rules.append(new_rule_parts[0])


        #print("ATOM", atoms, export_rules)
        return (atoms, rules, plus, export_rules)

    #输出规则
    def write2file(self, atoms, rules, plus, export_rules):
        samples_lex_out_file = "../projects/" + self.samples_file.split(".")[0] + ".lex"
        with open(samples_lex_out_file, "w") as f:
            for atom in atoms:
                f.write( "atom %s = %s"%(atom, atom) + "\n" )

            for bd, rule_id in rules.items():
                f.write( "rule %s = %s"%(rule_id, bd) + "\n" )

            for bd, rule_id in plus.items():
                f.write( "plus %s = %s"%(rule_id, bd) + "\n" )

            i = 0
            for rule in export_rules:
                i = i + 1
                f.write( "export rule%d = %s"%(i, rule) + "\n" )

            f.write("\n" )

        

    #生成模型
    def generate_stages(self):
        self.read_simples()
        self.build_synonyms()
        self.build_patterns_abstract()
        atoms, rules, plus, export_rules = self.generate_rules()
        self.write2file(atoms, rules, plus, export_rules)

