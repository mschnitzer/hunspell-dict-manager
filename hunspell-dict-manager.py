#!/usr/bin/python3

#######################################################################################
# author: Manuel Schnitzer
#
# description: small helper for adding words to a hunspell dictionary
# notice: I wrote this because I needed it at SUSE for updating our dictionary.
#         This script is currently not using the best way to manage a dictionary.
#         It is just a wrapper for the bash commands and does nothing else than
#         executing bash commands. I will adjust this in the near future.
#         PS: this is my first real python program so don't complain abaut it! :P
#######################################################################################

import argparse
import os

def arg_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument("-o", help="option (add, del or build)")
    parser.add_argument("-w", help="word")
    parser.add_argument("-f", help="file")
    parser.add_argument("-d", help="dictionary output file")
    content = parser.parse_args()

    return content

def spell_add(args):
    """Adding words to wordlist
    """
    if args.w and args.f:
        if args.w[0] == "'":
            args.w = args.w[1:-1]
            os.system("cat " + args.f + " > /tmp/wordlistmgr.tmp && echo \"" + args.w + "\" >> /tmp/wordlistmgr.tmp && rm " + args.f + " && touch " + args.f + " && sort /tmp/wordlistmgr.tmp | uniq >> " + args.f + " && rm /tmp/wordlistmgr.tmp")
            print("Word added: " + args.w)
        else:
            print("Invalid arguments")

def spell_del(args):
    """Deleting word from wordlist
    """
    if args.w and args.f:
        os.system("cat " + args.f + " > /tmp/wordlistmgr.tmp && cat /tmp/wordlistmgr.tmp | grep -v ^" + args.w + "$ > " + args.f + " && rm /tmp/wordlistmgr.tmp")
        print("Deleted word: " + args.w)
    else:
        print("Invalid arguments")


def spell_build(args):
    """Build dictionary
    """
    if os.geteuid() != 0:
        print("You have to be root to build the dictionary because you can't touch the /usr/share/myspell directory as user.")
    else:
        if args.d and args.f:
            os.system("wc -l " + args.f + " > /usr/share/myspell/" + args.d + ".dic && sort " + args.f + " | uniq >> /usr/share/myspell/" + args.d + ".dic && touch /usr/share/myspell/" + args.d + ".aff")
            print("Generated dictionary")
        else:
            print("Invalid arguments")

if __name__ == '__main__':
    args = arg_parser()

    funcmap = { 'add':   spell_add,
          'del':   spell_del,
          'build': spell_build,
        }

    func = funcmap.get(args.o)
    res = func(args)

# EOF