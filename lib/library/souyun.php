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
/*    private static function replaceHref($html) {
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
    }*/
    private static function dealMathjax($html) {
        $doc = phpQuery::newDocumentHTML($html);
        $dh = pq($doc)->find(".MathJax_Display");
        foreach ($dh as $key => $val) {
            $no = pq($doc)->find(".MathJax_Display:eq($key)")->html();
            $te = pq($val)->next("script")->text();
            $html = str_replace($no, "\n<nnnn>===" . $te . "===</nnnn>", $html);
        }
        // 重新解析
        $doc1 = phpQuery::newDocumentHTML($html);
        $ch = pq($doc1)->find(".MathJax_Preview");
        foreach ($ch as $ke => $va) {
            $no = pq($doc1)->find("nobr:eq($ke)")->html();

            $tes = pq($va)->next(".MathJax");
            $te = pq($tes)->next("script")->text();

            $html = str_replace($no, "===" . $te . "===", $html);
        }
        $html = str_replace("nnnn", "nobr", $html); // nnnn 避免冲突
        return $html;
    }
    // 去除 script 标签  nobr
    // 需要区分行内和行间公式
    private static function replaceMathjax($html) {
        $str = preg_replace('/<script[\sa-zA-Z\'\"=_:;\/\d-]{0,}>.*?<\/script>/', "", $html);
        // 去除 nobr
        preg_match_all("/\n<nobr>===(.*?)===<\/nobr>/", $str, $match); 
        // var_dump($match);
        foreach ($match[0] as $ke => $va) {
            $str = str_replace($match[0][$ke], "\r\n $$ " . $match[1][$ke] . " $$ ", $str);
        }
        $str = preg_replace('/<nobr>===/', " \\\\" . '\( ', $str);
        $str = preg_replace('/===<\/nobr>/', " \\\\" . '\) ', $str);

        return $str;
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
    /*public static function dealImg($html) {
        $doc = phpQuery::newDocumentHTML($html);
        $ch = pq($doc)->find("img");
        foreach ($ch as $ke => $va) {
            $te = pq($va)->attr("src");
            $ht = pq($va)->parent('a')->attr('href');
            if ($ht == $te) {
                $img = pq($va)->parent('a')->html();
                $href = $doc["img:eq($ke)"]->parent('a')->parent()->html();
                // var_dump($img);
                // var_dump($href);
                $html = str_replace($href, $img, $html);
            } else {
                continue;
            }
        }
        return $html;
    }*/

    public static function replaceImg($html) {
        $doc = phpQuery::newDocumentHTML($html);
        $ch = pq($doc)->find("img");
        $i = 0;
        $src = '';
        foreach ($ch as $ke => $va) {
            $te = pq($va)->attr("src");
            $ht = $doc["img:eq($ke)"];
            $src .= "\n[$i]: $te";
            // $html = str_replace($ht, "![]($te)", $html);
            $html = str_replace($ht, "\r\n\r\n![][$i]", $html);
            $i++;
        }
        $html = $html . $src;
        return $html;
    }

    // 处理table 内部包含的其他 换行元素
    private static function dealTable($html){
        $doc = phpQuery::newDocumentHTML($html);
        $ch = pq($doc)->find("td");
        foreach ($ch as $va) {
            // $te = pq($va)->text();
            // echo $te;
            $ht = pq($va)->html(); // 去除ht 中的多余元素

            $te = preg_replace("/[\r|\n]{0,}<span[\sa-zA-Z\'\"=_:;#\d-]{0,}>[\r|\n]{0,}/", '', $ht);
            $te = preg_replace("/[\r|\n]{0,}<\/span>[\r|\n]{0,}/", "", $te);
            // echo $te,"\n";
            $te = preg_replace("/[\r|\n]{0,}[ ]{0,}<p[\sa-zA-Z\'\"=_:-]{0,}>\s{0,2}[\r|\n]{0,}/", '', $te);
            $te = preg_replace("/[\r|\n]{0,}<\/p>[\r|\n]{0,}/", "", $te);
            // echo $te,"\n";

            $ht = trim($ht); // html 代码 两侧有换行符
            $html = str_replace($ht, $te, $html);
        }
        return $html;
    }
}