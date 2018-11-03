<?php
namespace Tools\lib;

use phpQuery;
use QL\QueryList;
use Tools\replaceElement;
use Tools\ToolUtil;

// header("Content-type:text/html; Charset=utf-8");
class Cto
{

    public static function getCto($html, $rules, $url)
    {
        $data = QueryList::html($html)->rules($rules)->query()->getData();
        $ret  = $data->all();

        $title = $ret[0]['title'];
        // $source = $ret[0]['source'];
        $time = $ret[0]['time'];
        $body = $ret[0]['body'];
        // var_dump($body);

        // pre 中的 code 需要 去除  pre code .html replacewith .text
        // $body = self::reCode($body);
        $body = ToolUtil::replaceHref($body);
        $body = ToolUtil::replaceImg($body);
        $body = ToolUtil::dealTable($body);

        $title  = "## " . $title . "\r\n\r\n";
        $time   = "时间：" . $time . "\r\n\r\n";
        $source = "来源：[" . $url . "](" . $url . ")" . "\r\n\r\n";
        // file_put_contents("../data/cont.html",$body);
        $replaceElement = new replaceElement();

        $body = $replaceElement->doReplace($body);

        $body    = ToolUtil::removeSpaces($body);
        $content = $title . $time . $source . $body;
        return $content;
    }

    public static function reCode($html)
    {
        $doc = phpQuery::newDocumentHTML($html);
        $ch  = pq($doc)->find("pre");
        foreach ($ch as $va) {
            $te   = pq($va)->text();
            $ht   = pq($va)->html();
            $ht   = trim($ht); // html 代码 两侧有换行符
            $html = str_replace($ht, $te, $html);
        }
        return $html;
    }
}
