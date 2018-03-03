

文件重命名
```php
<?php
// 修改参数即可
$arr = glob("zhihu*.md");
foreach ($arr as $val) {
    $handler = fopen($val, 'r');
    $name = fgets($handler);
    $name = explode("## ", $name)[1];
    $name = trim($name);
    // echo $name;
    fclose($handler);
    rename("./" . $val, "./" . $name . ".md");
}
```

图片批量下载 

```

``` 

