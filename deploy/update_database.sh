#!/bin/bash

main() {
  primary_file="$HOME/ce.sqlite3"
  temp_file="$HOME/ce.sqlite3.tmp"

  curl "$1" --progress-bar --output "$temp_file" && mv "$temp_file" "$primary_file"
}

if [[ $# -eq 1 ]]; then
  main "$1"
else
  echo "Provide the URL of the database to update to and no other arguments."
fi
