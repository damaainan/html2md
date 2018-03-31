<?php
namespace Tools;

// header("Content-type:text/html; Charset=utf-8"); // 不能有 header 头， composer 会报错 not found 
// 待解决

/**
 * 替换 html 元素为 md 标识
 */
class replaceElement {

    public function doReplace($str) {
        // 这个替换放在最前面就可以 在最后就失败 有一个干扰项
        // 可以加个标记在前部  再次编辑的时候方便改动
        $str = preg_replace("/\n{0,}[ ]{0,10}<pre[\sa-zA-Z\'\"=_:;\d-]{0,}>/", "\r\n```LANG\r\n", $str);
        $str = preg_replace('/<\/pre>/', "\r\n```\r\n", $str);

        

        $str = preg_replace('/<div[\sa-zA-Z\'\"=_:;#\d-]{0,}>/', '', $str);
        $str = preg_replace('/<\/div>/', "\r\n", $str);

        

        $str = preg_replace('/[ ]{0,}<span[\sa-zA-Z\x{4e00}-\x{9fa5}\'\"\.\(\),=_:;#\d-]{0,}>/u', '', $str);
        $str = preg_replace("/<\/span>\n{0,}/", " ", $str);

        $str = preg_replace("/[ ]{0,}<p[\sa-zA-Z\'\"\d=_\.;:,\(\)-]{0,}>\s{0,10}[\r|\n]{0,1}/", "", $str);
        $str = preg_replace("/[\s\r\n]{0,10}<\/p>/", "\r\n", $str);

        $str = self::dealHead($str);
        // $str = preg_replace('/\s{0,2}<h1[\d\sa-zA-Z\x{4e00}-\x{9fa5}\'\"=_:-]{0,}>/u', "\r\n## ", $str);
        // $str = preg_replace('/<\/h1>/', "\r\n", $str);
        // $str = preg_replace('/\s{0,3}<h2[\d\sa-zA-Z\x{4e00}-\x{9fa5}\'\"=_:-]{0,}>/u', "\r\n## ", $str);
        // $str = preg_replace('/<\/h2>/', "\r\n", $str);
        // $str = preg_replace('/\s{0,2}<h3[\d\sa-zA-Z\x{4e00}-\x{9fa5}\'\"=_:-]{0,}>/u', "\r\n### ", $str);
        // $str = preg_replace('/<\/h3>/', "\r\n", $str);
        // $str = preg_replace('/\s{0,2}<h4[\d\sa-zA-Z\'\"=_:-]{0,}>/', "\r\n#### ", $str);
        // $str = preg_replace('/<\/h4>/', "\r\n", $str);
        // $str = preg_replace('/\s{0,2}<h5[\d\sa-zA-Z\'\"=_:-]{0,}>/', "\r\n##### ", $str);
        // $str = preg_replace('/<\/h5>/', "\r\n", $str);
        // $str = preg_replace('/\s{0,2}<h6[\d\sa-zA-Z\'\"=_:-]{0,}>/', "\r\n###### ", $str);
        // $str = preg_replace('/<\/h6>/', "\r\n", $str);

        $str = preg_replace("/\n{0,1}[ ]{0,}<code[\sa-zA-Z\'\"=_:-]{0,}>/", '`', $str);
        $str = preg_replace("/<\/code>\s{0,}\n{0,}/", "`", $str);

        $str = preg_replace("/\n{0,1}[ ]{0,}<dt[\sa-zA-Z\'\"=_:-]{0,}>/", '', $str);
        $str = preg_replace("/<\/dt>\n{0,}/", "\r\n  \r\n", $str);

        $str = preg_replace('/\s{0,}<dl[\sa-zA-Z\'\"=_:;\d-]{0,}>/', "\r\n", $str);
        $str = preg_replace('/<\/dl>/', "\r\n", $str);

        $str = preg_replace('/\s{0,}<dd[\sa-zA-Z\'\"=_:;\d-]{0,}>\s{0,}/', "\r\n", $str);
        $str = preg_replace('/\s{0,}<\/dd>/', "\r\n\r\n", $str);

        $str = self::dealOthers($str);

        $str = self::dealList($str);

        // $str = preg_replace('/\s{0,2}<ol[\sa-zA-Z\'\"=_:-]{0,}>/', "\r\n", $str);
        // $str = preg_replace('/<\/ol>/', "\r\n", $str);

        // $str = preg_replace('/\s{0,2}<ul[\d\sa-zA-Z\'\"=_:-]{0,}>/', "\r\n", $str);
        // $str = preg_replace('/<\/ul>/', "\r\n", $str);

        // $str = preg_replace('/[ ]{0,4}<li[\sa-zA-Z\'\"=_:-]{0,}>\n{0,}/', '* ', $str);
        // $str = preg_replace('/<\/li>/', "", $str);

        // 替换已转义字符
        $str = str_replace('&lt;', "<", $str);
        $str = str_replace('&gt;', ">", $str);
        $str = str_replace('&amp;', "&", $str);

        $str = self::dealTable($str);
        // $str = preg_replace('/<table[\sa-zA-Z\'\"=_:%-]{0,}>/', "\r\n", $str);
        // $str = preg_replace('/<\/table>/', "\r\n", $str);

        // $str = preg_replace('/\s{0,}<thead[\sa-zA-Z\'\"=_:%-]{0,}>/', "\r\n", $str);
        // $str = preg_replace('/\s{0,}<\/thead>/', "\r\n", $str);

        // $str = preg_replace("/[ ]{0,}<tr[\d\sa-zA-Z\'\"=_:%-]{0,}>[\s\r\n]{0,}<t[dh][\d\sa-zA-Z\'\"=_:%-]{0,}>/", "| ", $str);
        // $str = preg_replace("/[ ]{0,}<t[dh][\d\sa-zA-Z\'\"=_:%-]{0,}>[\s\r\n]{0,}<\/tr>/", " | ", $str);
        // $str = preg_replace("/[ ]{0,}<\/t[dh]>[\s\r\n]{0,}<t[dh][\d\sa-zA-Z\'\"=_:%-]{0,}>/", " | ", $str);
        // $str = preg_replace("/[ ]{0,}<\/t[dh]>[\s\r\n]{0,}<\/tr>/", " |", $str);

        // $str = preg_replace('/\s{0,}<th[\sa-zA-Z\'\"=_:%-]{0,}>/', "\r\n", $str);
        // $str = preg_replace('/\s{0,}<\/th>/', "\r\n", $str);

        // $str = preg_replace('/\s{0,}<tbody[\sa-zA-Z\'\"=_:%-]{0,}>/', "", $str);
        // $str = preg_replace('/\s{0,}<\/tbody>/', "", $str);

        return $str;
    }

