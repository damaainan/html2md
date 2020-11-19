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
            "githubio" => array( // 有新旧两种样式 
                "title" => array("h1", 'text'),
                "source" => array(".article_meta .source a", 'text'),
                "time" => array("time", 'datetime'),
                "body" => array(".article-entry", 'html'),
                // "time" => array(".post-time", 'text'),
                // "body" => array(".post-content", 'html'),
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
                "time" => array(".ContentItem-time", 'text'),
                "body" => array(".Post-RichText", 'html'),
            ),
            "weixin" => array( 
                "title" => array("#activity-name", 'text'),
                // "source" => array(".article_meta .source a", 'text'),
                "time" => array("#publish_time", 'text'),
                "body" => array("#js_content", 'html'),
            ),
            "kancloud" => array( 
                // "title" => array("#activity-name", 'text'),
                // "source" => array(".article_meta .source a", 'text'),
                // "time" => array("#post-date", 'text'),
                "body" => array(".content", 'html'),
            ),
            "souyun" => array( // 未完成
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
            "laravel" => array( // https://laravel-china.org
                "title" => array("h1", 'text'),
                "time" => array(".timeago", 'title'),
                "body" => array("#emojify", 'html'),
            ),
            "51cto" => array( // http://blog.51cto.com
                "title" => array(".artical-title", 'text'),
                "time" => array(".artical-title-list .time", 'text'),
                "body" => array(".main-content", 'html'),
            ),
            "aliyun" => array( // https://yq.aliyun.com
                "title" => array(".blog-title", 'text'),
                "summary" => array(".blog-summary", "text"),
                "time" => array(".blog-o-info .b-time", 'text'),
                "body" => array(".content-detail", 'html'),
            ),
            "juejin" => array( // https://juejin.im
                "title" => array(".article-title", 'text'),
                "time" => array("time", 'text'),
                "body" => array(".article-content", 'html'),
            ),
            "juejin-entry" => array( // https://juejin.im 转载的文章
                "title" => array("h1", 'text'),
                "time" => array(".entry-public-info div:eq(2)", 'text'),
                "body" => array(".article-content", 'html'),
            ),
            "tianya" => array(
                "title" => array(),
            ),
            "pythoncaff" => array( // https://pythoncaff.com/docs/
                "title" => array("h1 span", 'text'),
                "book" => array(".book-article-meta a:eq(0)", 'text'),
                "chapter" => array(".book-article-meta a:eq(1)", 'text'),
                "body" => array(".markdown-body", 'html'),
            ),

            "mysql" => array( // http://mysql.taobao.org/monthly/2020/06/05/
                "title" => array(".title h2", 'text'),
                "body" => array(".content", 'html'),
            ),
            // https://wdxtub.com/interview/14520597062776.html  小土刀面试
            
            "xiaowu" => array( // https://www.cxyxiaowu.com
                "title" => array("h1", 'text'),
                "body" => array(".entry-content", 'html'),
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
            "jianshu" => array(
                "url" => array("", '')
            ),
            "laravel" => array(
                "url" => array(".rm-link-color", 'href')
            ),
            "pythoncaff" => array(
                "url" => array(".sorted_table .chapter-container:eq(1) li a", 'href')
            ),
            "xiaowu" => array( // https://www.cxyxiaowu.com
                "url" => array(".site-main .posts-wrapper div .entry-wrapper .grid_author_avt", 'href')
            ),
            "weixin" => array( // https://mp.weixin.qq.com
                "url" => array(".list-paddingleft-2 li p a", 'href')
            )
        ];
        return $config[$name];
    }
}
