<?php
namespace Tools\lib;

// require "../../vendor/autoload.php";  // 只需要在父文件引入一次 不需要再次引入

//use phpQuery;
use QL\QueryList;
use Tools\replaceElement;
use Tools\ToolUtil;

// header("Content-type:text/html; Charset=utf-8");
class Tuicool
{
    /**
     * @param  string $html
     * @param string $rules
     * @return string $content
     */
    public static function getTuiku($html, $rules)
    {
        // var_dump($html);
        // file_put_contents("../data/in.html", $html);
        // $html = file_get_contents("../data/in.html");
        // 部分网址获取不到内容
        $data = QueryList::html($html)->rules($rules)->query()->getData();
        $ret = $data->all();

        $title = $ret[0]['title'];
        $source = $ret[0]['source'];
        $time = $ret[0]['time'];
        $body = $ret[0]['body'];

        $replaceElement = new replaceElement();
        $body = $replaceElement::dealHrefSpaces($body);
        
        $body = ToolUtil::reCode($body);
        $body = ToolUtil::replaceHref($body);
        $body = ToolUtil::replaceImg($body);
        $body = ToolUtil::dealTable($body);

        $title = "## " . $title . "\r\n\r\n";
        $time = $time . "\r\n\r\n";
        $source = "来源：[" . $source . "](" . $source . ")" . "\r\n\r\n";
        // file_put_contents("../data/cont.html",$body);

        $body = $replaceElement->doReplace($body);

        $body = ToolUtil::removeSpaces($body);

        $content = $title . $source . $time . $body;
        return $content;
    }

/*    public static function replaceImgTui($html) {
        $doc = phpQuery::newDocumentHTML($html);
        $ch = pq($doc)->find("img");
        $i = 0;
        $src = '';
        foreach ($ch as $ke => $va) {
            $te = pq($va)->attr("src");
            $ht = $doc["img:eq($ke)"];
            $src .= "\n[$i]: $te";
            $html = str_replace($ht, "\r\n![][$i]\r\n", $html);
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
    }*/
}
