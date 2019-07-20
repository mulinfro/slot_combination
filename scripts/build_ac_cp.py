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

A = ahocorasick.Automaton()

def read_and_insert(A, f, tag):
    for line in open(base_path + "/words/music/" + f):
        line = line.strip()
        A.add_word(line, (tag, len(line), line))


def build_with_config():
    for fn, tag in word_dict_config.items():
        read_and_insert(A, fn, tag)
    A.make_automaton()
    print("A:", len(A))

build_with_config()


test_keys = [
"关晓彤",
"刘德华",
"忘情水",
"播放",
"大大",
]

def test():
    for t in test_keys:
        print(t, A.get(t, None))

#test()

#def 

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
