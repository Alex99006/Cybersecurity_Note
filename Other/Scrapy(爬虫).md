## Scrapy

我们将利用 Scrapy 和一个专门为侦察 而定制的爬虫`inlanefreight.com`。如果您对爬取/蜘蛛技术感兴趣，请参阅“[使用 Web 代理](https://academy.hackthebox.com/module/details/110)”模块，因为它也是 CBBH 的一部分。

### 安装 Scrapy

在开始之前，请确保你的系统上已经安装了 Scrapy。如果没有，你可以使用 Python 软件包安装程序 pip 轻松安装它：

 令人毛骨悚然的爬行动物

```apl
123123@htb[/htb]$ pip3 install scrapy
```

此命令将下载并安装 Scrapy 及其依赖项，为构建我们的蜘蛛做好环境准备。

### 侦察蜘蛛

首先，在终端中运行此命令以下载自定义 scrapy 蜘蛛，`ReconSpider`并将其解压到当前工作目录。

 令人毛骨悚然的爬行动物

```apl
123123@htb[/htb]$ wget -O ReconSpider.zip https://academy.hackthebox.com/storage/modules/144/ReconSpider.v1.2.zip
123123@htb[/htb]$ unzip ReconSpider.zip 
```

提取文件后，您可以`ReconSpider.py`使用以下命令运行：

 令人毛骨悚然的爬行动物

```apl
123123@htb[/htb]$ python3 ReconSpider.py http://inlanefreight.com
```

替换`inlanefreight.com`为您想要蜘蛛抓取的域名。蜘蛛将抓取目标并收集有价值的信息。

### 结果.json

运行后`ReconSpider.py`，数据将保存在 JSON 文件中`results.json`。您可以使用任何文本编辑器浏览此文件。生成的 JSON 文件结构如下：

代码：json

```json
{
    "emails": [
        "lily.floid@inlanefreight.com",
        "cvs@inlanefreight.com",
        ...
    ],
    "links": [
        "https://www.themeansar.com",
        "https://www.inlanefreight.com/index.php/offices/",
        ...
    ],
    "external_files": [
        "https://www.inlanefreight.com/wp-content/uploads/2020/09/goals.pdf",
        ...
    ],
    "js_files": [
        "https://www.inlanefreight.com/wp-includes/js/jquery/jquery-migrate.min.js?ver=3.3.2",
        ...
    ],
    "form_fields": [],
    "images": [
        "https://www.inlanefreight.com/wp-content/uploads/2021/03/AboutUs_01-1024x810.png",
        ...
    ],
    "videos": [],
    "audio": [],
    "comments": [
        "<!-- #masthead -->",
        ...
    ]
}
```

JSON 文件中的每个键代表从目标网站提取的不同类型的数据：

| JSON 密钥        | 描述                                           |
| ---------------- | ---------------------------------------------- |
| `emails`         | 列出在域中找到的电子邮件地址。                 |
| `links`          | 列出域内找到的链接的 URL。                     |
| `external_files` | 列出外部文件（例如 PDF）的 URL。               |
| `js_files`       | 列出网站使用的 JavaScript 文件的 URL。         |
| `form_fields`    | 列出在域中找到的表单字段（本例中为空）。       |
| `images`         | 列出在域中找到的图像的 URL。                   |
| `videos`         | 列出在域中找到的视频的 URL（本例中为空）。     |
| `audio`          | 列出在域中找到的音频文件的 URL（本例中为空）。 |
| `comments`       | 列出源代码中找到的 HTML 注释。                 |