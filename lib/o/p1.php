<?php
header("Content-type:text/html; Charset=utf-8");
require "../vendor/autoload.php";
require '../phpQuery/phpQuery.php';
require "../lib/replaceElement.calss.php";
use QL\QueryList;
// $html = file_get_contents("../data/cont.html");
$html = file_get_contents("../data/in.html");

$rules = array(
    // "title" => array(".article_row_fluid h1", 'text'),
    // "source" => array(".article_meta .source a",'text'),
    // "time" => array(".article_meta .timestamp",'text'),
    "body" => array("#nei", 'html'),
);
// var_dump($html);
$data = QueryList::html($html)->rules($rules)->query()->getData();
$ret = $data->all();
var_dump($ret);

// 获取所有节点元素的类型

// $res = getNodes($html);

// $arr = getStr($res);
// $arr = array_flip($arr);
// $allEle = array_flip($arr);
// var_dump($allEle);
// var_dump($res);

// reCode($html);
function reCode($html) {
    // clean pre code
    $doc = phpQuery::newDocumentHTML($html);
    $ch = pq($doc)->find("pre");
    // var_dump($ch);

    // $ele = $ch->elements;
    foreach ($ch as $va) {
        $te = pq($va)->text();
        // pq($va)->html($te);
        $ht = pq($va)->html();
        $html = str_replace($ht, $te, $html);
    }
    var_dump($html);
    // return $arr;
}
// replaceImgSeg($html);
function replaceImgSeg($html) {
    $doc = phpQuery::newDocumentHTML($html);
    $ch = pq($doc)->find("img");
    // var_dump($ch);

    // $ele = $ch->elements;
    foreach ($ch as $ke => $va) {
        // var_dump($va);
        $te = pq($va)->attr("data-src");
        // var_dump($te);
        // pq($va)->html($te);
        $ht = $doc["img:eq($ke)"];
        // var_dump($ht);
        // $ht=pq($va)->replaceWith();
        $html = str_replace($ht, "![]($te)", $html);
    }
    var_dump($html);
}
// replaceHrefSeg($html);
function replaceHrefSeg($html) {
    $doc = phpQuery::newDocumentHTML($html);
    $ch = pq($doc)->find("a");
    // var_dump($ch);

    // $ele = $ch->elements;
    foreach ($ch as $ke => $va) {
        // var_dump($va);
        $href = pq($va)->attr("href");
        $te = pq($va)->text();
        $ht = $doc["a:eq($ke)"];
        // var_dump($te);
        // pq($va)->html($te);
        // $ht=pq($va)->prop("outerHTML");
        // var_dump($ht);
        // $ht=pq($va)->replaceWith();
        $html = str_replace($ht, "[$te]($href)", $html);
    }
    var_dump($html);
}

function getNodes($html) {
    $doc = phpQuery::newDocumentHTML($html);
    $ch = pq($doc)->children();

    $ele = $ch->elements;
    foreach ($ele as $k => $va) {
        $tag = $va->tagName;
        // 需要检查是否有子元素
        $gg = pq($doc)->children()->eq($k)->html();
        $ret = checkNode($gg);
        if ($ret) {
            $arr2 = getNodes($gg);
            $arr[$k][$tag] = $arr2;
        } else {
            $arr[$k] = $tag;
        }
    }
    return $arr;
}
function checkNode($html) {
    $doc = phpQuery::newDocumentHTML($html);
    $ch = pq($doc)->children();
    $ele = $ch->elements;
    if (count($ele) == 0) {
        return false;
    } else {
        return true;
    }
}

function getStr($res, $nodestr = '') {
    $arr = [];
    foreach ($res as $kk => $vv) {
        $nodeLink = $nodestr;
        $ret = checkArray($vv);
        if ($ret) {
            // echo "$kk= =";
            if (is_int($kk)) {
                // $nodeLink .= "eq(" . $kk . ")->";
            } else {
                $arr[] = $kk;
                // echo $kk,"<br/>";
                // $nodeLink .= "children('" . $kk . "')->";
                // $nodeLink .= "children()->";
            }
            $arr1 = getStr($vv, $nodeLink);
            $arr = array_merge($arr, $arr1);
        } else {
            // echo $vv,"<br/>";
            $arr[] = $vv;
            // echo $nodeLink;
            // echo "eq(" . $kk . ")->children('" . $vv . "');<br/>";
        }
    }
    return $arr;
}

function checkArray($arr) {
    if (is_array($arr)) {
        return 1;
    } else {
        return 0;
    }
}

// $replaceElement = new replaceElement();

// $html    = $replaceElement->doReplace($html);
// var_dump($html);
