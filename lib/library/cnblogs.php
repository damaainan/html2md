<?php 
namespace Tools\lib;
use QL\QueryList;
use Tools\replaceElement;
use phpQuery;
// header("Content-type:text/html; Charset=utf-8");
class Cnblogs{
    public static function getCnblogs($html,$rules) {

        $data = QueryList::html($html)->rules($rules)->query()->getData();
        $ret = $data->all();
// var_dump($html);
// var_dump($ret);
// die();
        $title = $ret[0]['title'];
        $source = $ret[0]['source'];
        $time = $ret[0]['time'];
        $body = $ret[0]['body'];

        // 代码部分 view code 需要单独处理
        // $body = self::replaceImgTui($body);
        $body = self::replaceHref($body);

        $title = "## " . $title . "\r\n\r\n";
        $time = $time . "\r\n\r\n";
        $source = "来源：[" . $source . "](" . $source . ")" . "\r\n\r\n";
        // file_put_contents("../data/cont.html",$body);
        $replaceElement = new replaceElement();

        $body = $replaceElement->doReplace($body);
        $content = $title . $source . $time . $body;
        return $content;
    }

    private static function replaceHref($html) {
        $doc = phpQuery::newDocumentHTML($html);
        $ch = pq($doc)->find("a");
        foreach ($ch as $ke => $va) {
            $href = pq($va)->attr("href");
            if(!$href){
                continue;
            }
            $te = pq($va)->text();
            $ht = $doc["a:eq($ke)"];
            $html = str_replace($ht, "[$te]($href)", $html);
        }
        return $html;
    }
    // 代码部分特殊处理
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
    public static function replaceImg($html) {
        $doc = phpQuery::newDocumentHTML($html);
        $ch = pq($doc)->find("img");
        foreach ($ch as $ke => $va) {
            $te = pq($va)->attr("data-src");
            $te = "https://segmentfault.com" . explode("?", $te)[0];
            $ht = $doc["img:eq($ke)"];
            $html = str_replace($ht, "\r\n\r\n![]($te)", $html);
        }
        return $html;
    }
}