<?php 
namespace Tools\lib;
use phpQuery;
use QL\QueryList;
use Tools\replaceElement;
class Zhihu{
    public static function getZhihu($html, $rules, $url) {
        
        $data = QueryList::html($html)->rules($rules)->query()->getData();
        $ret = $data->all();

        $title = $ret[0]['title'];
        // $source = $ret[0]['source'];
        $time = $ret[0]['time'];
        $body = $ret[0]['body'];

        $body =  self::reCode($body);
        $body =  self::replaceOther($body);
        $body = self::replaceHref($body);
        $body = self::replaceImg($body);

        $title = "## " . $title . "\r\n\r\n";
        $time = "时间：" . $time . "\r\n\r\n";
        $source = "来源：[$url]($url)" . "\r\n\r\n";
        $replaceElement = new replaceElement();

        $body = $replaceElement->doReplace($body);
        $body = preg_replace("/[\r\n]{2,}/", "\n\n", $body); // 替换多余的换行
        $content = $title . $source . $time . $body;
        return $content;

    }
    public static function reCode($html) {
        $doc = phpQuery::newDocumentHTML($html);
        $ch = pq($doc)->find("pre");
        foreach ($ch as $va) {
            $te = pq($va)->text();
            $ht = pq($va)->html();
            $html = str_replace($ht, $te, $html);
        }
        return $html;
    }

    private static function replaceOther($str){
        $str = preg_replace('/<noscript>.*?<\/noscript>/', '', $str); // ? 避免贪婪模式 不加 ？ 会多匹配
        $str = preg_replace('/<figcaption>.*?<\/figcaption>/', '', $str); 
        $str = str_replace('<figure>', '', $str); 
        $str = str_replace('</figure>', '', $str); 
        $str = str_replace('leqslant', 'leq', $str); 
        $str = str_replace('geqslant', 'geq', $str); 
        return $str;

    }

    // <figure><noscript>  需要处理    Latex 公式需要处理 

    public static function replaceImg($html) {
        $doc = phpQuery::newDocumentHTML($html);
        $ch = pq($doc)->find("img");
        $i = 0;
        $src = '';
        foreach ($ch as $ke => $va) {
            $te = pq($va)->attr("data-actualsrc");
            if(!$te){
                $te = pq($va)->attr("data-original");
            }
            if(!$te){
                $te = pq($va)->attr("src");
            }
            $ht = $doc["img:eq($ke)"];
            if(strpos($te, 'equation?tex=')){
                $tex = pq($va)->attr("alt");
                $tex = " \\\\" . '( ' . $tex . " \\\\" . ') ';
                $html = str_replace($ht, $tex, $html);
            }else{
                $src .= "\n[$i]: $te";
                $html = str_replace($ht, "\r\n\r\n![][$i]\r\n", $html);
                $i++;
            }
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