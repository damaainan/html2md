<?php
// 知乎文件批量改名  有 () 的会报错
$arr = glob("zhihu*.md");
foreach ($arr as $val) {
    $handler = fopen($val, 'r');
    $name = fgets($handler);
    $name = explode("## ", $name)[1];
    $name = trim($name);
    // echo $name;
    fclose($handler);
    rename("./" . $val, "./" . $name . ".md");
}