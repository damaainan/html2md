<?php 
// 配置文件
namespace Tools;

class Config{
    public  function getConfig($str){
        $config = [
            "tuicool" => array(
                "title" => array(".article_row_fluid h1", 'text'),
                "source" => array(".article_meta .source a", 'text'),
                "time" => array(".article_meta .timestamp", 'text'),
                "body" => array("#nei", 'html'),
            ),
            "csdn" => array(
                "title" => array(".article_title h1 a", 'text'),
                "source" => array(".article_title h1 a", 'href'),
                "time" => array(".article_r .link_postdate", 'text'),
                "body" => array("#article_content", 'html'),
            ),
            "segmentfault" => array(
                "title" => array("#articleTitle a", 'text'),
                "source" => array("#articleTitle a", 'href'),
                // "time" => array(".",'text'),
                "body" => array(".article__content", 'html'),
            ),
            "cnblogs" => array(
                "title" => array("#cb_post_title_url", 'text'),
                "source" => array("#cb_post_title_url", 'href'),
                "time" => array("#post-date", 'text'),
                "body" => array("#cnblogs_post_body", 'html'),
            ), //博客园

            "jobbole" => array(
                "title" => array(".article_row_fluid h1", 'text'),
                "source" => array(".article_meta .source a", 'text'),
                "time" => array(".article_meta .timestamp", 'text'),
                "body" => array("#nei", 'html'),
            ), // 伯乐在线
            "mengzhidu" => array( // https://www.mengzhidu.com/online/item/4/49

            ),
            "github" => array( // issue
                "title" => array(".js-issue-title", 'text'),
                // "source" => array(".article_meta .source a", 'text'),
                "time" => array("relative-time", 'datetime'),
                "body" => array("td.d-block", 'html'),
            ),
            "zhihu" => array( 
                "title" => array("h1", 'text'),
                // "source" => array(".article_meta .source a", 'text'),
                "time" => array("time", 'datetime'),
                "body" => array(".PostIndex-content", 'html'),
            ),
            "weixin" => array( 
                "title" => array("#activity-name", 'text'),
                // "source" => array(".article_meta .source a", 'text'),
                "time" => array("#post-date", 'text'),
                "body" => array("#js_content", 'html'),
            ),
        ];
        return $config[$str];
    }

    /**
     * 获取页面链接集合
     * @param  string $name 
     * @return array
     */
    public function getListConfig($name){
        $config = [
            "tuicool" => array(
                "url" => array(".single_simple span a", 'href')
            ),
            "csdn" => array(
                "url" => array(".article_row_fluid h1", 'text')
            ),
            "segmentfault" => array(
                "url" => array(".summary h2 a", 'href')
            ),
            "cnblogs" => array(// 还有页面中的
                "url" => array("#myposts .PostList .postTitl2 a", 'href')
            ), //博客园

            "jobbole" => array(
                "url" => array(".article_row_fluid h1", 'text')
            ), // 伯乐在线
            "mengzhidu" => array( // https://www.mengzhidu.com/online/item/4/49

            ),
            "github" => array( // issue
                "url" => array(".js-issue-title", 'text')
            ),
            "zhihu" => array( // issue
                "url" => array(".js-issue-title", 'text')
            ),
        ];
        return $config[$name];
    }
}
