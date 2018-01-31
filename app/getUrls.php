<?php 
header("Content-type:text/html; Charset=utf-8");
require "../vendor/autoload.php";
use Tools\getContent;

// 批量获取页面上的有效链接
function getUrls(){
    $url = $argv[1];
    $Mark = new getContent();
    $ret = $Mark->getListUrl($url);
    echo $ret;
}