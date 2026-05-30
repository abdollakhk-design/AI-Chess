#!/bin/zsh

cd /Users/abdollakhkhalil/Desktop/python.py

if [ -d ".venv" ]; then
  . .venv/bin/activate >/dev/null 2>&1
fi

python3 ai_chess/main.py

echo
echo "Ойын жабылды. Бұл терезені жабу үшін Enter басыңыз."
read
