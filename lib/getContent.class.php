<?php 
header("Content-type:text/html; Charset=utf-8");
require "../vendor/autoload.php";

require "replaceElement.calss.php";
use QL\QueryList;

/**
 * 获取最后内容
 */
class getContent{
    private static $config=[
        "tuiku" => array(
            "title" => array(".article_row_fluid h1",'text'),
            "source" => array(".article_meta .source a",'text'),
            "time" => array(".article_meta .timestamp",'text'),
            "body" => array("#nei",'html')
        ),
        "csdn" => array(),
        "segment" => array(),
        "cnblogs" => array(),//博客园
    ];
    public static function getConfig(){
        return self::$config;
    }
    
    public static function doMark($url){
        $arr = explode('/', $url);
        $name = $arr[count($arr)-1];
        $html = file_get_contents($url);

        // 判断 url 选择方法
        // 
        $content = self::getTuiku($html);
        if($content){
            self::putContent($name,$content,"tuiku");
            echo ".";
            return 1;
        }else{
            echo "X";
            return 0;
        }

    }

    public static function getTuiku($html){
        $config = self::getConfig();
        $rules = $config['tuiku']; // 从config 根据 url 获取

        $data = QueryList::html($html)->rules($rules)->query()->getData();
        $ret = $data->all();

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
        $content = $title .$source .$time .$body ;
        return $content;

    }
    public static function getCSDN($html){}
    public static function getSegment($html){}
    public static function getCnblogs($html){}

    private static function putContent($name,$content,$flag){
        $file = "../out/".$flag.$name.".md";

        if(is_file($file)){
            unlink($file);
        }

        $fp = fopen($file,"a");

        fwrite($fp,$content);
        fclose($fp);
    }
}