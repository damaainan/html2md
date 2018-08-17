<?php
namespace Tools\lib;
use phpQuery;
use QL\QueryList;
use Tools\replaceElement;
use Tools\ToolUtil;

// header("Content-type:text/html; Charset=utf-8");
class Zcfy {

    public static function getZCFY($html, $rules, $url) {
        $data = QueryList::html($html)->rules($rules)->query()->getData();
        $ret = $data->all();

        $title = $ret[0]['title'];
        // $source = $ret[0]['source'];
        $time = $ret[0]['time'];
        $from = $ret[0]['from'];
        $body = $ret[0]['body'];
        // var_dump($body);

        // pre 中的 code 需要 去除  pre code .html replacewith .text
        $body = ToolUtil::reCode($body);
        $body = ToolUtil::replaceHref($body);
        $body = ToolUtil::replaceImg($body);

        $body = ToolUtil::dealTable($body);

        $title = "## " . $title . "\r\n\r\n";
        $time= $time."\r\n\r\n";
        $source = "来源：[" . $url . "](" . $url . ")" . "\r\n\r\n";
        $from = "原文：[" . $from . "](" . $from . ")\r\n\r\n";
        $replaceElement = new replaceElement();

        $body = $replaceElement->doReplace($body);
        $body = ToolUtil::removeSpaces($body);
        $content = $title . $source . $from . $body;
        return $content;
    }
}