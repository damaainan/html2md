<?php 
namespace Tools;

require "../vendor/autoload.php";

class getHtml{
	public static function getUrl($url){
		// 1. 初始化
		 $ch = curl_init();
		 // 2. 设置选项，包括URL
		 curl_setopt($ch,CURLOPT_URL,$url);
		 curl_setopt($ch,CURLOPT_RETURNTRANSFER,1);
		 curl_setopt($ch,CURLOPT_HEADER,0); //https://www.tuicool.com/topics
		 curl_setopt($ch, CURLOPT_USERAGENT, "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3322.4 Safari/537.36");
	    curl_setopt($ch, CURLOPT_REFERER, "https://www.tuicool.com/topics");
	    curl_setopt($ch, CURLOPT_SSL_VERIFYPEER, false); // 跳过证书检查
	    curl_setopt($ch, CURLOPT_SSL_VERIFYHOST, false);  // 从证书中检查SSL加密算法是否存在
		 // 3. 执行并获取HTML文档内容
		 $output = curl_exec($ch);
		 if($output === FALSE ){
		 echo "CURL Error:".curl_error($ch);
		 }
		 // 4. 释放curl句柄
		 curl_close($ch);
		 return $output;
	}
}