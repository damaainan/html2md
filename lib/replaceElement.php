<?php
namespace Tools;

// header("Content-type:text/html; Charset=utf-8"); // 不能有 header 头， composer 会报错 not found 
// 待解决

/**
 * 替换 html 元素为 md 标识
 */
class replaceElement {

    public function doReplace($str) {
        $str = preg_replace('/\s{0,3}<pre[\sa-zA-Z\'\"=_:-]{0,}>/', "\r\n```LANG\r\n", $str);
        // 这个替换放在最前面就可以 在最后就失败 有一个干扰项
        // 可以加个标记在前部  再次编辑的时候方便改动

        $str = preg_replace('/<\/pre>/', "\r\n```\r\n", $str);

        $str = preg_replace('/<br[\/]{0,1}>/', "\r\n", $str);

        $str = preg_replace('/<div[\sa-zA-Z\'\"=_:-]{0,}>/', '', $str);
        $str = preg_replace('/<\/div>/', "\r\n", $str);

        $str = preg_replace('/<strong[\sa-zA-Z\'\"=_:-]{0,}>/', ' **`', $str);
        $str = preg_replace('/<\/strong>/', "`** ", $str);

        $str = preg_replace('/<em[\sa-zA-Z\'\"=_:-]{0,}>/', ' **', $str);
        $str = preg_replace('/<\/em>/', "** ", $str);

        $str = preg_replace('/<span[\sa-zA-Z\'\"=_:-]{0,}>/', '', $str);
        $str = preg_replace('/<\/span>/', "\r\n", $str);

        $str = preg_replace('/\s{0,1}<p[\sa-zA-Z\'\"=_:-]{0,}>\s{0,2}/', '', $str);
        $str = preg_replace('/<\/p>/', "\r\n", $str);

        $str = preg_replace('/\s{0,2}<h1[\sa-zA-Z\'\"=_:-]{0,}>/', "\r\n# ", $str);
        $str = preg_replace('/<\/h1>/', "\r\n", $str);
        $str = preg_replace('/\s{0,3}<h2[\sa-zA-Z\'\"=_:-]{0,}>/', "\r\n## ", $str);
        $str = preg_replace('/<\/h2>/', "\r\n", $str);
        $str = preg_replace('/\s{0,2}<h3[\sa-zA-Z\'\"=_:-]{0,}>/', "\r\n### ", $str);
        $str = preg_replace('/<\/h3>/', "\r\n", $str);
        $str = preg_replace('/\s{0,2}<h4[\sa-zA-Z\'\"=_:-]{0,}>/', "\r\n#### ", $str);
        $str = preg_replace('/<\/h4>/', "\r\n", $str);
        $str = preg_replace('/\s{0,2}<h5[\sa-zA-Z\'\"=_:-]{0,}>/', "\r\n##### ", $str);
        $str = preg_replace('/<\/h5>/', "\r\n", $str);
        $str = preg_replace('/\s{0,2}<h6[\sa-zA-Z\'\"=_:-]{0,}>/', "\r\n###### ", $str);
        $str = preg_replace('/<\/h6>/', "\r\n", $str);

        $str = preg_replace('/<code[\sa-zA-Z\'\"=_:-]{0,}>/', '`', $str);
        $str = preg_replace('/<\/code>/', "`", $str);

        $str = preg_replace('/<ol[\sa-zA-Z\'\"=_:-]{0,}>/', "\r\n", $str);
        $str = preg_replace('/<\/ol>/', "", $str);

        $str = preg_replace('/<ul[\sa-zA-Z\'\"=_:-]{0,}>/', "\r\n", $str);
        $str = preg_replace('/<\/ul>/', "", $str);

        $str = preg_replace('/\s{0,2}<li[\sa-zA-Z\'\"=_:-]{0,}>/', '* ', $str);
        $str = preg_replace('/<\/li>/', "", $str);

        $str = preg_replace('/&lt;/', "<", $str);
        $str = preg_replace('/&gt;/', ">", $str);

        $str = preg_replace('/<table[\sa-zA-Z\'\"=_:%-]{0,}>/', "\r\n", $str);
        $str = preg_replace('/<\/table>/', "\r\n", $str);

        $str = preg_replace('/\s{0,}<thead[\sa-zA-Z\'\"=_:%-]{0,}>/', "\r\n", $str);
        $str = preg_replace('/\s{0,}<\/thead>/', "\r\n", $str);

        $str = preg_replace("/[ ]{0,}<tr[\d\sa-zA-Z\'\"=_:%-]{0,}>[\s\r\n]{0,}<t[dh][\d\sa-zA-Z\'\"=_:%-]{0,}>/", "| ", $str);
        $str = preg_replace("/[ ]{0,}<t[dh][\d\sa-zA-Z\'\"=_:%-]{0,}>[\s\r\n]{0,}<\/tr>/", " | ", $str);
        $str = preg_replace("/[ ]{0,}<\/t[dh]>[\s\r\n]{0,}<t[dh][\d\sa-zA-Z\'\"=_:%-]{0,}>/", " | ", $str);
        $str = preg_replace("/[ ]{0,}<\/t[dh]>[\s\r\n]{0,}<\/tr>/", " |", $str);

        // $str = preg_replace('/\s{0,}<th[\sa-zA-Z\'\"=_:%-]{0,}>/', "\r\n", $str);
        // $str = preg_replace('/\s{0,}<\/th>/', "\r\n", $str);

        $str = preg_replace('/\s{0,}<tbody[\sa-zA-Z\'\"=_:%-]{0,}>/', "", $str);
        $str = preg_replace('/\s{0,}<\/tbody>/', "", $str);

        return $str;
    }
}
