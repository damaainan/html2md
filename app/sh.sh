#!/bin/bash 

php step.php urls.txt

#  awk -F': ' '/img/{print $2}' tui*.md | awk '{system("aria2c "$0)}'
#  awk -F': ' '/remote/{print $2}' *.md | awk -F'/' '{system("aria2c -o "$NF".png "$0)}'