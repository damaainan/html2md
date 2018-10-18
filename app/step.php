<?php
header("Content-type:text/html; Charset=utf-8");
// set_time_limit(0);
require "../vendor/autoload.php";

use Tools\GetContent;
// require "../lib/getContent.class.php";

// 从脚本参数获取地址  或者 从 文件获取一系列地址
function deal($argc, $argv){
    $urls = [];
    if ($argv[1] === "urls.txt") {
        // 从文本获取地址
        $fp = fopen("urls.txt", "r");
        while (!feof($fp)) {
            $href = fgets($fp);
            $href = trim($href);
            // var_dump($href);
            if ($href) {
                $urls[] = $href;
            }
        }
        fclose($fp);
    } else {
        for ($i = 1; $i < $argc; $i++) {
            $urls[] = $argv[$i];
        }
    }

    // 遍历数组全部采集
    $Mark = new GetContent();
    $num = 0;
    for ($i = 0, $len = count($urls); $i < $len; $i++) {
        $url = $urls[$i];
        $ret = $Mark->doMark($url);
        if($i%10==0){
            sleep(1);
        }
        echo $ret;
        if($ret == '1'){
            $num++;
        }
    }
    echo "\r\n总共 " . $num . " 篇\r\n";
}

deal($argc, $argv);
