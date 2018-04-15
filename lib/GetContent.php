<?php
namespace Tools;

// header("Content-type:text/html; Charset=utf-8");
require "../vendor/autoload.php";
// require '../phpQuery/phpQuery.php';
// require "replaceElement.calss.php";

// require "config.php"; // 能不能不用引入的方式？

use QL\QueryList;
use Tools\replaceElement;
use Tools\GetHtml;
use Tools\config;
use Tools\lib\Tuicool;
use Tools\lib\Segmentfault;
use Tools\lib\Cnblogs;
use Tools\lib\github;
use Tools\lib\zhihu;
use Tools\lib\csdn;
use Tools\lib\souyun;

/**
 * 获取最后内容
 */
class GetContent {
    // 配置文件要独立出来
    /*private static $config = [
    ];*/
    // public $configs = [];
    // function __construct(){ // 这种方式 报错 $this ,可能是类引用的问题
    //      require "config.php"；
    //     $this->configs = $config;
    // }

    public static function getConfig() {
        // require "config.php";  // 这样很 low 
        // var_dump($config);
        // return $config;
        $config = new Config();
        return $config->getConfig();
    }

    public static function doMark($url) {
        $config = new Config();
        // $configs = $config->getConfig();

        // var_dump($configs);die();
        $arr = explode('/', $url);
        $name = $arr[count($arr) - 1];
        // $html = file_get_contents($url); // 可以优化为专门的 curl 方法
        $html = GetHtml::getUrl($url); // 可以优化为专门的 curl 方法
        // $configs = $this->configs;

        // array_search 
        // 判断 url 选择方法
        if (strpos($url, "segmentfault")) {
            $rules = $config->getConfig('segmentfault');
            $content = Segmentfault::getSegmentfault($html,$rules);
            $flag = 'segmentfault';
        } else if (strpos($url, "tuicool")) {
            $rules = $config->getConfig('tuicool');
            $content = Tuicool::getTuiku($html,$rules);
            $flag = 'tuicool';
        } else if (strpos($url, "cnblogs")) {
            $rules = $config->getConfig('cnblogs');
            $content = Cnblogs::getCnblogs($html,$rules);
            $flag = 'cnblogs';
            $name = explode(".", $name)[0];
        } else if (strpos($url, "github")) {
            $rules = $config->getConfig('github');
            $content = Github::getGithub($html,$rules);
            $flag = 'github';
        } else if (strpos($url, "zhihu")) {
            $rules = $config->getConfig('zhihu');
            $content = Zhihu::getZhihu($html,$rules,$url);
            $flag = 'zhihu';
        } else if (strpos($url, "weixin")) {
            $rules = $config->getConfig('weixin');
            $content = Weixin::getWeixin($html,$rules,$url);
            $flag = 'weixin';
        } else if (strpos($url, "csdn")) {
            $rules = $config->getConfig('csdn');
            $content = Csdn::getCSDN($html,$rules,$url);
            $flag = 'csdn';
        } else if (strpos($url, "sou-yun")) {
            $rules = $config->getConfig('souyun');
            $content = Souyun::getYun($html,$rules,$url);
            $name = explode("=", $name)[1];
            $flag = 'souyun';
        }
        if ($content) {
            self::putContent($name, $content, $flag);
            echo ".";
            return 1;
        } else {
            echo "X";
            return 0;
        }

    }

    private static function putContent($name, $content, $flag) {
        $file = "../out/" . $flag . "/" . $flag . $name . ".md";
        if (is_file($file)) {
            unlink($file);
        }
        $fp = fopen($file, "a");
        fwrite($fp, $content);
        fclose($fp);
    }
    // 用 sqllite 存储已抓取过的 url 
    public static function getListUrl($url){
        // 根据 url 中的关键字 判断采取何种 rule 
        // 列表 list 收藏 bookmarks 页面总结 page 

        // 还需要分页抓取 
        
        $keyword = self::getKeyWord($url);
        if (strpos($url, "zhuanlan.zhihu")) { // 知乎 特殊处理 直接抓取 json  &offset=20
            $prefix = "https://zhuanlan.zhihu.com";
            for($i=0;;$i++){
                $offset = 20 * $i;
                $newurl = $url . "?offset=" . $offset . "&limit=20";
                $data = GetHtml::getUrl($newurl);
                $data = json_decode($data,true);
                if(!$data){
                    break;
                }
                foreach ($data as $val) {
                    $urls[] = $prefix . $val['url'];
                }
            }
            return $urls;
        }
        
        $configs = new Config();
        $html = GetHtml::getUrl($url); // 获取下拉才会出现的 ajax 内容 未解决
        // 分离列表项
        // if (strpos($url, "segmentfault")) {
        //     $rules = $configs->getListConfig('segmentfault');
        // } else if (strpos($url, "tuicool")) {
        //     $rules = $configs->getListConfig('tuicool');
        // } else if (strpos($url, "cnblogs")) {
        //     $rules = $configs->getListConfig('cnblogs');
        // } else if (strpos($url, "github")) {
        //     $rules = $configs->getListConfig('github');
        // } 

        $rules = $configs->getListConfig($keyword);
        $prefixs = [
            'cnblogs' => '',
            'tuicool' => 'https://www.tuicool.com',
            'segmentfault' => 'https://segmentfault.com',
            'github' => '',
            'zhihu' => '',
            'csdn' => '',
        ];
        $prefix = $prefixs[$keyword];

        // if($keyword == 'segmentfault'){
        //     $prefix = "https://segmentfault.com";
        // }else if($keyword == 'tuicool'){
        //     $prefix = "https://www.tuicool.com";
        // }

        $data = QueryList::html($html)->rules($rules)->query()->getData();
        $ret = $data->all();
        // echo $html;
        // var_dump($ret);exit();
        foreach ($ret as $val) {
            $urls[] = $prefix . $val['url'];
        }
        return $urls;
    }

    public static function getKeyWord($url){
        $arr = ['cnblogs', 'tuicool', 'segmentfault', 'github'];
        $res = array_filter(array_map(function($val) use ($url){
                                $rr = strpos($url, $val);
                                if($rr!==false)
                                    return $rr;
                                else
                                    return false;
                            }, $arr), 
                            function($v, $k){
                                  return $v!==false;  
                            }, 
                            ARRAY_FILTER_USE_BOTH
        );
        $res = array_keys($res);
        if($res){
            return $arr[$res[0]];
        }
        return 0;
    }
}
