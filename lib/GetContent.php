<?php
namespace Tools;

// header("Content-type:text/html; Charset=utf-8");
require "../vendor/autoload.php";
// require '../phpQuery/phpQuery.php';
// require "replaceElement.calss.php";

// require "config.php"; // 能不能不用引入的方式？

use QL\QueryList;
//use Tools\replaceElement;
//use Tools\GetHtml;
//use Tools\Config; // 同一命名空间下 会自动寻找

// php7 新特性 use方法 批量导入
use Tools\lib\{Tuicool, Segmentfault, Cnblogs, github, zhihu, csdn, souyun, Weixin, Jianshu, Zcfy, Laravel, GithubIO, Cto, Ruan, Aliyun};

// use Tools\lib\Segmentfault;
// use Tools\lib\Cnblogs;
// use Tools\lib\github;
// use Tools\lib\zhihu;
// use Tools\lib\csdn;
// use Tools\lib\souyun;
// use Tools\lib\Weixin;
// use Tools\lib\Jianshu;
// use Tools\lib\Zcfy;
// use Tools\lib\Laravel;
// use Tools\lib\GithubIO;
// use Tools\lib\Cto;
// use Tools\lib\Ruan;
// use Tools\lib\Aliyun;

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

    public static function getConfig($name) {
        // require "config.php";  // 这样很 low 
        // var_dump($config);
        // return $config;
        // $config = new Config();
        return Config::getConfig($name);
    }

    public static function doMark($url) {
        // $config = new Config();
        // $configs = $config->getConfig();

        // var_dump($configs);die();
        $arr = explode('/', $url);
        $name = $arr[count($arr) - 1];
        if($name == ''){
            $name = $arr[count($arr) - 2];
        }
        // $html = file_get_contents($url); // 可以优化为专门的 curl 方法
        $html = GetHtml::getUrl($url); // 可以优化为专门的 curl 方法
        // $configs = $this->configs;

        // array_search 
        // 判断 url 选择方法
        $content = '';
        $flag = '';
        if (strpos($url, "segmentfault")) {
            $rules = Config::getConfig('segmentfault');
            $content = Segmentfault::getSegmentfault($html,$rules);
            $flag = 'segmentfault';
        } else if (strpos($url, "tuicool")) {
            $rules = Config::getConfig('tuicool');
            $content = Tuicool::getTuiku($html,$rules);
            $flag = 'tuicool';
        } else if (strpos($url, "cnblogs")) {
            $rules = Config::getConfig('cnblogs');
            $content = Cnblogs::getCnblogs($html,$rules);
            $flag = 'cnblogs';
            $name = explode(".", $name)[0];
        } else if (strpos($url, "github.io") && strpos($url, "github.io") == strpos($url, "github")) {
            $rules = Config::getConfig('githubio');
            $content = GithubIO::getGithubIO($html,$rules, $url);
            $flag = 'githubio';
        } else if (strpos($url, "github")) {
            $rules = Config::getConfig('github');
            $content = Github::getGithub($html,$rules, $url);
            $flag = 'github';
        } else if (strpos($url, "zhihu")) {
            $rules = Config::getConfig('zhihu');
            $content = Zhihu::getZhihu($html,$rules,$url);
            $flag = 'zhihu';
        } else if (strpos($url, "weixin")) {
            $rules = Config::getConfig('weixin');
            $content = Weixin::getWeixin($html,$rules,$url);
            $flag = 'weixin';
        } else if (strpos($url, "csdn")) {
            $rules = Config::getConfig('csdn');
            $content = Csdn::getCSDN($html,$rules,$url);
            $flag = 'csdn';
        } else if (strpos($url, "sou-yun")) {
            // $rules = Config::getConfig('souyun');
            $content = Souyun::getYun($html);
            $name = explode("=", $name)[1];
            $flag = 'souyun';
        } else if (strpos($url, "jianshu")) {
            $rules = Config::getConfig('jianshu');
            $content = Jianshu::getJianShu($html,$rules,$url);
            $flag = 'jianshu';
        } else if (strpos($url, "zcfy")) {
            $rules = Config::getConfig('zcfy');
            $content = Zcfy::getZCFY($html,$rules,$url);
            $flag = 'zcfy';
        } else if (strpos($url, "laravel")) {
            $rules = Config::getConfig('laravel');
            $content = Laravel::getLaravel($html,$rules,$url);
            $flag = 'laravel';
        } else if (strpos($url, "51cto")) {
            $rules = Config::getConfig('51cto');
            $content = Cto::getCto($html,$rules,$url);
            $flag = '51cto';
        } else if (strpos($url, "aliyun")) {
            $rules = Config::getConfig('aliyun');
            $content = Aliyun::getAliyun($html,$rules,$url);
            $flag = 'aliyun';
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
        $urls = [];
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
        
        // $configs = new Config();
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

        $rules = Config::getListConfig($keyword);
        $prefixs = [
            'cnblogs' => '',
            'tuicool' => 'https://www.tuicool.com',
            'segmentfault' => 'https://segmentfault.com',
            'github' => 'https://github.com',
            'zhihu' => '',
            'csdn' => '',
            'jianshu' => '',
            'laravel' => '',
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
        $arr = ['cnblogs', 'tuicool', 'segmentfault', 'github', 'jianshu', 'laravel'];
        $res = array_filter(array_map(function($val) use ($url){
                                $rr = strpos($url, $val);
                                if($rr!==false)
                                    return $rr;
                                else
                                    return false;
                            }, $arr), 
                            function($v){
                                  return $v!==false;  
                            }, 
                            ARRAY_FILTER_USE_BOTH
        );
        $ret = array_keys($res);
        $key = array_shift($ret); // 取开头第一个元素
        if($res){
            return $arr[$key];
        }
        return 0;
    }
}
