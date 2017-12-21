<?php 
header("Content-type:text/html; Charset=utf-8");
$str=file_get_contents("../1.css");

/////***********************1

preg_match_all('/[\{|;]\s{0,1}([a-z-]*)[^:\};\s]/', $str, $matches);

// var_dump($matches[0]);
$s=$matches[0];
foreach ($s as &$value) {
	$value = str_replace(array(' ',';','{'),array('','',''),$value);
}
$stt=implode($s,',');
// var_dump($stt);

/////***********************2
$cssStr = <<<EOD
table{width:100%;border-collapse: collapse;color:#111;font-size: 12px;}
.table-bordered td {  border: 1px solid #CCC !important;  }  
th{padding-right: 20px;text-align: right;width:300px;}
.local td{padding-left: 20px;height:36px;width:25%;}
.local tr>td:nth-child(1),.local tr>td:nth-child(3){background: #DDD;text-align: right}
.local tr>td:nth-child(2),.local tr>td:nth-child(4){text-align: left}
.img_board1{width:200px;margin:5px 5px;height:100px;}
.img_board2{width:100px;margin:5px 5px;height:100px;}
#progress{text-align: center;font-size: 16px;margin:20px 0;font-weight: bold;}
#prief_info{font-size: 16px;}
h1{font-size: 24px;font-weight: bold;margin:10px 0;}
h5{margin:5px 0;font-weight: bold;}
#back_list hr{height:1px;border:none;border-top:1px solid #DDD;margin:5px 0;}
#back_list b{font-size: 14px;font-weight: bold;}
#title_list{background: #f2f2f2;line-height: 20px;padding: 8px 0;}
#title_list span{margin:0 4px;}
EOD;

// 必须有空行
preg_match_all('/width\s{0,1}:\s{0,1}(.*?)[^:];/',$cssStr,$match);
// var_dump($match[0]);

// 将第一步获取的属性 遍历组合 剔除需要保留的属性 其余全部替换
// 
// 还需要去除不用的 元素 ，放在第一步  减少操作

$css=preg_replace('/width\s{0,1}:\s{0,1}(.*?)[^:];/','',$cssStr);
// 多次重复 将无关属性全部替换 
echo $css;


/////***********************3 

// 将对应元素的样式 加到页面行内样式上