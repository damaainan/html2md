<?php
namespace Tools\lib;

use QL\QueryList;
use Tools\replaceElement;
use phpQuery;
use Tools\ToolUtil;

class Tianya
{
 // issues
    // 逻辑不一样 需要判断每个块是否是楼主所发 否则舍弃
    public static function getTianya($html, $rules, $url)
    {
        $data = QueryList::html($html)->rules($rules)->query()->getData();
        $ret = $data->all();

        $title = $ret[0]['title'];
        // $source = $ret[0]['source'];
        $time = $ret[0]['time'];
        $body = $ret[0]['body'];

        $body = ToolUtil::reCode($body);
        $body = self::replaceImg($body);
        $body = self::replaceHref($body); // 处理链接和图片的顺序

        $title = "## " . $title . "\r\n\r\n";
        $time = "时间：" . $time . "\r\n\r\n";
         $source = "来源：[" . $url . "](" . $url . ")" . "\r\n\r\n";
        // file_put_contents("../data/cont.html",$body);
        $replaceElement = new replaceElement();

        $body = $replaceElement->doReplace($body);
        $body = ToolUtil::removeSpaces($body);
        $content = $title  . $time . $source . $body;
        return $content;
    }
    // 分析body 部分每个块
    private static function ($html) {
    }
}
