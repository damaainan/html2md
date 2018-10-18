
# 添加png 后缀
awk -F': ' '/img/{print  $2}' *.md | xargs -I[ sed -i "s@[@[.png@" seg*.md
# 替换网址

sed -i 's@ https://segmentfault.com/img/@ ./img/@' seg*.md

awk -F': ' '/img/{print $2}' seg*.md | awk -F'[?/]' '{system("aria2c -o "$5".png "$0)}'

awk -F': ' '/img/{print $2}' seg*.md | awk -F'/view' '{print $1}'

awk -F': ' '/img/{print $2}' seg*.md | awk -F'/view' '{system("sed -i \"s@"$0"@"$1".png@\" seg*.md")}'

# 重命名 

ls seg*.md | xargs -I[ awk -F'## ' 'NR==1{print $2}' [
ls seg*.md | xargs -I[ awk -F'## ' 'NR==1{system("mv [ \""$2".md\"")}' [
