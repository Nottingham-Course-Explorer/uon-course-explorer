#!/bin/bash

git fetch

if [ ! "$(git log origin/main ^main)" ]; then
  git rebase origin/main
  sudo systemctl restart uon-ce
fi
