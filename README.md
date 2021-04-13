# getPxoGames

Simple program to get Freespace2 PXO games
Intended to be used on gnome Panel using the seconds to
display one game at a time.

I just really wanna be alerted if a game is in progress is all

Add command to panel
```bash
/bin/bash -c '/usr/bin/python3 /absolute/path/to/getPxoGames.py $(date -u +%s)'
```

https://pxo.nottheeye.com/api/docs/
