#!/usr/bin/python3

#######################################################################################
# author: Manuel Schnitzer
#
# description: small helper for adding words to a hunspell dictionary
# notice: I wrote this because I needed it at SUSE for updating our dictionary.
#         This script is currently not using the best way to manage a dictionary.
#         It is just a wrapper for the bash commands and does nothing else than
#         executing bash commands. I will adjust this in the near future.
#         PS: this is my first real python program so don't complain about it! :P
#######################################################################################

import argparse
import os

def arg_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument("-o",
        choices=('add', 'del', 'build'),
        help="option (add, del or build)")
    parser.add_argument("-w", help="word")
    parser.add_argument("-f", help="file")
    parser.add_argument("-d", help="dictionary output file")
    args = parser.parse_args()

    if args.w and args.w[0] == "'":
        # Remove shell quoting
        args.w = args.w[1:-1]

    if args.o in ('add', 'del') and not args.f:
        parser.error("Missing filename")

    if args.o == "build" and os.geteuid() != 0:
        parser.error("You have to be root to build the dictionary because you can't touch the /usr/share/myspell directory as user.")

    return args

def sort_file(args):
    """
    Adds or deletes words in a file

    Avoids race condition by avoiding any intermediate files
    """
    lines=[]
    f = open(args.f, 'r+')
    lines = [ i  for i in f ]

    word = args.w+'\n'

    if args.o == 'add' and word not in lines:
        lines.append(word)
    elif args.o == 'del':
        lines.remove(word)
    else:
        pass

    lines = sorted(list(set(lines)))
    f.seek(0)
    f.writelines(lines)
    f.truncate()
    f.close()

def spell_add(args):
    """
    Adding words to wordlist
    """
    sort_file(args)
    print("Word added: " + args.w)

def spell_del(args):
    """
    Deleting word from wordlist
    """
    sort_file(args)
    print("Deleted word: " + args.w)

def spell_build(args):
    """
    Build dictionary
    """
    num_lines = sum(1 for line in open(args.f))
    wcline = "{} {}\n".format(num_lines, args.f)

    D="/usr/share/myspell/"
    open(D + args.d + ".aff", "w").close()

    sort_file(args.f)
    with open(args.f, "r") as infile:
        with open(D + args.d + ".dic", "w") as outfile:
            outfile.write(wcline)
            for inlines in infile:
                outfile.write(inlines)
    print("Generated dictionary")

if __name__ == '__main__':
    args = arg_parser()

    funcmap = {
        'add':   spell_add,
        'del':   spell_del,
        'build': spell_build,
    }

    func = funcmap.get(args.o)
    res = func(args)
