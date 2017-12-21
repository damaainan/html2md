<?php 
header("Content-type:text/html; Charset=utf-8");
/**
 * 接收命令行的地址参数
 */
// $argc 个数
// $argc 参数数组
if(count($argv)<2){
	echo "请输入网址";
	return;
}
print_r($argv);

$url=$argv[1];
// 第一步  获取网页内容
		// 有几种情况需要考虑
		// 1.  普通网页
		// 2.  js 生成的网页
 
// 第二步 提取网页的有效内容

// 第三步 根据对应关系 转化为 markdown 内容


// 第四步 