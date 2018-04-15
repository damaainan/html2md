<?php 

namespace Tools\DBUtil;

use Tools\DBUtil\SQLite;

class Link{
	private $table_name = "link";
	private $primary_key = "id";
	public static function getItemByName($link){
		$sql = " SELECT * from link WHERE link LIKE '%$link%' ";
		$ret = SQLite::queryRow($sql);
		return $ret;
	}
}