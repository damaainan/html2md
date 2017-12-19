<?php
header("Content-type:text/html; Charset=utf-8");
require '../phpQuery/phpQuery.php';

$html = file_get_contents("../data/cont.html");

// 获取所有节点元素的类型 

$res = getNodes($html);

$arr = getStr($res);
$arr = array_flip($arr);
$allEle = array_flip($arr);
var_dump($allEle);
// var_dump($res);


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
	$arr =[];
    foreach ($res as $kk => $vv) {
        $nodeLink = $nodestr;
        $ret = checkArray($vv);
        if ($ret) {
            // echo "$kk= =";
            if (is_int($kk)) {
                // $nodeLink .= "eq(" . $kk . ")->";
            } else {
            	$arr[]=$kk;
            	// echo $kk,"<br/>";
                // $nodeLink .= "children('" . $kk . "')->";
                // $nodeLink .= "children()->";
            }
            $arr1 = getStr($vv, $nodeLink);
            $arr =array_merge($arr,$arr1);
        } else {
        	// echo $vv,"<br/>";
        	$arr[]=$vv;
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
