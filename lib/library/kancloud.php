<?php
namespace Tools\lib;
//use phpQuery;
use QL\QueryList;
//use Tools\replaceElement;

// header("Content-type:text/html; Charset=utf-8");
// 不同于其他类  抓取的是整本书的内容
class Kancloud {
    // 生成 toc 
    public static function getToc($url){
        $html = file_get_contents($url);

        $arr = explode('/', $url);
        $dirname = $arr[count($arr)-2];
        $suf = $arr[count($arr)-1];
        $pre = str_replace($suf, '', $url);
        // echo $html;
        $rules = array(
            'name' => array("#main .seo .catalog ul li", "text"),
            "link" => array("#main .seo .catalog ul li a","href")
        );
        $data = QueryList::html($html)->rules($rules)->query()->getData();
        $ret = $data->all();
        $str = '';
        $href = [];
        foreach ($ret as $va) {
            $name = $va['name'];
            $href[] = $name.'*****'.$link = $pre . $va['link'];
            $str .= "[" . $name ."](".$link.")\r\n";
        }
        // 返回全对象
        $data['str'] = $str;
        $data['href'] = $href;
        $data['dir'] = $dirname;
        return $data;
    }
    // 获取内容 直接传参 文件名
    public static function getContent($href){
        $html = file_get_contents($href); // 页面内容获取有问题
        // var_dump($href);
        // echo $html;
        $rules = array(
            "body" => array(".content","text")
        );
        $data = QueryList::html($html)->rules($rules)->query()->getData();
        $ret = $data->all();
        $body = $ret[0]['body'];
        $body = str_replace("&lt;", '<', $body);
        $body = str_replace("&gt;", '>', $body);
        return $body;
    }
}