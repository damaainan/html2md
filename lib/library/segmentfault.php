<?php
namespace Tools\lib;
use phpQuery;
use QL\QueryList;
use Tools\replaceElement;
use Tools\ToolUtil;

// header("Content-type:text/html; Charset=utf-8");
class Segmentfault {

    public static function getSegmentfault($html, $rules) {
        $data = QueryList::html($html)->rules($rules)->query()->getData();
        $ret = $data->all();

        $title = $ret[0]['title'];
        $source = $ret[0]['source'];
        // $time = $ret[0]['time'];
        $body = $ret[0]['body'];
        // var_dump($body);

        // pre 中的 code 需要 去除  pre code .html replacewith .text
        $body = ToolUtil::reCode($body);
        $body = ToolUtil::replaceHref($body);
        $body = self::replaceImgSeg($body);

        $title = "## " . $title . "\r\n\r\n";
        // $time= $time."\r\n\r\n";
        $source = "来源：[https://segmentfault.com" . $source . "](https://segmentfault.com" . $source . ")" . "\r\n\r\n";
        // file_put_contents("../data/cont.html",$body);
        $replaceElement = new replaceElement();

        $body = $replaceElement->doReplace($body);
        $content = $title . $source . $body;
        return $content;
    }
/*    public static function reCode($html) {
        $doc = phpQuery::newDocumentHTML($html);
        $ch = pq($doc)->find("pre");
        foreach ($ch as $va) {
            $te = pq($va)->text();
            $ht = pq($va)->html();
            $html = str_replace($ht, $te, $html);
        }
        return $html;
    }

    private static function replaceHrefSeg($html) {
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
    }*/
    private static function replaceImgSeg($html) {
        $doc = phpQuery::newDocumentHTML($html);
        $ch = pq($doc)->find("img");
        $i = 0;
        $src = '';
        foreach ($ch as $ke => $va) {
            $te = pq($va)->attr("data-src");
            if(strpos($te, "?src=http")){ // 处理来自其他网站的图片
                $te = explode('&', explode("?src=", $te)[1])[0];
            }else{
                $te = "https://segmentfault.com" . explode("?", $te)[0];
            }
            $ht = $doc["img:eq($ke)"];
            $src .= "\n[$i]: $te";
            $html = str_replace($ht, "\r\n\r\n![][$i]", $html);
            $i++;
        }
        $html = $html . $src;
        return $html;
    }
}