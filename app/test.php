<?php
// 用于断点 xdebug 调试 

header("Content-type:text/html; Charset=utf-8");
// set_time_limit(0);
require "../vendor/autoload.php";

use Tools\GetContent;
// require "../lib/getContent.class.php";

$urls = [];
$urls[] = "https://cpury.github.io/learning-where-you-are-looking-at/";
// 遍历数组全部采集
$Mark = new GetContent();

for ($i = 0, $len = count($urls); $i < $len; $i++) {
    $url = $urls[$i];
    $ret = $Mark->doMark($url);
    if($i%10==0){
        sleep(1);
    }
    echo $ret;
}
