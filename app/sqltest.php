<?php 

require "../vendor/autoload.php";

use Tools\DBUtil\Link;

$ret = Link::getItemByName('');
var_dump($ret);