<?php 
namespace Tools\lib;


use QL\QueryList;
use Tools\replaceElement;
use phpQuery;
use Tools\ToolUtil;

class Github{ // issues
	public static function getGithub($html, $rules, $url) {
		$data = QueryList::html($html)->rules($rules)->query()->getData();
        $ret = $data->all();

        $title = $ret[0]['title'];
        // $source = $ret[0]['source'];
        $time = $ret[0]['time'];
        $body = $ret[0]['body'];

        $labels = self::getLabels($html);

        $body = ToolUtil::reCode($body);
        $body = self::replaceImg($body);
        $body = self::replaceHref($body); // 处理链接和图片的顺序

        $title = "## " . $title . "\r\n\r\n";
        $time = $time . "\r\n\r\n";
         $source = "来源：[" . $url . "](" . $url . ")" . "\r\n\r\n";
        // file_put_contents("../data/cont.html",$body);
        $replaceElement = new replaceElement();

        $lstr = "Labels: " . implode(' , ', $labels) . "\r\n\r\n";

        $body = $replaceElement->doReplace($body);
        $content = $title  . $time . $source . $lstr . $body;
        return $content;
	}

    // 获取标签
    private static function getLabels($html){
        $doc = phpQuery::newDocumentHTML($html);
        $ch = pq($doc)->find(".sidebar-labels-style");
        $labels = [];
        foreach ($ch as $ke => $va) {
            $labels[] = pq($va)->attr("title");
        }
        return $labels;
    }

    private static function replaceImg($html) { // 先处理 img 标签外的 a 标签
        $doc = phpQuery::newDocumentHTML($html);
        $ch = pq($doc)->find("img");
        $dh = pq($doc)->find("a");
        $count = count($dh);
        $i=$count;
        $src='';
        foreach ($ch as $ke => $va) {
            $te = pq($va)->attr("src");
            // $ht = $doc["img:eq($ke)"];
            $pahtml = pq($doc)->find("img:eq($ke)")->parent("a")->parent("p")->html();
            $src .= "\n[$i]: $te";
            $html = str_replace($pahtml, "\r\n\r\n![][$i]", $html);
            $i++;
        }
        $html = $html.$src;
        return $html;
    }
    private static function replaceHref($html) {
        $doc = phpQuery::newDocumentHTML($html);
        $ch = pq($doc)->find("a");
        // $dh = pq($doc)->find("img");
        // $count = count($dh);
        $i=0;
        $src='';
        foreach ($ch as $ke => $va) {
            $href = pq($va)->attr("href");
            $te = pq($va)->text();
            $ht = $doc["a:eq($ke)"];
            $src .= "\n[$i]: $href";
            $html = str_replace($ht, "[$te][$i]", $html);
            $i++;
        }
        $html = $html.$src;
        return $html;
    }
}