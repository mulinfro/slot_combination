import ahocorasick

base_path = "/mnt/lustre/asrdata/home/ll202/data/lex_words/music"
base_path = "/mnt/lustre/asrdata/home/ll202/slot_infer"
base_path = "/home/liangliu/slot_infer"

word_dict_config = {
 "歌曲名" : "GQM",
 "操作": "OP",
 "歌手名": "GSM",
 "介词": "JC",
 "量词": "LC",
}


AC = ahocorasick.Automaton()

def read_and_insert(ac, f, tag):
    for line in open(slot_path + "/" + f):
        line = line.strip()
        ac.add_word(line, (tag, len(line), line))

def build_rule_ac(word_dict_config, all_word_rule_tag):
    # word slots
    for fn, tag in word_dict_config.items():
        read_and_insert(AC, fn, tag)

    # word rule tag
    for word, tag in all_word_rule_tag.items():
        AC.add_word(word, tag)
    AC.make_automaton()


import weighted_interval_scheduling as WIS

def test_text():
    path = base_path + "/music_cle"
    for t in open(path):
        t = t.strip()
        print(t,"#", )
        ans = []
        for end_index, (tag, lg, key) in A.iter(t):
            start_index = end_index - lg + 1
            ans.append(([key,tag], start_index, end_index))
            print(start_index, end_index, t[start_index:end_index+1], key, tag)
        print(WIS.compute_best_cover(ans))
    return ans


test_text()
