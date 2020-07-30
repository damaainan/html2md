<?php
namespace Tools\lib;

use phpQuery;
use QL\QueryList;
use Tools\replaceElement;
use Tools\ToolUtil;

// header("Content-type:text/html; Charset=utf-8");
class Mysql
{

    public static function getMysql($html, $rules, $url)
    {
        $data = QueryList::html($html)->rules($rules)->query()->getData();
        $ret  = $data->all();

        $title = $ret[0]['title'];
        $body  = $ret[0]['body'];

        // pre 中的 code 需要 去除  pre code .html replacewith .text
        $body = self::reCode($body);
        $body = ToolUtil::replaceHref($body);
        $body = self::replaceImg($body);
        $body = ToolUtil::dealTable($body);

        $title = "## " . $title . "\r\n\r\n";

        $replaceElement = new replaceElement();

        $body = $replaceElement->doReplace($body);

        $body = ToolUtil::removeSpaces($body);

        $content = $title . $body;
        return $content;
    }
    private static function replaceImg($html)
    {
        $doc = phpQuery::newDocumentHTML($html);
        $ch  = pq($doc)->find("img");
        $i   = 0;
        $src = '';
        foreach ($ch as $ke => $va) {
            $te = pq($va)->attr("src");
            $ht = $doc["img:eq($ke)"];
            if(strpos($te, "http") === false){
                $src .= "\n[$i]: " . "http://mysql.taobao.org" . "$te";
            }else{
                $src .= "\n[$i]: " . "$te";
            }
            $html = str_replace($ht, "\r\n![][$i]\r\n", $html);
            $i++;
        }
        $html = $html . $src;
        return $html;
    }
    private static function reCode($html)
    {
        $doc = phpQuery::newDocumentHTML($html);
        $ch = pq($doc)->find("pre");
        foreach ($ch as $ke => $va) {
            // $ht = pq($va);
            // $ht = $doc["pre:eq($ke)"];

            // $langstr = substr($ht, 0, 32);
            // echo $langstr;
            // $lang="LANG";
            // if(strpos($langstr, 'cpp') !== false){
            //     $lang="cpp";
            // }else if(strpos($langstr, 'bash') !== false){
            //     $lang="bash";
            // }
            // <pre><code class="hljs objectivec">
            // if(!$lang){
                // $lang="LANG";
            // }
            $te = pq($va)->text();
            // $ht = pq($va)->html();
            // $te = str_replace("复制代码", '', $te);
            $ht = $doc["pre:eq($ke)"];
            // $ht = trim($ht); // html 代码 两侧有换行符
            $html = str_replace($ht, "\r\n\r\n```".$lang."\r\n".$te."\r\n```\r\n", $html);
        }
        return $html;
    }
}
