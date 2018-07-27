<?php
header("Content-type:text/html; Charset=utf-8");
require "../vendor/autoload.php";

use Tools\replaceElement;
use phpQuery;


$html = file_get_contents("../data/yue.html");

$replaceElement = new replaceElement();

$body = $replaceElement->doReplace($html);

file_put_contents("../out/other/yue.md", $body);




public function replaceHref($html) {
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


