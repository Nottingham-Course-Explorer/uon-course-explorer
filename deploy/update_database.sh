#!/bin/bash

primary_file="$HOME/ce.sqlite3"
temp_file="$HOME/ce.sqlite3.tmp"

main() {
  echo "Downloading database..."
  curl "$1" --progress-bar --output "$temp_file" && mv "$temp_file" "$primary_file" && echo "Success!"
}

if [[ $# -eq 1 ]]; then
  main "$1"
else
  echo "Provide the URL of the database to update to and no other arguments."
fi
