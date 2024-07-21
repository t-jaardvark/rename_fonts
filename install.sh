#!/bin/bash
# install.sh
pdir="rename_fonts.py"
bin=""

bin="rename_fonts"
[ -f "$HOME/git/repo/mybin/$bin" ] && rm "$HOME/git/repo/mybin/$bin"
ln $HOME/git/repo/myscripts/$pdir/$bin $HOME/git/repo/mybin/$bin
