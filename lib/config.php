<?php 
// 配置文件
namespace Tools;

class Config{
    public static  function getConfig($str){
        $config = [
            "tuicool" => array(
                "title" => array(".article_row_fluid h1", 'text'),
                "source" => array(".article_meta .source a", 'text'),
                "time" => array(".article_meta .timestamp", 'text'),
                "body" => array("#nei", 'html'),
            ),
            "csdn" => array(
                "title" => array("h1", 'text'),
                "source" => array("h1 a", 'href'),
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
                "titleimg" => array(".TitleImage", 'src'),
                "time" => array(".ContentItem-time a span", 'text'),
                "body" => array(".Post-RichText", 'html'),
            ),
            "weixin" => array( 
                "title" => array("#activity-name", 'text'),
                // "source" => array(".article_meta .source a", 'text'),
                "time" => array("#post-date", 'text'),
                "body" => array("#js_content", 'html'),
            ),
            "kancloud" => array( 
                // "title" => array("#activity-name", 'text'),
                // "source" => array(".article_meta .source a", 'text'),
                // "time" => array("#post-date", 'text'),
                "body" => array(".content", 'html'),
            ),
            "souyun" => array(
                "body" => array(".tab-page:eq(0)", "html")
            ),
            "jianshu" => array( 
                "title" => array("h1", 'text'),
                "time" => array(".publish-time", 'text'),
                "body" => array(".show-content", 'html'),
            ),
            "zcfy" => array( 
                "title" => array(".detail-title", 'text'),
                "time" => array("time", 'text'),
                "from" => array(".orginal-source-url", 'href'),
                "body" => array(".markdown-body", 'html'),
            ),
        ];
        return $config[$str];
    }

    /**
     * 获取页面链接集合
     * @param  string $name 
     * @return array
     */
    public static function getListConfig($name){
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
                "url" => array(".js-issue-row .js-navigation-open", 'href')
            ),
            "zhihu" => array( // issue
                "url" => array(".js-issue-title", 'text')
            ),
        ];
        return $config[$name];
    }
}
