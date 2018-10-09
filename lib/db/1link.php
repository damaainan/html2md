<?php 

namespace Tools\DBUtil;

use Tools\DBUtil\SQLiteDB;
// use Tools\DBUtil\DBUtil;

class Link {
    public static $table = 'link';
    public static function getAll($name = '*') {
        // $medoo = new MedooDB();
        // $database = $medoo::$database;
        // $rest = $database->select(self::$table, ["id"]);

        $rest = SQLiteDB::findAlls(self::$table);
        // var_dump($rest);
        return $rest;
    }

    /**
     * [allTurns description]
     * @param  [type] $select ['turn'] 会返回 [['turn']=>1,['turn']=>1,['turn']=>1,....]
     *                        'turn'   会返回 [1,2,3,4...]  决定返回 一维数组 还是 二维数组
     * @return [type]         [description]
     */
    public static function allTurns($select, $where = []) {
        $rest = SQLiteDB::findAlls(self::$table, $select, $where);
        // var_dump($rest);
        return $rest;
    }

    public static function addLinks($data) {
        $rest = SQLiteDB::adds(self::$table, $data);
        return $rest;
    }
    public static function addLink($data) {
        $rest = SQLiteDB::addOne(self::$table, $data);
        return $rest;
    }

    public static function alterLink($id, $data) {
        $rest = SQLiteDB::alter(self::$table, ['id' => $id], $data);
        return $rest;
    }

}