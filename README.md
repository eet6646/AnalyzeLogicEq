AnalyzeLogicEq
==============

Analyze a logic equation

```no-highlight
usage: analyzeLogicEq.py [-h] [-expr EXPR] [-o OUTPUTFILE] [-mint | -maxt]
                         [-v {1,2,3}] [-cq]

Evaluate a Boolean Logic Expression

optional arguments:
  -h, --help            show this help message and exit
  -expr EXPR            Boolean expression
  -o OUTPUTFILE, --outputFile OUTPUTFILE
                        Output to text file
  -mint, --minterms     Only get minterms
  -maxt, --maxterms     Only get maxterms
  -v {1,2,3}, --verbose {1,2,3}
                        Level 1: Displays the resulting table, Level 2: Same
                        as level 1 including warnings/information, Level 3:
                        Same as level 2 including extra information like
                        minterm/maxterm count
  -cq, --consolequiet   If this flag is provided, no output will display on
                        the console. This does not affect the verbosity and
                        the file output.

If 'expr' argument is omitted, the program will run interactively.
```

Example
======

```no-highlight
$ python analyzeLogicEq.py -expr "A|B&(C^D)" -o "output.txt"
```

```no-highlight
A B C D  | R
=============
0 0 0 0  | 0
0 0 0 1  | 0
0 0 1 0  | 0
0 0 1 1  | 0
0 1 0 0  | 0
0 1 0 1  | 1
0 1 1 0  | 1
0 1 1 1  | 0
1 0 0 0  | 1
1 0 0 1  | 1
1 0 1 0  | 1
1 0 1 1  | 1
1 1 0 0  | 1
1 1 0 1  | 1
1 1 1 0  | 1
1 1 1 1  | 1
```

```no-highlight
$ python analyzeLogicEq.py -expr "A|B&(C^D)" -mint
```

```no-highlight
A B C D  | R
=============
0 1 0 1  | 1
0 1 1 0  | 1
1 0 0 0  | 1
1 0 0 1  | 1
1 0 1 0  | 1
1 0 1 1  | 1
1 1 0 0  | 1
1 1 0 1  | 1
1 1 1 0  | 1
1 1 1 1  | 1
```

```no-highlight
$ python analyzeLogicEq.py
```

```no-highlight
Enter logic equation:
R = A | B & (D ^ (B & C))

== Options ==
Press enter with no input to use the default value.

Output to file? (default none)
filename: output_sample.txt
Display minterms, maxterms or both (default both): both
Verbose level [1,2,3] (default 1): 3
Output to console? (Does not affect output to file/verbosity) [y,n] (default y): n

-- see output_sample.txt
```