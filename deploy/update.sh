#!/bin/bash

echo "Fetching changes..."
git fetch

if [[ -n "$(git log origin/main ^main)" ]]; then
  echo "Changes detected, updating..."
  git rebase origin/main
  cd "${PWD}"/.venv/bin/activate
  uv sync
  sudo systemctl restart uon-ce
  echo "Done."
else
  echo "No changes detected."
fi
