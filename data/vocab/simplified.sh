#!/bin/bash
find . -type f -name '*.csv' -print0 | while IFS= read -r -d '' f; do
  echo "$f"
  opencc -i "$f" -o "$f.tmp" -c t2s.json &&
  mv "$f.tmp" "$f"
done
