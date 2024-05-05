博客采用Hugo生成，官网<https://www.gohugo.org/>

## 常用命令

1. 指定目录新建博客

`hugo new posts/test.md`

2. 构建生成静态页面，在public下生成内容

`hugo -D`

3. 启动Hugo的开发服务器，在本地文件发生变化时重新构建网站并刷新浏览器，同时包括草稿内容

`hugo server -w -D`

## Typora写markdown

hugo是一个静态博客生成工具，有自己的文件组织方式，导致的结果就是使用typora不能正常显示图片，插入图片也不能放在正确的位置上。为了解决这个问题,按下面约定来书写：


```
├── java
│   └── 2024-05-05-learn-java
│       ├── index.md
│       └── java-logo.jpg
```

创建文章目录，在目录里新建index.md，图片粘贴时默认拷贝到同目录，这样markdown书写时可以正常预览，构建静态页面后也能正常访问。

