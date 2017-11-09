# ----------------------------------------------------------------------
# clex.py
#
# A lexer for ANSI C.
# ----------------------------------------------------------------------

import sys
sys.path.insert(0, "../..")

import ply.lex as lex

# Reserved words
reserved = (
    'AUTO', 'BREAK', 'CASE', 'CHAR', 'CONST', 'CONTINUE', 'DEFAULT', 'DO', 'DOUBLE',
    'ELSE', 'ENUM', 'EXTERN', 'FLOAT', 'FOR', 'GOTO', 'IF', 'INT', 'LONG', 'REGISTER',
    'RETURN', 'SHORT', 'SIGNED', 'SIZEOF', 'STATIC', 'STRUCT', 'SWITCH', 'TYPEDEF',
    'UNION', 'UNSIGNED', 'VOID', 'VOLATILE', 'WHILE',
)

tokens = reserved + (
    # Literals (identifier, integer constant, float constant, string constant,
    # char const)
    'ID', 'TYPEID', 'ICONST', 'FCONST', 'SCONST', 'CCONST',

    # Operators (+,-,*,/,%,|,&,~,^,<<,>>, ||, &&, !, <, <=, >, >=, ==, !=)
    'PLUS', 'MINUS', 'TIMES', 'DIVIDE', 'MOD',
    'OR', 'AND', 'NOT', 'XOR', 'LSHIFT', 'RSHIFT',
    'LOR', 'LAND', 'LNOT',
    'LT', 'LE', 'GT', 'GE', 'EQ', 'NE',

    # Assignment (=, *=, /=, %=, +=, -=, <<=, >>=, &=, ^=, |=)
    'EQUALS', 'TIMESEQUAL', 'DIVEQUAL', 'MODEQUAL', 'PLUSEQUAL', 'MINUSEQUAL',
    'LSHIFTEQUAL', 'RSHIFTEQUAL', 'ANDEQUAL', 'XOREQUAL', 'OREQUAL',

    # Increment/decrement (++,--)
    'PLUSPLUS', 'MINUSMINUS',

    # Structure dereference (->)
    'ARROW',

    # Conditional operator (?)
    'CONDOP',

    # Delimeters ( ) [ ] { } , . ; :
    'LPAREN', 'RPAREN',
    'LBRACKET', 'RBRACKET',
    'LBRACE', 'RBRACE',
    'COMMA', 'PERIOD', 'SEMI', 'COLON',

    # Ellipsis (...)
    'ELLIPSIS',
)

# Completely ignored characters
t_ignore = ' \t\x0c'

# Newlines


def t_NEWLINE(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")

# Operators
t_PLUS = r'\+'
t_MINUS = r'-'
t_TIMES = r'\*'
t_DIVIDE = r'/'
t_MOD = r'%'
t_OR = r'\|'
t_AND = r'&'
t_NOT = r'~'
t_XOR = r'\^'
t_LSHIFT = r'<<'
t_RSHIFT = r'>>'
t_LOR = r'\|\|'
t_LAND = r'&&'
t_LNOT = r'!'
t_LT = r'<'
t_GT = r'>'
t_LE = r'<='
t_GE = r'>='
t_EQ = r'=='
t_NE = r'!='

# Assignment operators

t_EQUALS = r'='
t_TIMESEQUAL = r'\*='
t_DIVEQUAL = r'/='
t_MODEQUAL = r'%='
t_PLUSEQUAL = r'\+='
t_MINUSEQUAL = r'-='
t_LSHIFTEQUAL = r'<<='
t_RSHIFTEQUAL = r'>>='
t_ANDEQUAL = r'&='
t_OREQUAL = r'\|='
t_XOREQUAL = r'\^='

# Increment/decrement
t_PLUSPLUS = r'\+\+'
t_MINUSMINUS = r'--'

# ->
t_ARROW = r'->'

# ?
t_CONDOP = r'\?'

# Delimeters
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_LBRACKET = r'\['
t_RBRACKET = r'\]'
t_LBRACE = r'\{'
t_RBRACE = r'\}'
t_COMMA = r','
t_PERIOD = r'\.'
t_SEMI = r';'
t_COLON = r':'
t_ELLIPSIS = r'\.\.\.'

# Identifiers and reserved words

reserved_map = {}
for r in reserved:
    reserved_map[r.lower()] = r


def t_ID(t):
    r'[A-Za-z_][\w_]*'
    t.type = reserved_map.get(t.value, "ID")
    return t

# Integer literal
t_ICONST = r'\d+([uU]|[lL]|[uU][lL]|[lL][uU])?'

# Floating literal
t_FCONST = r'((\d+)(\.\d+)(e(\+|-)?(\d+))? | (\d+)e(\+|-)?(\d+))([lL]|[fF])?'

# String literal
t_SCONST = r'\"([^\\\n]|(\\.))*?\"'

# Character constant 'c' or L'c'
t_CCONST = r'(L)?\'([^\\\n]|(\\.))*?\''

# Comments


def t_comment(t):
    r'/\*(.|\n)*?\*/'
    t.lexer.lineno += t.value.count('\n')

# Preprocessor directive (ignored)


def t_preprocessor(t):
    r'\#(.)*?\n'
    t.lexer.lineno += 1


def t_error(t):
    print("Illegal character %s" % repr(t.value[0]))
    t.lexer.skip(1)

# Token class.  This class is used to represent the tokens produced.
class CEnum(object):
    def __str__(self):
        return 'CEnum(%s,%r,%d,%d)' % (self.key, self.id, self.start, self.end)

    def __repr__(self):
        return str(self)

def parseEnum(toks):
    found = False
    tmp = CEnum()
    all = []
    for i in range(0, len(toks)):
        if 'ENUM' == toks[i].type:
            # print(toks[i])
            tmp.key = 'ENUM'
            found = True
            if 'ID' == toks[i+1].type:
                tmp.id = toks[i+1].value
        if 'LBRACE' == toks[i].type and found:
            tmp.start = i
        if 'RBRACE' == toks[i].type and found:
            tmp.end = i
            all.append(tmp)
            found = False

    print(all)


lexer = lex.lex()
if __name__ == "__main__":
    try:
        filename = sys.argv[1]
        f = open(filename)
        data = f.read()
        f.close()
    except IndexError:
        sys.stdout.write('Reading from standard input (type EOF to end):\n')
        data = sys.stdin.read()

    _input = lexer.input
    _input(data)

    tokens = []
    _token = lexer.token
    while True:
        tok = _token()
        if not tok:
            break
        tokens.append(tok)
        sys.stdout.write('(%s,%r,%d,%d)\n' % (tok.type, tok.value, tok.lineno, tok.lexpos))

    #print(tokens)
    parseEnum(tokens)