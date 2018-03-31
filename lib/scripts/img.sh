#!/bin/bash
# echo $IFS
# 知乎文件批量改名

MY_SAVEIFS=$IFS  # 改变分隔符
# IFS=$(echo -en "\n\b")  
IFS=$'\n'  
# echo $IFS
for i in `ls zhihu*.md`
do
    # echo $i
    name=$i
    nname=`awk -F'## ' 'NR==1{print $2}' $name`
    echo $nname".md";
    mv "./"${name} "./"${nname}".md";
done

IFS=$MY_SAVEIFS  