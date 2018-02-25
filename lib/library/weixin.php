<?php 
namespace Tools\lib;
use phpQuery;
use QL\QueryList;
use Tools\replaceElement;
class Weixin{
	public static function getWeixin($html, $rules, $url) {
        
        $data = QueryList::html($html)->rules($rules)->query()->getData();
        $ret = $data->all();

        $title = $ret[0]['title'];
        // $source = $ret[0]['source'];
        $time = $ret[0]['time'];
        $body = $ret[0]['body'];

        // $body =  self::replaceOther($body);
        $body = self::replaceHref($body);
        $body = self::replaceImg($body);

        $title = "## " . $title . "\r\n\r\n";
        $time = $time . "\r\n\r\n";
        $source = "来源：$url" . "\r\n\r\n";
        $replaceElement = new replaceElement();

        $body = $replaceElement->doReplace($body);
        $body = preg_replace("/[\r\n]{2,}/", "\n\n", $body); // 替换多余的换行
        $content = $title . $source . $time . $body;
        return $content;

    }

    public static function replaceImg($html) {
        $doc = phpQuery::newDocumentHTML($html);
        $ch = pq($doc)->find("img");
        $i = 0;
        $src = '';
        foreach ($ch as $ke => $va) {
            $te = pq($va)->attr("data-original");
            $ht = $doc["img:eq($ke)"];
            $src .= "\n[$i]: $te";
            $html = str_replace($ht, "\r\n\r\n![][$i]", $html);
            $i++;
        }
        $html = $html . $src;
        return $html;
    }
    private static function replaceHref($html) {
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