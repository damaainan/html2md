<?php
header("Content-type:text/html; Charset=utf-8");
require "../vendor/autoload.php";

use Tools\lib\Kancloud;

$url = $argv[1];

// $url = 'https://www.kancloud.cn/wizardforcel/w3school-java/93709';
$ret = Kancloud::getToc($url);
// echo $ret;
$str = $ret['str']; // toc
$href = $ret['href'];
$dir = $ret['dir'];

$fdir = "../out/kancloud/" . $dir;
if (!is_dir($fdir)) {
    mkdir($fdir);
}
file_put_contents($fdir . '/toc.md', $str);

foreach ($href as $val) {
    $arr = explode('*****', $val);
    $name = $arr[0];
    $name = str_replace('/', '-', $name);
    $name = str_replace('amp;', '', $name);
    $name = str_replace(':', '：', $name);
    $name = str_replace('*', '＊', $name); // windows 系统中 英文 * : /  不能参与命名文件
    $name = preg_replace("/\r\n/", '', $name);
    // echo $name;
    $href = $arr[1];
    // echo $name,"\n",$href,"\n";
    $content = Kancloud::getContent($href);
    file_put_contents($fdir . '/' . $name . '.md', $content);
}