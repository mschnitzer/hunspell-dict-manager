# hunspell-dict-manager
It's a small helper for adding words to a hunspell dictionary.
Note: Only tested with openSUSE13.2

# Examples
Adding a word to a wordlist txt file:
```
./hunspell-dict-manager.py -o add -f wordlist.txt -w MY_WORD
```

Remove a word from a wordlist txt file:
```
./hunspell-dict-manager.py -o del -f wordlist.txt -w MY_WORD
```

Building a dictionary from a wordlist txt file:
```
sudo ./hunspell-dict-manager.py -o build -f wordlist.txt -d dictname
```

A wordlist looks like that:
```
WORD1
WORD2
WORD3
```

Just create an empty txt file and add some words to it by using the add option.

The dictionaries are located in /usr/share/myspell/DICTNAME.dic