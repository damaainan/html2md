<?php 
namespace Tools\lib;

// header("Content-type:text/html; Charset=utf-8");
class Tuicool{

    public static function getTuiku($html) {
        // var_dump($html);
        // file_put_contents("../data/in.html", $html);
        // $html = file_get_contents("../data/in.html");
        // 部分网址获取不到内容
        $config = self::getConfig();
        $rules = $config['tuicool']; // 从config 根据 url 获取

        $data = QueryList::html($html)->rules($rules)->query()->getData();
        $ret = $data->all();

        $title = $ret[0]['title'];
        $source = $ret[0]['source'];
        $time = $ret[0]['time'];
        $body = $ret[0]['body'];
        if (strpos($source, "cnblogs")) {
            // cnblogs 处理
        }
        $body = self::replaceImgTui($body);
        $body = self::replaceHrefTui($body);

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
        foreach ($ch as $ke => $va) {
            $te = pq($va)->attr("src");
            $ht = $doc["img:eq($ke)"];
            $html = str_replace($ht, "\r\n\r\n![]($te)", $html);
        }
        return $html;
    }
    private static function replaceHrefTui($html) {
        $doc = phpQuery::newDocumentHTML($html);
        $ch = pq($doc)->find("a");
        foreach ($ch as $ke => $va) {
            $href = pq($va)->attr("href");
            $te = pq($va)->text();
            $ht = $doc["a:eq($ke)"];
            $html = str_replace($ht, "[$te]($href)", $html);
        }
        return $html;
    }
}