<?php 
namespace Tools\lib;

// header("Content-type:text/html; Charset=utf-8");
class Cnblogs{
    public static function getCnblogs($html) {
        $config = self::getConfig();
        $rules = $config['cnblogs']; // 从config 根据 url 获取

        $data = QueryList::html($html)->rules($rules)->query()->getData();
        $ret = $data->all();

        $title = $ret[0]['title'];
        $source = $ret[0]['source'];
        $time = $ret[0]['time'];
        $body = $ret[0]['body'];

        // 代码部分 view code 需要单独处理
        // $body = self::replaceImgTui($body);
        // $body = self::replaceHrefTui($body);

        $title = "## " . $title . "\r\n\r\n";
        $time = $time . "\r\n\r\n";
        $source = "来源：[" . $source . "](" . $source . ")" . "\r\n\r\n";
        // file_put_contents("../data/cont.html",$body);
        $replaceElement = new replaceElement();

        $body = $replaceElement->doReplace($body);
        $content = $title . $source . $time . $body;
        return $content;
    }
}