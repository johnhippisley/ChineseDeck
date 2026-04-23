#!/bin/bash

set -euo pipefail

if [[ $# -ne 2 ]]; then
    echo "Usage: $0 PREFIX DIRECTORY"
    exit 1
fi

prefix="$1"
root_dir="$2"

lesson_nums=()

while IFS= read -r csv_file; do
    filename="$(basename "$csv_file")"

    if [[ "$filename" =~ ^lesson_([0-9]+)_vocab\.csv$ ]]; then
        lesson_num="${BASH_REMATCH[1]}"
        full_tag="${prefix}::L${lesson_num}"

        echo -e "\033[0;32mRunning: python3 tag.py \"$csv_file\" \"$full_tag\"\033[0m"
        python3 tag.py "$csv_file" "$full_tag"

        lesson_nums+=("$lesson_num")
    else
        echo -e "\033[0;33mSkipping: $csv_file (filename does not match lesson_XX_vocab.csv)\033[0m"
    fi
done < <(find "$root_dir" -type f -name "*.csv")

echo
mapfile -t sorted < <(printf '%s\n' "${lesson_nums[@]}" | sort -n)
echo "Lessons Processed: $(IFS=', '; echo "${sorted[*]}")"
