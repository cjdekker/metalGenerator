#!/usr/bin/env python3
"""
tab parsing logic divides text as follows with a tab for a 4-string instrument:

xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx\n
xxxx*aaaaaa|aaaaaaa| yyyyyyyy|bbbbbbb|bbbbbbb| yyyyy\n
yyyy|aaaaaa|aaaaaaa| yyyyyyyy|bbbbbbb|bbbbbbb| yyy\n
yyyy|aaaaaa|aaaaaaa| yyyyyyyy|bbbbbbb|bbbbbbb|\n
yyyy|aaaaaa|aaaaaaa| yyyyyyyy|bbbbbbb|bbbbbbb| yyyyyyy\n
yyyy~xxxxxx\n
*ccccccccccccc|\n
|ccccccccccccc|\n
|ccccccccccccc|yyy\n
|ccccccccccccc|\n
~xxxxxxxx\n

'a', 'b', and 'c' areas are passage sections
'a' and 'b' together comprise passage[0]
'c' comprises passage[1]
'y', 'a', 'b', 'c' areas and '|' locations are all in a passage region
'x' area is not in any region

'*'( == '|') begins a new passage as well as a new passage region
'~'( != '|') ends a passage region (at this point we know there are no more strings)

the 'x'/'y' passage region differentiation is meaningful only when we encounter a '\n': if we are in a
passage region we need to increment the string number, if not it's a no-op.
"""
fh = open('tabs/seven_tears.txt', 'r')
#fh = open('tab.txt', 'r')
txt = fh.read()

passage = [] # list of lists-representing-strings composed of concatenated sections
song = [] # to be a list of passages

in_region = in_section = False
region_start_xpos = 0
xpos = 1 # current horizontal index, starting from 1

"""
xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx\n
xxxx*aaaaaa|aaaaaaa| yyyyyyyy|bbbbbbb|bbbbbbb| yyyyy\n
yyyy|aaaaaa|aaaaaaa| yyyyyyyy|bbbbbbb|bbbbbbb| yyy\n
yyyy|aaaaaa|aaaaaaa| yyyyyyyy|bbbbbbb|bbbbbbb|\n
yyyy|aaaaaa|aaaaaaa| yyyyyyyy|bbbbbbb|bbbbbbb| yyyyyyy\n
yyyy~xxxxxx\n
*ccccccccccccc|\n
|ccccccccccccc|\n
|ccccccccccccc|yyy\n
|ccccccccccccc|\n

yyyy|---|----| yyyyyyyy|----|----|\nyy\n|---|----| yyyyyyyy|----|----| yyy\nyyyy~xxxxxx\n ccccccccccccc|\n
"""
def join_region():
    global in_region
    in_region = True
    global region_start_xpos
    region_start_xpos = xpos
    global passage
    passage = [[]]

def leave_region():
    global in_region
    in_region = False
    song.append(list(passage))
    
def join_section():
    global in_section
    in_section = True

def leave_section():
    global in_section
    in_section = False

for C in txt:

    if C == '\n':

        if in_region:
            if xpos < region_start_xpos:
                leave_region()
        if in_section:
            leave_section()

        xpos = 1
    else:
        xpos += 1

    if C == '|':

        if in_region:
            if xpos == region_start_xpos:
                passage.append([]) # new string
        else:
            join_region()

        if not in_section:
            join_section()

        continue

    if C != '|' and xpos == region_start_xpos:
        if in_region:
            leave_region()
        if in_section:
            raise Exception('this should not be')

    if C == ' ' or C =='(':
        if in_section:
            leave_section()
            continue

    if in_section:
        passage[-1].append(C)

for _passage in song:
    print('p:')
    for string in _passage:
        for _t in string:
            print(_t, end='')
        print()

exit()
