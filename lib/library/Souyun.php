<?php
namespace Tools\lib;
use phpQuery;
use QL\QueryList;
use Tools\replaceElement;

// header("Content-type:text/html; Charset=utf-8");
class Souyun {
    public static function getYun($html) {
        // $data = QueryList::html($html)->rules($rules)->query()->getData();
        // $ret = $data->all();

        // $body = $ret[0]['body'];

        $body = $html; // 暂时采用固定文件
        $body = self::getCiDes($body);
        // echo $body;
        die;
        
        $body = self::dealTable($body);
        $body = self::replaceHref($body);
        $body = self::replaceImg($body);
        $body = self::dealMathjax($body);

        $title = "## " . trim($title) . "\r\n\r\n";
        $time = "时间：" . $time . "\r\n\r\n";
        $source = "来源：[" . $source . "](" . $source . ")" . "\r\n\r\n";
        $replaceElement = new replaceElement();

        $body = $replaceElement->doReplace($body);

        $body = self::replaceMathjax($body);

        $content = $title . $source . $time . $body;
        return $content;
    }

    private static function getCiDes($html){
        $doc = phpQuery::newDocumentHTML($html);
        $ch = pq($doc)->find(".ciTuneDesc");
        $dh = pq($doc)->find(".ciTuneFormat");
        foreach ($ch as $ke=>$va) {
            // 描述
            $flag=0;
            $map =[];
            if(pq($va)->find('span')->hasClass('ciTuneName')){
                $map['title'] = $title = pq($va)->find('.ciTuneName')->html();
                $flag++;
            }
            if(pq($va)->find('span')->hasClass('comment')){
                $map['comment'] = $comment = pq($va)->find('.comment')->html();
                $flag++;
            }
            if($flag==0){
                $map['desc'] = $desc = pq($va)->html();
            }
            $ret1[] = $map;
        }

        foreach ($dh as $key=>$val) {
            // 描述
            $flag=0;
            $map1 =[];
            if(pq($val)->find('span')->hasClass('rightIndentLabel')){
                $map1['name'] = pq($val)->find('.rightIndentLabel')->html();
                $flag++;
            }
            if(pq($val)->find('span')->hasClass('tuneFormatDesc')){
                $map1['diao']  = pq($val)->find('.tuneFormatDesc')->html();
                $flag++;
            }
            if(pq($val)->find('span')->hasClass('indentLabel')){
                $map1['author']  = pq($val)->find('.indentLabel')->html();
                $flag++;
            }
            if(pq($val)->find('p')->hasClass('mSize')){
                $map1['cont']  = pq($val)->find('.mSize')->html();
                $flag++;
            }
            
            $ret2[] = $map1;
        }
        print_r($ret1);
        print_r($ret2);
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
            if (!$href) {
                continue;
            }
            $te = pq($va)->text();
            $ht = $doc["a:eq($ke)"];
            $src .= "\n[$i]: $href";
            // $html = str_replace($ht, "[$te]($href)", $html);
            $html = str_replace($ht, "[$te][$i]", $html);
            $i++;
        }
        $html = $html . $src;
        return $html;
    }

}