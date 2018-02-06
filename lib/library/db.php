<?php 
/**
 * sqlite 读取类 存储已经抓取过的地址 避免重复
 */

class DNHandler{

    private static $db;  
    function __construct(){  
        try {  
            $this->open(dirname(__FILE__).'/../data/sqlite.db');  
        }catch (Exception $e){  
            die($e->getMessage());  
        }  
    }  
      
    private static function instance(){  
        if (!self::$db) {  
            self::$db = new DNHandler();  
        }         
    }  
  
    /** 
     * 创建表 
     * @param string $sql 
     */  
    public static function create($sql){  
        self::instance();  
        $result = @self::$db->query($sql);  
        if ($result) {  
            return true;  
        }  
        return false;  
    }  
  
    /** 
     * 执行增删改操作 
     * @param string $sql 
     */  
    public static function execute($sql){  
        self::instance();  
        $result = @self::$db->exec($sql);  
        if ($result) {  
            return true;  
        }  
        return false;  
    }  
  
    /** 
     * 获取记录条数 
     * @param string $sql 
     * @return int 
     */  
    public static function count($sql){  
        self::instance();  
        $result = @self::$db->querySingle($sql);  
        return $result ? $result : 0;  
    }  
  
    /** 
     * 查询单个字段 
     * @param string $sql 
     * @return void|string 
     */  
    public static function querySingle($sql){  
        self::instance();  
        $result = @self::$db->querySingle($sql);  
        return $result ? $result : '';  
    }  
  
    /** 
     * 查询单条记录 
     * @param string $sql 
     * @return array 
     */  
    public static function queryRow($sql){  
        self::instance();  
        $result = @self::$db->querySingle($sql,true);  
        return $result;  
    }  
  
    /** 
     * 查询多条记录 
     * @param string $sql 
     * @return array 
     */  
    public static function queryList($sql){  
        self::instance();  
        $result = array();  
        $ret = @self::$db->query($sql);  
        if (!$ret) {  
            return $result;  
        }  
        while($row = $ret->fetchArray(SQLITE3_ASSOC) ){  
            array_push($result, $row);  
        }  
        return $result;       
    }  
}  

