<?php
header("Content-type:text/html; Charset=utf-8");
require "../vendor/autoload.php";

use Tools\replaceElement;
use phpQuery;


$html = file_get_contents("../data/yue.html");

$replaceElement = new replaceElement();

$body = $replaceElement->doReplace($html);

file_put_contents("../out/other/yue.md", $body);




function replaceHref($html) {
    $doc = phpQuery::newDocumentHTML($html);
    $ch = pq($doc)->find(".calibre3");
    $count = count($ch);
    $i = 1;
    // $i = $count;
    $src = '';
    foreach ($ch as $ke => $va) {
        $ht = $doc[".calibre3:eq($ke)"];
        // $src .= "\n[$i]: $href";
        // $html = str_replace($ht, "[$te][$i]", $html);
        $i++;
    }
    // $html = $html . $src;
    // return $html;
}


