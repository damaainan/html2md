<?php 
header("Content-type:text/html; Charset=utf-8");
class Segmentfault{

    public static function getSegmentfault($html) {
        $config = self::getConfig();
        $rules = $config['segmentfault']; // 从config 根据 url 获取

        $data = QueryList::html($html)->rules($rules)->query()->getData();
        $ret = $data->all();

        $title = $ret[0]['title'];
        $source = $ret[0]['source'];
        // $time = $ret[0]['time'];
        $body = $ret[0]['body'];
        // var_dump($body);

        // pre 中的 code 需要 去除  pre code .html replacewith .text
        $body = self::reCode($body);
        $body = self::replaceImgSeg($body);
        $body = self::replaceHrefSeg($body);

        $title = "## " . $title . "\r\n\r\n";
        // $time= $time."\r\n\r\n";
        $source = "来源：[https://segmentfault.com" . $source . "](https://segmentfault.com" . $source . ")" . "\r\n\r\n";
        // file_put_contents("../data/cont.html",$body);
        $replaceElement = new replaceElement();

        $body = $replaceElement->doReplace($body);
        $content = $title . $source . $body;
        return $content;
    }

    private static function replaceHrefSeg($html) {
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
    public static function replaceImgSeg($html) {
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