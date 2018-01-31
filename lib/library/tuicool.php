<?php
namespace Tools\lib;

// require "../../vendor/autoload.php";  // 只需要在父文件引入一次 不需要再次引入

use phpQuery;
use QL\QueryList;
use Tools\replaceElement;

// header("Content-type:text/html; Charset=utf-8");
class Tuicool {
    /**
     * 转载自博客园的会发生跳转 从原链接处理
     * @param  [type] $html [description]
     * @return [type]       [description]
     */
    public static function getTuiku($html, $rules) {
        // var_dump($html);
        // file_put_contents("../data/in.html", $html);
        // $html = file_get_contents("../data/in.html");
        // 部分网址获取不到内容

        // $config = self::getConfig();
        // $rules = $config['tuicool']; // 从config 根据 url 获取
        // $rules = array(
        //     "title" => array(".article_row_fluid h1", 'text'),
        //     "source" => array(".article_meta .source a", 'text'),
        //     "time" => array(".article_meta .timestamp", 'text'),
        //     "body" => array("#nei", 'html'),
        // );
        $data = QueryList::html($html)->rules($rules)->query()->getData();
        $ret = $data->all();
var_dump($html);
die();
        $title = $ret[0]['title'];
        $source = $ret[0]['source'];
        $time = $ret[0]['time'];
        $body = $ret[0]['body'];
        if (strpos($source, "cnblogs")) {
            // cnblogs 处理
        }
        $body = self::replaceHrefTui($body);
        $body = self::replaceImgTui($body);

        $title = "## " . $title . "\r\n\r\n";
        $time = $time . "\r\n\r\n";
        $source = "来源：[" . $source . "](" . $source . ")" . "\r\n\r\n";
        // file_put_contents("../data/cont.html",$body);
        $replaceElement = new replaceElement();

        $body = $replaceElement->doReplace($body);
        $content = $title . $source . $time . $body;
        return $content;

    }

    public static function replaceImgTui($html) {
        $doc = phpQuery::newDocumentHTML($html);
        $ch = pq($doc)->find("img");
        $i = 0;
        $src = '';
        foreach ($ch as $ke => $va) {
            $te = pq($va)->attr("src");
            $ht = $doc["img:eq($ke)"];
            $src .= "\n[$i]: $te";
            $html = str_replace($ht, "\r\n\r\n![][$i]", $html);
            $i++;
        }
        $html = $html . $src;
        return $html;
    }
    private static function replaceHrefTui($html) {
        $doc = phpQuery::newDocumentHTML($html);
        $ch = pq($doc)->find("a");
        $dh = pq($doc)->find("img");
        $count = count($dh);
        $i = $count;
        $src = '';
        foreach ($ch as $ke => $va) {
            $href = pq($va)->attr("href");
            $te = pq($va)->text();
            $ht = $doc["a:eq($ke)"];
            $src .= "\n[$i]: $href";
            $html = str_replace($ht, "[$te][$i]", $html);
            $i++;
        }
        $html = $html . $src;
        return $html;
    }
}