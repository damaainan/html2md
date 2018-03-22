<?php
namespace Tools\lib;
use phpQuery;
use QL\QueryList;
use Tools\replaceElement;

// header("Content-type:text/html; Charset=utf-8");
class Cnblogs {
    public static function getCnblogs($html, $rules) {

        $data = QueryList::html($html)->rules($rules)->query()->getData();
        $ret = $data->all();
// var_dump($html);
// var_dump($ret);
// die();
        $title = $ret[0]['title'];
        $source = $ret[0]['source'];
        $time = isset($ret[0]['time']) ? $ret[0]['time'] : '';
        $body = $ret[0]['body'];

        // 代码部分 view code 需要单独处理
        // 需要先清理代码部分
        // $body = self::dealImg($body);die();  // 图片替换没处理好
        $body = self::reCode($body);
        // echo $body;
        $body = self::replaceImg($body);
        $body = self::replaceHref($body);

        $title = "## " . $title . "\r\n\r\n";
        $time = $time . "\r\n\r\n";
        $source = "来源：[" . $source . "](" . $source . ")" . "\r\n\r\n";
        // file_put_contents("../data/cont.html",$body);
        $replaceElement = new replaceElement();

        $body = $replaceElement->doReplace($body);
        $content = $title . $source . $time . $body;
        return $content;
    }

    private static function replaceHref($html) {
        $doc = phpQuery::newDocumentHTML($html);
        $ch = pq($doc)->find("a");
        $i = 100;
        $src = '';
        foreach ($ch as $ke => $va) {
            $href = pq($va)->attr("href");
            if (!$href) {
                continue;
            }
            $te = pq($va)->text();
            $ht = $doc["a:eq($ke)"];
            $src .= "\n[$i]: $href";
            $html = str_replace($ht, "[$te][$i]", $html);
            $i++;
        }
        $html = $html . $src;
        return $html;
    }
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
    // 处理图片第一步
    public static function dealImg($html) {
        $doc = phpQuery::newDocumentHTML($html);
        $ch = pq($doc)->find("img");
        foreach ($ch as $ke => $va) {
            $te = pq($va)->attr("src");
            $ht = pq($va)->parent('a')->attr('href');
            if ($ht == $te) {
                $img = pq($va)->parent('a')->html();
                $href = $doc["img:eq($ke)"]->parent('a')->parent()->html();
                var_dump($img);
                var_dump($href);
                $html = str_replace($href, $img, $html);
            } else {
                continue;
            }
        }
        return $html;
    }
    public static function reCode1($html) {
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

            $pahtml = pq($doc)->find("img:eq($ke)")->parent("a")->html();
            $pahtmlstr = pq($doc)->find("img:eq($ke)")->parent("a")->parent()->html();
            // 获取 a 标签的 html
            $src .= "\n[$i]: $te";
            if(trim($pahtml) == trim($ht)){
                // echo "\n*****\n";
                // echo $pahtml;
                // echo "\n*****\n";
                // echo $pahtmlstr;
                // echo "\n*****\n";
                // echo $ht;
                // echo "\n*****\n";   // pahtmlstr 需要去除两边换行  str-replace 是字符串替换，多行替换可以
                $html = str_replace(trim($pahtmlstr), "\r\n![][$i]", $html);
            }else{
                $html = str_replace($ht, "\r\n![][$i]", $html);
            }
            $i++;
        }
        $html = $html . $src;
        return $html;
    }
}