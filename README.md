# html2md
一个小工具，抓取html主体部分，并转化为markdown

已基本可以使用，将待抓取的页面地址存入 `urls.txt` ，执行 `php step.php urls.txt` 即可


### 可抓取网站列表
参考 `Config.php` 文件


### 执行步骤

文章地址追加写入 `urls.txt` ，执行  `sh sh.sh`

#### 批量获取页面上的有效链接写入 `urls.txt`

`php getUrls.php url`

支持的网站 参考 `Config.php` 文件

## 看云广场书籍抓取

`php book.php url`