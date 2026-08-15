#!/bin/bash
cd "$(dirname "$0")" || exit 1
if [ ! -d ".venv" ]; then
  echo "Creating .venv..."
  python3 -m venv .venv || exit 1
fi
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install matplotlib
python run.py
status=$?
echo
if [ $status -eq 0 ]; then echo "Finished successfully."; else echo "Something failed. See the output above."; fi
read -r -p "Press Enter to close..."
exit $status