    private static function dealOthers($str){
        $str = preg_replace('/<br[\/]{0,1}>/', "\r\n", $str);
        $str = preg_replace('/<hr[\/]{0,1}>/', "\r\n-----\r\n", $str);


        $str = preg_replace("/\n{0,}[ ]{0,}<strong>/", ' **`', $str);
        $str = preg_replace('/<\/strong>\n{0,}/', "`** ", $str);

        $str = preg_replace('/<b>/', ' **', $str);
        $str = preg_replace('/<\/b>/', "** ", $str);

        $str = preg_replace("/\n{0,}[ ]{0,}<em>\n{0,}/", ' ', $str);
        $str = preg_replace("/\n{0,}[ ]{0,}<\/em>\n{0,}/", " ", $str);



        $str = preg_replace("/[ ]{0,}<tt>\s{0,}\n{0,}/", "", $str);
        $str = preg_replace("/\s{0,}<\/tt>\n{0,}/", "", $str);

        $str = preg_replace("/<i>/", "`", $str);
        $str = preg_replace("/<\/i>/", "`", $str);
        $str = preg_replace("/<u>\s{0,}/", "", $str);
        $str = preg_replace("/\s{0,}<\/u>/", "", $str);

        $str = preg_replace("/<figure>\s{0,}\n{0,}/", "", $str);
        $str = preg_replace("/\s{0,}<\/figure>/", "\n", $str);


        $str = preg_replace("/<\/{0,1}blockquote>/", "", $str);
        
        $str = preg_replace("/<\/{0,1}font>\n{0,}/", "", $str);
        return $str;
    }

    // 处理表格
    private static function dealTable($str){
        $str = preg_replace('/<table[\sa-zA-Z\'\"\d=_:%-]{0,}>/', "\r\n", $str);
        $str = preg_replace('/<\/table>/', "\r\n", $str);

        $str = preg_replace('/\s{0,}<thead[\sa-zA-Z\'\"=_:%-]{0,}>/', "\r\n", $str);
        $str = preg_replace('/\s{0,}<\/thead>/', "\r\n", $str);

        $str = preg_replace("/[ ]{0,}<tr[\d\sa-zA-Z\'\"=_:%-]{0,}>[\s\r\n]{0,}<t[dh][\d\sa-zA-Z\'\"=_:%-]{0,}>[\s\r\n]{0,}/", "| ", $str);
        $str = preg_replace("/[ ]{0,}<t[dh][\d\sa-zA-Z\'\"=_:%-]{0,}>[\s\r\n]{0,}<\/tr>/", " |", $str);
        $str = preg_replace("/[\s\r\n]{0,}<\/t[dh]>[\s\r\n]{0,}<t[dh][\d\sa-zA-Z\'\"=_:%-]{0,}>[\s\r\n]{0,}/", " | ", $str);
        $str = preg_replace("/[\s\r\n]{0,}<\/t[dh]>[\s\r\n]{0,}<\/tr>/", " |", $str);

        $str = preg_replace('/\s{0,}<tbody[\sa-zA-Z\'\"=_:%-]{0,}>/', "", $str);
        $str = preg_replace('/\s{0,}<\/tbody>/', "", $str);
        return $str;
    }
    // 处理列表
    private static function dealList($str){
        $str = preg_replace('/\s{0,2}<ol[\sa-zA-Z\'\"\d=_:-]{0,}>/', "\r\n", $str);
        $str = preg_replace('/<\/ol>/', "\r\n", $str);

        $str = preg_replace('/\s{0,2}<ul[\d\sa-zA-Z\'\"=_:-]{0,}>/', "\r\n", $str);
        $str = preg_replace('/<\/ul>/', "\r\n", $str);

        $str = preg_replace('/[ ]{0,}<li[\sa-zA-Z\'\"=_:-]{0,}>\s{0,}\n{0,}/', "* ", $str);
        $str = preg_replace('/<\/li>/', "", $str);
        return $str;
    }
    // 处理标题
    private static function dealHead($str){
        $hbase_p = '/\s{0,2}<';
        $hbase_s = '[\d\sa-zA-Z\x{4e00}-\x{9fa5}\'\"\.=_;:-]{0,}>\s{0,}/u'; // 拼接 h1 - h6 
        for ($i = 1; $i < 7; $i++) {
            $head = "\n" . str_pad("", $i, "#");
            if($i==1){
                $head = $head . "#";
            }
            $h = "h".$i;
            $pattern = $hbase_p . $h .$hbase_s;
            $str = preg_replace($pattern, $head . " ", $str);
            $str = preg_replace('/<\/'. $h .'>/', "\r\n", $str);
        }
        return $str;
    }
}
