<?php 
namespace Tools;

require "../vendor/autoload.php";
use phpQuery;

class ToolUtil {
    // 代码部分特殊处理 多种代码形式 正常形式的代码可以了
    public static function reCode($html) {
        $doc = phpQuery::newDocumentHTML($html);
        $ch = pq($doc)->find("pre");
        foreach ($ch as $va) {
            $te = pq($va)->text();
            $ht = pq($va)->html();
            $ht = trim($ht); // html 代码 两侧有换行符
            $html = str_replace($ht, $te, $html);
        }
        return $html;
    }
    public static function replaceImg($html) {
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
    public static function replaceHref($html) {
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
    }
}