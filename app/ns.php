<?php 
require '../vendor/autoload.php';
// use \Tools\replaceElement;

// $re = new replaceElement();
// var_dump($re);

$ss = new Tools\lib\Tuicool();
var_dump($ss);
// 文件名必须和类名对应 大小写不敏感
// tuicool.php 可以
// tucool.class.php 报错 

/*

最前 \ 不带也可以

两种使用方式

use \Tools\replaceElement;
$re = new replaceElement();


或者 

直接

$re = new \Tools\replaceElement();
var_dump($re);

composer.json 格式

"命名空间\\":"文件夹/"

    "type": "project",
    "autoload": {  
        "psr-4": {  
            "Tools\\": "lib/"
        }  
    },

 */