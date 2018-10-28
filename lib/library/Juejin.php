<?php
namespace Tools\lib;
use phpQuery;
use QL\QueryList;
use Tools\replaceElement;
use Tools\ToolUtil;

// header("Content-type:text/html; Charset=utf-8");
class Juejin {

    public static function getJuejin($html, $rules, $url) {
        $data = QueryList::html($html)->rules($rules)->query()->getData();
        $ret = $data->all();

        $title = $ret[0]['title'];
        $time = $ret[0]['time'];
        $body = $ret[0]['body'];

        // pre 中的 code 需要 去除  pre code .html replacewith .text
        $body = ToolUtil::reCode($body);
        $body = ToolUtil::replaceHref($body);
        $body = self::replaceImg($body);
        $body = ToolUtil::dealTable($body);

        $title = "## " . $title . "\r\n\r\n";
        $time= "时间：".$time."\r\n\r\n";

        $source = "来源：<" . $url . ">";
        $replaceElement = new replaceElement();

        $body = $replaceElement->doReplace($body);

        $body = ToolUtil::removeSpaces($body);
        
        $content = $title . $time . $source . $body;
        return $content;
    }
    private static function replaceImg($html){
        $doc = phpQuery::newDocumentHTML($html);
        $ch = pq($doc)->find("img");
        $i = 0;
        $src = '';
        foreach ($ch as $ke => $va) {
            $te = pq($va)->attr("data-src");
            $ht = $doc["img:eq($ke)"];
            $src .= "\n[$i]: $te";
            $html = str_replace($ht, "\r\n![][$i]\r\n", $html);
            $i++;
        }
        $html = $html . $src;
        return $html;
    }

}