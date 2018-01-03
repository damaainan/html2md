<?php 
// 配置文件

$config = [
        "tuicool" => array(
            "title" => array(".article_row_fluid h1", 'text'),
            "source" => array(".article_meta .source a", 'text'),
            "time" => array(".article_meta .timestamp", 'text'),
            "body" => array("#nei", 'html'),
        ),
        "csdn" => array(
            "title" => array(".article_row_fluid h1", 'text'),
            "source" => array(".article_meta .source a", 'text'),
            "time" => array(".article_meta .timestamp", 'text'),
            "body" => array("#nei", 'html'),
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

        ),
    ];