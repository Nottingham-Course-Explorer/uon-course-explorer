#!/bin/bash

git fetch

if [[ -n "$(git log origin/main ^main)" ]]; then
  git rebase origin/main
  source "${PWD}"/.venv/bin/activate
  pip install -r requirements.txt
  sudo systemctl restart uon-ce
fi

sudo systemctl is-active uon-ce