
# 添加png 后缀
awk -F': ' '/img/{print  $2}' *.md | xargs -I[ sed -i "s@[@[.png@" seg*.md
# 替换网址

sed -i 's@ https://segmentfault.com/img/@./img/@' seg*.md