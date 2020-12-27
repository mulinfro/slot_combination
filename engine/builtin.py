
keywords = {
     "export": "EXPORT",
     "if":     "IF",
     "end":    "END",
     "atom":   "ATOM",
     "rule":   "RULE",
     "plus":   "PLUS",
     # default modes
     "__ANY__":    "__ANY__",  # .*
     "__SPACE__":  "__SPACE__",
     "__EMPTY__":  "__EMPTY__",
}
op_alp = '|^$?+*=>.:@'

op_info = {
"^": "^",
".": ".",
"$": "$",
"?": "?",
"@": "@",
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
"@": "P0",
}

op_funcs = {
    "+": "+",
    "?": "?",
    "*": "*",
    "a_b_times": "a&b",
}

