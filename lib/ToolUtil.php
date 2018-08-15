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
    // 在每个 table 第一行后 加 |-|-|-| 
    public static function dealTable($html){
        $doc = phpQuery::newDocumentHTML($html);
        $tables = pq($doc)->find("table");
        foreach ($tables as $ke => $table) {
            // 第一个 tr 后加一行  th 或 td 的数量
            // $ht = pq($table)->find("tr:eq(0)");
            $ht = $doc["table:eq($ke) tr:eq(0)"];

            $te = pq($table)->find("tr:eq(0)")->find("td");
            if(!$te){
                $te = pq($table)->find("tr:eq(0)")->find("th");
            }
            if(!$te){
                continue;
            }
            $count = count($te);
            $tt = str_pad('', $count * 10, "<td>-</td>");
            $tstr = $ht . "\r\n<tr>" . $tt . "</tr>";
            echo $ht,"\r\n";
            echo $count,"\r\n";
            echo $tstr,"\r\n";
            // echo $tt,"\r\n";
            
            $html = str_replace($ht, $tstr, $html);
        }
        return $html;
    }
    // 去除表格部分多余的空行
    public static function removeTableSpaces($html){
        $doc = phpQuery::newDocumentHTML($html);
        $tables = pq($doc)->find("table");
        foreach ($tables as $ke => $table) {
            $tastr = $doc["table:eq($ke)"]; 
            // 需要取出表格部分多余的空行
            $retastr = preg_replace("/([\r\n]){1,}/", "\r\n", $tastr);
            $html = str_replace($tastr, $retastr, $html);
        }
        return $html;
    }

    // 去除多余的空行 
    public static function removeSpaces($html){
        # $html = preg_replace("/[(\r\n)|(\s+\r\n)]{2,}/i", "\r\n\r\n", $html);
        $html = preg_replace("/([\r\n]){2,}/", "\r\n\r\n", $html); // \r\n 的问题？ (\r\n) 不行 ([\r\n]) 可以
        return $html;
    }
}