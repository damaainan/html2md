


    awk -F': ' '/img/{print $2}' tui*.md | awk '{system("aria2c "$0)}'
    awk -F': ' '/remote/{print $2}' seg*.md | awk -F'/' '{system("aria2c -o "$NF".png "$0)}'
    awk -F': ' '/img/{print $2}' seg*.md | awk -F'/' '{system("aria2c -o "$NF".png "$0)}'
