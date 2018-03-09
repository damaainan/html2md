<?php 
header("Content-type:text/html; Charset=utf-8");
require "../vendor/autoload.php";
use Tools\Content;

// 批量获取页面上的有效链接
function getUrls($argv){
    $url = $argv[1];
    $Mark = new Content();
    $ret = $Mark->getListUrl($url);
    // echo $ret;
    $fp = fopen('./urls.txt', "a");
    fwrite($fp, "\n");
    foreach ($ret as $val) {
        fwrite($fp, $val."\n");
    }
    fclose($fp);
}
getUrls($argv);