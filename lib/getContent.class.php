<?php

header("Content-type:text/html; Charset=utf-8");
require "../vendor/autoload.php";
// require '../phpQuery/phpQuery.php';
// require "replaceElement.calss.php";
use QL\QueryList;
use Tools\replaceElement;
use Tools\lib\Tuicool;
use Tools\lib\Segmentfault;
/**
 * 获取最后内容
 */
class getContent {
    // 配置文件要独立出来
    private static $config = [
        "tuicool" => array(
            "title" => array(".article_row_fluid h1", 'text'),
            "source" => array(".article_meta .source a", 'text'),
            "time" => array(".article_meta .timestamp", 'text'),
            "body" => array("#nei", 'html'),
        ),
        "csdn" => array(
            "title" => array(".article_row_fluid h1", 'text'),
            "source" => array(".article_meta .source a", 'text'),
            "time" => array(".article_meta .timestamp", 'text'),
            "body" => array("#nei", 'html'),
        ),
        "segmentfault" => array(
            "title" => array("#articleTitle a", 'text'),
            "source" => array("#articleTitle a", 'href'),
            // "time" => array(".",'text'),
            "body" => array(".article__content", 'html'),
        ),
        "cnblogs" => array(
            "title" => array("#cb_post_title_url", 'text'),
            "source" => array("#cb_post_title_url", 'href'),
            "time" => array("#post-date", 'text'),
            "body" => array("#nei", 'html'),
        ), //博客园

        "jobbole" => array(
            "title" => array(".article_row_fluid h1", 'text'),
            "source" => array(".article_meta .source a", 'text'),
            "time" => array(".article_meta .timestamp", 'text'),
            "body" => array("#nei", 'html'),
        ), // 伯乐在线
    ];
    public static function getConfig() {
        return self::$config;
    }

    public static function doMark($url) {
        $arr = explode('/', $url);
        $name = $arr[count($arr) - 1];
        $html = file_get_contents($url); // 可以优化为专门的 curl 方法

        // 判断 url 选择方法
        if (strpos($url, "segmentfault")) {
            $obj = new Segmentfault();
            $content = $obj->getSegmentfault($html);
            $flag = 'segmentfault';
        } else if (strpos($url, "tuicool")) {
            $obj = new Tuicool();
            $content = $obj->getTuiku($html);
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

    public static function getCSDN($html) {}



    public static function reCode($html) {
        $doc = phpQuery::newDocumentHTML($html);
        $ch = pq($doc)->find("pre");
        foreach ($ch as $va) {
            $te = pq($va)->text();
            $ht = pq($va)->html();
            $html = str_replace($ht, $te, $html);
        }
        return $html;
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
