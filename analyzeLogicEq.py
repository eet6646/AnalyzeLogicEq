
import string
import re
import argparse

# UserInput : ReplaceWith
SYMBOL_LOGIC = {
    '*': 'and',   # and
    '&': 'and',
    '+': 'or',    # or
    '|': 'or',
    '\'': 'not',  # not
    '!': 'not',
    '#': '^',     # xor
    '^': '^',
    '(': '(',     # grouping
    ')': ')'
}

SYMBOLS = list(' ()') + sum([[key, value] for key, value in SYMBOL_LOGIC.iteritems()], [])

# Global variables, replaced by input arguments
OUT_FILE = None
VERBOSITY = 1
CONSOLE_QUIET = False


def printV(lvl, msg):
    '''
    Display the message only if the provided level is smaller or equal to the verbosity setting.
    Output to file only if a file handle is provided
    '''
    if lvl <= VERBOSITY:
        if not CONSOLE_QUIET:
            print msg
        if OUT_FILE:
            OUT_FILE.write(msg+'\n')


def toBin(x):
    ''' Convert to binary string'''
    return bin(x)[2:]


def addPad(x, varNum):
    ''' Add '0' padding to the left side of a number 'x' '''
    pad = (varNum - len(x))*'0'
    return pad + x


def getVariables(expr):
    '''Gets variables from a given string expression, returns list'''

    variables = []
    for c in expr:
        if c not in SYMBOLS and c not in variables:
            if c.lower() not in string.lowercase:
                printV(2, "Character '{0}' considered as a variable (intended?)".format(c))
            variables.append(c)
    return variables


def processExpr(expr):
    '''Build the boolean expression, returns the clean ready to evaluate expression'''

    for key, value in SYMBOL_LOGIC.iteritems():
        expr = expr.replace(key, ' '+value+' ')

    # Clean up expression
    expr = ' '.join([x.strip() for x in expr.split()])
    printV(3, "\nBoolean expression:")
    printV(2, "R = " + expr.replace('^', 'xor'))
    return expr


def processInput(expr, out_file, disp_if_res, verbose_lvl):
    ''' Main Function, evaluate the expression '''
    global VERBOSITY, OUT_FILE, CONSOLE_QUIET
    if out_file:
        OUT_FILE = out_file
    VERBOSITY = verbose_lvl

    printV(2, "Boolean Expression Evaluator")
    lExpr = processExpr(expr)
    variables = getVariables(expr)
    varNum = len(variables)
    decMax = 2 ** varNum
    resultPad = 2

    printV(1, '\n' + ' '.join(variables) + ' '*resultPad + '| R')
    printV(1, '=' * (varNum*2 + resultPad + 3))

    for i in xrange(decMax):
        cExpr = lExpr
        listOfBits = addPad(toBin(i), varNum)
        for i, val in enumerate(listOfBits):
            _var = variables[i]  # Variable to replace
            _bit = ' '+val+' '

            # Replace the variable with the corresponding bit
            cExpr = re.sub('((^|\s){v}($|\s))'.format(v=_var), _bit, cExpr)

        result = int(eval(cExpr))

        if disp_if_res == -1:  # print all
            printV(1, ' '.join(listOfBits) + ' '*resultPad + '| ' + str(result))
        elif disp_if_res == result:  # minterms & maxterms
            printV(1, ' '.join(listOfBits) + ' '*resultPad + '| ' + str(result))

    printV(1, '')
    printV(2, 'Done')

    if OUT_FILE:
        OUT_FILE.close()


def runInteractive():
    '''
    If the 'expr' variable is omitted from the arguments, it calls this function.
    This function gets input then calls the processInput(..)
    '''
    expr = ''
    while expr == '':
        expr = raw_input('Enter logic equation: \nR = ')

    print "\n== Options =="
    print "Press enter with no input to use the default value.\n"
    out_file = raw_input('Output to file? (default none)\nfilename: ')
    if not out_file == '':
        out_file = open(out_file, 'w')

    disp_if_res = raw_input('Display minterms, maxterms or both (default both): ')
    if disp_if_res.startswith('min'):
        disp_if_res = 1
    elif disp_if_res.startswith('max'):
        disp_if_res = 0
    else:
        disp_if_res = -1

    verbose_lvl = raw_input('Verbose level [1,2,3] (default 1): ')
    if verbose_lvl not in ['1', '2', '3']:
        verbose_lvl = 1

    console_output = raw_input('Output to console? (Does not affect output to file/verbosity) [y,n] (default y): ')
    if console_output.lower().startswith('n'):
        global CONSOLE_QUIET
        CONSOLE_QUIET = True

    processInput(expr, out_file, disp_if_res, verbose_lvl)

if __name__ == "__main__":
    '''
        Get input from arguments then call processInput(...)
    '''
    parser = argparse.ArgumentParser(description='Evaluate a Boolean Logic Expression', epilog="If 'expr' argument is omitted, the program will run interactively.")
    parser.add_argument("-expr", help='Boolean expression')
    parser.add_argument("-o", "--outputFile", type=argparse.FileType('w'), help="Output to text file")
    group = parser.add_mutually_exclusive_group()
    group.add_argument("-mint", "--minterms", action="store_true", help="Only get minterms")
    group.add_argument("-maxt", "--maxterms", action="store_true", help="Only get maxterms")
    parser.add_argument("-v", "--verbose", type=int, choices=[1, 2, 3], default=1, help='Level 1: Displays the resulting table, Level 2: Same as level 1 including warnings/information, Level 3: Same as level 2 including extra information like minterm/maxterm count')
    parser.add_argument("-cq", "--consolequiet", action="store_true", help='If this flag is provided, no output will display on the console. This does not affect the verbosity and the file output.')
    args = parser.parse_args()

    if not args.expr:
        runInteractive()
    else:
        disp_if_res = -1
        if args.minterms:
            disp_if_res = 1
        elif args.maxterms:
            disp_if_res = 0

        if args.consolequiet:
            CONSOLE_QUIET = True

        processInput(args.expr, args.outputFile, disp_if_res, args.verbose)
