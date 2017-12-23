<?php

header("Content-type:text/html; Charset=utf-8");
require "../vendor/autoload.php";
require '../phpQuery/phpQuery.php';
require "replaceElement.calss.php";
use QL\QueryList;

/**
 * 获取最后内容
 */
class getContent
{
    private static $config = [
        "tuicool"      => array(
            "title" => array(".article_row_fluid h1", 'text'),
            "source" => array(".article_meta .source a",'text'),
            "time" => array(".article_meta .timestamp",'text'),
            "body" => array("#nei",'html')
        ),
        "csdn"         => array(
            "title"  => array(".article_row_fluid h1", 'text'),
            "source" => array(".article_meta .source a", 'text'),
            "time"   => array(".article_meta .timestamp", 'text'),
            "body"   => array("#nei", 'html'),
        ),
        "segmentfault" => array(
            "title"  => array("#articleTitle a", 'text'),
            "source" => array("#articleTitle a", 'href'),
            // "time" => array(".article_meta .timestamp",'text'),
            "body"   => array(".article__content", 'html'),
        ),
        "cnblogs"      => array(
            "title"  => array(".article_row_fluid h1", 'text'),
            "source" => array(".article_meta .source a", 'text'),
            "time"   => array(".article_meta .timestamp", 'text'),
            "body"   => array("#nei", 'html'),
        ), //博客园
    ];
    public static function getConfig()
    {
        return self::$config;
    }

    public static function doMark($url)
    {
        $arr  = explode('/', $url);
        $name = $arr[count($arr) - 1];
        $html = file_get_contents($url); // 可以优化为专门的 curl 方法

        // 判断 url 选择方法
        if (strpos($url, "segmentfault")) {
            $content = self::getSegmentfault($html);
            $flag    = 'segmentfault';
        } else if (strpos($url, "tuicool")) {
            $content = self::getTuiku($html);
            $flag    = 'tuicool';
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

    public static function getTuiku($html)
    {
        // 部分网址获取不到内容
        $config = self::getConfig();
        $rules  = $config['tuicool']; // 从config 根据 url 获取

        $data = QueryList::html($html)->rules($rules)->query()->getData();
        $ret  = $data->all();

        $title  = $ret[0]['title'];
        $source = $ret[0]['source'];
        $time   = $ret[0]['time'];
        $body   = $ret[0]['body'];
        $body   = self::replaceImg($body);
        $body   = self::replaceHref($body);

        $title  = "## " . $title . "\r\n\r\n";
        $time   = $time . "\r\n\r\n";
        $source = "来源：[" . $source . "](" . $source . ")" . "\r\n\r\n";
        // file_put_contents("../data/cont.html",$body);
        $replaceElement = new replaceElement();

        $body    = $replaceElement->doReplace($body);
        $content = $title . $source . $time . $body;
        return $content;

    }
    public static function getCSDN($html)
    {}
    public static function getSegmentfault($html)
    {
        $config = self::getConfig();
        $rules  = $config['segmentfault']; // 从config 根据 url 获取

        $data = QueryList::html($html)->rules($rules)->query()->getData();
        $ret  = $data->all();

        $title  = $ret[0]['title'];
        $source = $ret[0]['source'];
        // $time = $ret[0]['time'];
        $body = $ret[0]['body'];
        // var_dump($body);

        // pre 中的 code 需要 去除  pre code .html replacewith .text
        $body = self::reCode($body);
        $body = self::replaceImg($body);
        $body = self::replaceHref($body);

        $title = "## " . $title . "\r\n\r\n";
        // $time= $time."\r\n\r\n";
        $source = "来源：[https://segmentfault.com" . $source . "](https://segmentfault.com" . $source . ")" . "\r\n\r\n";
        // file_put_contents("../data/cont.html",$body);
        $replaceElement = new replaceElement();

        $body    = $replaceElement->doReplace($body);
        $content = $title . $source . $body;
        return $content;
    }
    public static function getCnblogs($html)
    {}

    public static function reCode($html)
    {
        $doc = phpQuery::newDocumentHTML($html);
        $ch  = pq($doc)->find("pre");
        foreach ($ch as $va) {
            $te   = pq($va)->text();
            $ht   = pq($va)->html();
            $html = str_replace($ht, $te, $html);
        }
        return $html;
    }

    public static function replaceImg($html)
    {
        $doc = phpQuery::newDocumentHTML($html);
        $ch  = pq($doc)->find("img");
        foreach ($ch as $ke => $va) {
            $te   = pq($va)->attr("data-src");
            $ht   = $doc["img:eq($ke)"];
            $html = str_replace($ht, "![]($te)", $html);
        }
        return $html;
    }

    private static function replaceHref($html)
    {
        $doc = phpQuery::newDocumentHTML($html);
        $ch  = pq($doc)->find("a");
        foreach ($ch as $ke => $va) {
            $href = pq($va)->attr("href");
            $te   = pq($va)->text();
            $ht   = $doc["a:eq($ke)"];
            $html = str_replace($ht, "[$te]($href)", $html);
        }
        return $html;
    }
    private static function putContent($name, $content, $flag)
    {
        $file = "../out/" . $flag . $name . ".md";

        if (is_file($file)) {
            unlink($file);
        }

        $fp = fopen($file, "a");

        fwrite($fp, $content);
        fclose($fp);
    }
}
