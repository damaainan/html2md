<?php
namespace Tools;

// header("Content-type:text/html; Charset=utf-8");
require "../vendor/autoload.php";
// require '../phpQuery/phpQuery.php';
// require "replaceElement.calss.php";

// require "config.php"; // 能不能不用引入的方式？

use QL\QueryList;
use Tools\replaceElement;
use Tools\lib\Tuicool;
use Tools\lib\Segmentfault;

/**
 * 获取最后内容
 */
class getContent {
    // 配置文件要独立出来
    /*private static $config = [
    ];*/
    // public $configs = [];
    // function __construct(){ // 这种方式 报错 $this ,可能是类引用的问题
    //      require "config.php"；
    //     $this->configs = $config;
    // }

    public static function getConfig() {
        require "config.php";  // 这样很 low 
        // var_dump($config);
        return $config;
    }

    public static function doMark($url) {
        $configs = self::getConfig();
        // var_dump($configs);die();
        $arr = explode('/', $url);
        $name = $arr[count($arr) - 1];
        $html = file_get_contents($url); // 可以优化为专门的 curl 方法
        // $configs = $this->configs;

        // 判断 url 选择方法
        if (strpos($url, "segmentfault")) {
            $rules = $configs['segmentfault'];
            $obj = new Segmentfault();
            $content = $obj->getSegmentfault($html);
            $flag = 'segmentfault';
        } else if (strpos($url, "tuicool")) {
            $rules = $configs['tuicool'];
            $obj = new Tuicool();
            $content = $obj->getTuiku($html,$rules);
            $flag = 'tuicool';
        } else if (strpos($url, "cnblogs")) {
            $content = self::getCnblogs($html);
            $flag = 'cnblogs';
            $name = explode(".", $name)[0];
        }
        if ($content) {
            self::putContent($name, $content, $flag);
            echo ".";
            return 1;
        } else {
            echo "X";
            return 0;
        }

    }

    private static function putContent($name, $content, $flag) {
        $file = "../out/" . $flag . $name . ".md";
        if (is_file($file)) {
            unlink($file);
        }
        $fp = fopen($file, "a");
        fwrite($fp, $content);
        fclose($fp);
    }
}
