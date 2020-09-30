# ------------------------------------------------------------
# Processing a log file
# ------------------------------------------------------------
import lex

# List of token names.   This is always required
tokens = [
    'TIMESTAMP',
    'PROC',
    'MESSAGE'
]

t_ignore = ' \t'

def t_TIMESTAMP(t):
    # Regular expression for TIMESTAMP
    r'[0-2][0-9]:[0-5][0-9]:[0-5][0-9]\.[0-9]{1,6}\ [-+][0-9]{4}(?=\t)'
    t.type = 'TIMESTAMP'
    return t

def t_PROC(t):
    # Regular expression for PROC
    r'[a-zA-Z-\.]+(?=\t)'
    # t.value = t.value[1:len(t.value) - 1]
    t.type = 'PROC'
    return t

def t_MESSAGE(t):
    # Regular expression for MESSAGE
    r'[^\t]*\n'

    # t.value = t.value[:len(t.value) - 1]
    t.type = 'MESSAGE'
    return t



# Error handling rule
def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)


class LogProcLexer:
    data = None
    lexer = None

    def __init__(self):
        fh = open("log", 'r')
        self.data = fh.read()
        fh.close()
        self.lexer = lex.lex()
        self.lexer.input(self.data)

    def collect_messages(self):
        tokens = []
        isKernel = False
        while True:
            tok = self.lexer.token()
            if not tok:
                break  # No more input
            if tok.type == 'PROC' and tok.value == 'kernel':
                isKernel = True
            if isKernel and tok.type == 'MESSAGE':
                tokens.append(tok)
                isKernel = False
        return tokens


if __name__ == '__main__':
    print(LogProcLexer().collect_messages())
