
# sed -i 's@^[ ]\{0,2\}[0-9]\{1,3\}[ ]@@' *.md  # 替换代码行前面的序号

^[ ]{0,2}\d{1,3}[ ]{1}  # 用编辑器执行替换

sed -i 's@```LANG@```java@' *.md

awk -F': ' '/https:\/\/images20/{print $2}' *.md | awk -F'-' '{system("aria2c -o ./img/"$NF" "$0)}'

sed -i 's@https://images[0-9]\{4\}.cnblogs.com/blog/[0-9]\{7\}/[0-9]\{6\}/[0-9]\{7\}-[0-9]\{17\}-@./img/@' *.md

# 根据时间排序 

ls *.md | xargs -I[ awk 'NR==5{print $0"**["}' [ | sort -d | awk -F'**' '{print $2}' | xargs -I[ awk -F'## ' 'BEGIN{sum=0}NR==1{sum++;if(sum<10)print "0"sum$2;else print sum$2}' [


ls cn*.md | xargs -I[ awk -F'## ' 'NR==1{system("mv [ \""$2".md\"")}' [

# 查找 MathJax 公式的正则 
