#!/bin/zsh

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$SCRIPT_DIR"

if [ -d "../.venv" ]; then
  . ../.venv/bin/activate >/dev/null 2>&1
elif [ -d ".venv" ]; then
  . .venv/bin/activate >/dev/null 2>&1
fi

python3 main.py

echo
echo "Ойын жабылды. Бұл терезені жабу үшін Enter басыңыз."
read
