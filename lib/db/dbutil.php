<?php 
namespace Tools\DBUtil;

  
class DBUtil{
	public static function getParams($data){
		foreach ($data as $key => $value) {
			$params .= $value;
		}
		return $params;
	}
}