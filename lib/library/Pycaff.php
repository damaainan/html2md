<?php
namespace Tools\lib;

use QL\QueryList;
use Tools\replaceElement;
use Tools\ToolUtil;

// header("Content-type:text/html; Charset=utf-8");
class Pycaff
{
    public static function getPycaff($html, $rules, $url)
    {
        $data = QueryList::html($html)->rules($rules)->query()->getData();
        $ret  = $data->all();

        $title   = trim($ret[0]['title']);
        $book = "> 书籍：《" . trim($ret[0]['book']) . "》  \r\n";
        $chapter    = "> 章节：【" . trim($ret[0]['chapter']) . "】\r\n\r\n";
        $body    = $ret[0]['body'];
        // pre 中的 code 需要 去除  pre code .html replacewith .text
        $body = ToolUtil::reCode($body);
        $body = ToolUtil::replaceHref($body);
        $body = ToolUtil::replaceImg($body);
        $body = ToolUtil::dealTable($body);

        $title  = "## " . $title . "\r\n\r\n";
        $source = "来源：[" . $url . "](" . $url . ")" . "\r\n\r\n";
        // file_put_contents("../data/cont.html",$body);
        $replaceElement = new replaceElement();

        $body = $replaceElement->doReplace($body);
        $body    = ToolUtil::removeSpaces($body);

        $body = str_replace('LANG', 'python', $body);

        $content = $title . $book . $chapter . $source  . $body;
        return $content;
    }
}
