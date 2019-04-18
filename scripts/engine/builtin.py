
from config import DEAUFALT_MAX_REPEAT
import random

keywords = {
     "export": "EXPORT",
     "if": "IF",
     "end": "END",
}
op_alp = '|^$?+*=>.'

op_info = {
"^": "^",
".": ".",
"$": "$",
"?": "?",
"+": "+",
"*": "*",
"|": "|",
"=": "=",
"=>": "=>",
}

op_type = {
"^": "P0",
"$": "P0",
".": "PRE",
"?": "SUF",
"+": "SUF",
"*": "SUF",
"|": "BIN",
"=": "ASSIGN",
"=>": "P0",
}

def a_b_times(a, b):
    candi = list(range(a, b+1))
    return lambda f: lambda env: repeat(env, f, candi)

def repeat(env, f, cand_list):
    n = random.choice(cand_list)
    parts = [f(env) for i in range(n) ]
    return "".join(parts)

op_funcs = {
    "+": lambda f: lambda env: repeat(env, f, list(range(1, DEAUFALT_MAX_REPEAT+1) ) ),
    "?": lambda f: lambda env: repeat(env, f, [0, 1]),
    "*": lambda f: lambda env: repeat(env, f, list(range(0, DEAUFALT_MAX_REPEAT+1) ) ),
    "a_b_times": a_b_times,
}

