


    awk -F': ' '/img/{print $2}' tui*.md | awk '{system("aria2c "$0)}'
    awk -F': ' '/remote/{print $2}' seg*.md | awk -F'/' '{system("aria2c -o "$NF".png "$0)}'
    awk -F': ' '/img/{print $2}' seg*.md | awk -F'/' '{system("aria2c -o "$NF".png "$0)}'

下载图片命令别名

```sh
    ls tui*.md | xargs -I[ awk -F': ' '/img[0-9]{1}\.tuicool/{system("aria2c "$2)}' [ # 正则无效
    ls tui*.md | xargs -I[ awk -F': ' '/img/{system("aria2c "$2)}' [  # 正则无效
    ls tui*.md | xargs -I[ awk -F': ' '/:\/\/img/{system("aria2c "$2)}' [  # 正则有效

    ls tui*.md | xargs -I[ awk -F': ' '/img[0-9]{1}\.tuicool/{print $2}' [ # 这种正则无效
    ls tui*.md | xargs -I[ awk -F': ' '/:\/\/img/{print $2}/{print $2}' [  # 这种正则可以
    ls tui*.md | xargs -I[ awk -F': ' '/img/{print $2}' [ # 不包含正则有效

    ls tui*.md | xargs -I[ sed -i "s@https://img[0-9]\{1\}.tuicool.com@./img@" [
```

    ^[ ]{0,2}\d{1,3}[ ]


掘金图片下载 

    ls jue*.md | xargs -I[ awk -F': ' '/imageView2/{print $2}' [ | awk -F'[/?]' '{system("aria2c -o "$7".png "$0)}'
    
    # 替换图片路径  
    ls jue*.md | xargs -I[ awk -F': ' '/imageView2/{print $2}' [ | awk -F'[/?]' '{system("sed -i \"s@"$0"@./img/"$7".png@\" jue*.md")}'
    
    imageslim # 动图  
    ls jue*.md | xargs -I[ awk -F': ' '/imageslim/{print $2}' [ | awk -F'[/?]' '{system("aria2c -o "$7".gif "$0)}'
    
    ls jue*.md | xargs -I[ awk -F'## ' 'NR==1{system("mv [ \""$2".md\"")}' [


知乎图片下载 

    awk -F': ' '/zhimg/{system("aria2c "$2)}' zhihu*.md