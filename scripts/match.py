import ahocorasick

base_path = "/mnt/lustre/asrdata/home/ll202/data/lex_words/music"
base_path = "/mnt/lustre/asrdata/home/ll202/slot_infer"
base_path = "/home/liangliu/slot_infer"


rule_segs = {}

def match(sen):
    all_matched_words = set()
    word_rule_reverse_dict = {} 

    all_rule_need_word_cnt = {}
    rule_cnt = {}
    candicates = []
    for end_index, (tag, lg, key) in AC.iter(sen):
        #start_index = end_index - lg + 1
        if key in word_rule_reverse_dict and key not in all_matched_words: 
            all_matched_words.add(key)
            for word in word_rule_reverse_dict[key]:
                rule_cnt[word] = rule_cnt.get(word,0 ) + 1

    for rule, cnt in rule_cnt.items()
        if cnt == all_rule_need_word_cnt[rule]:
            candicates.append(rule)



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
