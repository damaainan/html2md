<?php 

require "../vendor/autoload.php";

use Tools\DBUtil\SQLiteDB;
use Tools\DBUtil\Link;

$data = ['link'=>'http','name'=>'terst','create_time'=>'2018-04-15 12:22:22','status'=>1] ;

$ret = Link::addLink($data);
var_dump($ret);



// $ret = SQLiteDB::create("CREATE TABLE link (id INTEGER,link TEXT,name TEXT,status INTEGER,create_time text);");
// var_dump($ret);