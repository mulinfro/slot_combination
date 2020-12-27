
from builtin import op_type, keywords, op_alp, op_info
from syntax_check import *

class token():
    def __init__(self, tkn_type, tkn_val, line=0, col=0):
        self.tp   = tkn_type
        self.val  = tkn_val
        self.line = line
        self.col  = col

    def get(self):
        return (self.tp, self.val)

    def __eq__(self, e):
        return self.get() == e

    def __repr__(self):
        return ("type:%s; val %s; line %d col %d") %(self.tp, self.val, self.line, self.col)


def num(s):
    try:
        return int(s)
    except ValueError:
        return float(s)

class token_list():
    def __init__(self, chars):
        self.chars = chars
        self.pre_token = token("SEP", "NEWLINE")
        self.tokens = self.read_tokens()

    def read_tokens(self):
        tokens = []
        while True:
            self.pre_token = tkn = self.read_a_token()
            if tkn is None:
                return tokens
            tokens.append(tkn)
        
    def read_a_token(self):
        self.read_white_space(" \t")
        if self.chars.eof(): return None
        ch = self.chars.peek()
        if ch in ('"', "'"): tkn = self.read_string()
        elif ch == '#': tkn = self.read_note()
        elif ch == '<': tkn = self.read_list()
        elif ch == '[': tkn = self.read_list_f()
        elif ch == '{': tkn = self.read_hashmap()
        elif ch == '(': tkn = self.read_parn()
        elif str.isdigit(ch): tkn = self.read_num()
        elif ch in op_alp: tkn = self.read_op()
        elif ch in ',\n;':     tkn = self.read_sep()
        else: tkn = self.read_var()
        return tkn

    # 跳过空格
    def read_white_space(self, ss = " \t"):
        while not self.chars.eof() and self.chars.peek() in ss:
            self.chars.next()

    def read_var(self):
        line, col = self.chars.line, self.chars.col
        is_valid = lambda x: x not in '"<>{}[]()#,;\n \t' + op_alp
        var = ""
        while not self.chars.eof() and is_valid(self.chars.peek()):
            var += self.chars.next()
        if var in keywords: 
            kw = keywords[var]
            if kw in ["IF", "END"]:
                return self.read_note()
            return token(kw, var, line, col)
        if var == "":
            Error("Unexpected symbol", line, col)
            
        return token("STR", var, line, col)
        
    def read_list(self):
        return self.read_pair("ANGLE", '>')

    def read_list_f(self):
        return self.read_pair("LIST", ']')

    def read_hashmap(self):
        return self.read_pair("DICT", '}')

    def read_parn(self):
        return self.read_pair("PARN",')')

    # 注释
    def read_note(self):
        while not self.chars.eof() and self.chars.peek() != "\n":
            self.chars.next()
        return self.read_a_token()

    # 读一个() [] or {}
    def read_pair(self, tp, end_ch):
        line, col = self.chars.line, self.chars.col
        val = []
        self.chars.next()
        while not self.chars.eof():
            self.read_white_space(" \t\n")
            ch = self.chars.peek()
            if ch == end_ch:
                self.chars.next()
                return token(tp, val, line, col)
            else:
                val.append(self.read_a_token())
        self.chars.crack('missing ' + end_ch)

    def read_sep(self):
        line, col = self.chars.line, self.chars.col
        ch = self.chars.next()
        if ch == ',':
            self.read_white_space(" \t\n")
            return token('SEP', 'COMMA', line, col)
        elif ch == ';':
            self.read_white_space(" \t\n")
            return token('SEP', 'SEMI', line, col)
        else: 
            return token('SEP', 'NEWLINE', line, col)

    def read_op(self):
        line, col = self.chars.line, self.chars.col
        op = ""
        while self.chars.peek() in op_alp:
            op += self.chars.next()
            if op not in op_info:
                self.chars.back()
                op = op[0:-1]
                break
        return token("OP", op_info[op], line, col)

    def read_num(self):
        line, col = self.chars.line, self.chars.col
        ns = ""
        has_e = False
        while not self.chars.eof():
            ch = self.chars.peek()
            if str.isdigit(ch) or ch in '.Ee':
                ns += ch
                if ch in "Ee": has_e = True
            elif has_e and (ch == '+' or ch == '-'):
                ns += ch     # 科学记数法
            else:
                break

            self.chars.next()
            if ch not in "Ee": has_e = False
        return token("NUM", ns, line, col)

    # String语法与python中一样,可能是 "  ' , 多行string用""" , ''''
    def read_string(self):
        line, col = self.chars.line, self.chars.col
        val = ""
        isEscape = False
        terminal_char = self.chars.next()
        is_multi = self.check_multi_string(terminal_char)
        while not self.chars.eof():
            ch = self.chars.next()
            if isEscape:
                isEscape = False
                if ch in escape_table: val += escape_table[ch]
                else: val += "\\" + ch
            elif ch == '\n' and not is_multi:
                self.chars.crack('missing terminal %s'%terminal_char)
            elif ch == '\\':
                isEscape = True
            elif (ch == terminal_char) and (not is_multi \
                     or self.check_multi_string(ch)) :
                return token('STRING', val, line, col)
            else:
                val += ch

        self.chars.crack('missing terminal %s'%terminal_char)

    def check_multi_string(self, tc):
        if tc != self.chars.peek():  return False
        if self.chars.eof() or tc != self.chars.looknext(): return False
        self.chars.next(), self.chars.next()
        return True
