# weixin_public
一个抓微信公众号文章并发送email 的爬虫
目标问题：地铁上或公司厕所没有信号，无法看公众号文章，即使是保存到印象笔记也不能离线查看。
没解决问题：
1.前段技术不够，所以不能自动输入微信公众号抓js中的文章的列表(还有一个根据openid加密后的参数)，用的是手动获取js地址添加到字典，再去爬其中的文章列表。
2.图片解析可能不全面，代码中只是粗粗的把所有的img标签中获取data－src链接作为src属性值，删除其他。
