
import random

keywords = {
     "export": "EXPORT",
     "if":     "IF",
     "end":    "END",
     "atom":   "ATOM",
     "rule":   "RULE",
     "plus":   "PLUS",
     # default modes
     "ANY":    "ANY",  # .*
     "SPACE":  "SPACE",
}
op_alp = '|^$?+*=>.:'

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
"::": "::",
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
"::": "P0",
}

op_funcs = {
    "+": "+",
    "?": "?",
    "*": "*",
    "a_b_times": "a&b",
}

