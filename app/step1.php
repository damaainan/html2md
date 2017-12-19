<?php 
header("Content-type:text/html; Charset=utf-8");

/**
 * 第一步 获取各部分元素 querylist
 */
require "../vendor/autoload.php";

require "../lib/replaceElement.calss.php";
use QL\QueryList;


// 根据地址区分使用不同的规则 

$url = "https://www.tuicool.com/articles/BVnYBvj";

$arr = explode('/', $url);
$name = $arr[count($arr)-1];


$html = file_get_contents($url);
// $html = file_get_contents("../data/22.html");
$rules = array(
	"title" => array(".article_row_fluid h1",'text'),
	"source" => array(".article_meta .source a",'text'),
	"time" => array(".article_meta .timestamp",'text'),
	"body" => array("#nei",'html')
);

$data = QueryList::html($html)->rules($rules)->query()->getData();
$ret = $data->all();

/**
 * 处理 body 
 */

$title = $ret[0]['title'];
$source = $ret[0]['source'];
$time = $ret[0]['time'];
$body = $ret[0]['body'];


$title = "## ".$title."\r\n\r\n";
$time= $time."\r\n\r\n";
$source = "来源：[".$source."](".$source.")"."\r\n\r\n";

// file_put_contents("../data/cont.html",$body);

$replaceElement = new replaceElement();

$body = $replaceElement->doReplace($body);

$file = "../out/".$name.".md";

if(is_file($file)){
    unlink($file);
}

$fp = fopen($file,"a");

fwrite($fp,$title);
fwrite($fp,$source);
fwrite($fp,$time);
fwrite($fp,$body);
fclose($fp);

// file_put_contents("../out/ret.md",$body);