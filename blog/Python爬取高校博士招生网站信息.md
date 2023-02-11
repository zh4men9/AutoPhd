## 前言
想通过python快速的爬取高校博士招生网站，进而整理一份网站名单，以方便查阅各大高校博士招生信息。

整理好的博客在这里：
[全国各大985/211博士招生网站](https://blog.csdn.net/qq_32614873/article/details/128983071?csdn_share_tail=%7B%22type%22:%22blog%22,%22rType%22:%22article%22,%22rId%22:%22128983071%22,%22source%22:%22qq_32614873%22%7D)


## Python爬取
### 1. 根据搜索引擎关键字爬取
常见搜索引擎搜索格式[1]：
- 百度搜索引擎：
http://www.baidu.com.cn/s?wd=’ 关键词’&pn=‘分页’。
wd是搜索的关键词，pn是分页的页面，由于百度搜索每页的结果是十个（最上面的可能是广告推广，不是搜索结果），所以pn=0是第一页，第二页是pn=10…
例如https://www.baidu.com/s?wd=python&pn=0，得到的是关于python的第一页搜索结果。
- 必应搜索引擎：
http://global.bing.com/search?q=‘关键词’
- 搜狗搜索引擎
https://www.sogou.com/web?query=‘关键词’
- 360搜索引擎
https://www.so.com/s?q=‘关键词’

这里，我采用必应搜索引擎。比如，我想搜索北京大学的博士招生信息，对应搜索指令为`http://global.bing.com/search?q=北京大学+博士招生`

所以现在需要解决的第一个问题就是如何利用python获取搜索引擎的搜索结果。

参考了如下文章后[2]，修改了自己的代码，实现了如下功能：自定义搜索关键字，获取搜索结果第一页结果，输出结果网页的标题及其对应URL到文件中，等待后续处理文件。

代码如下：

```python
import re
import requests
from lxml.html import etree
import time

# 重定向输出结果到./data/original_data.txt
import sys
sys.stdout = open('./data/original_data.txt', 'w', encoding='utf-8')

def get_bing_url(keywords):
    keywords = keywords.strip('\n')
    bing_url = re.sub(r'^', 'https://cn.bing.com/search?q=', keywords)
    bing_url = re.sub(r'\s', '+', bing_url)
    return bing_url


if __name__ == '__main__':
    # base_keys是读取基础的搜索关键字，这里是“+博士招生+2023”， 你可以自定义其他搜索关键字，加号表示空格，即搜索结果中需要包含的关键字
    base_keys = open('./data/base.txt', 'r', encoding='utf-8')
    for key in base_keys:
        # added_keys是读取附加的搜索关键字，比如“北京大学”
        added_keys = open('./data/add.txt', 'r', encoding='utf-8') # add.txt contains the name of universities
        for t_key in added_keys:
            new_key = t_key.strip()+key.strip()
            print(t_key)
            bing_url = get_bing_url(new_key)

            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:81.0) Gecko/20100101 Firefox/81.0',
                    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                    'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
                    'Accept-Encoding': 'gzip, deflate',
                    'cookie': 'DUP=Q=sBQdXP4Rfrv4P4CTmxe4lQ2&T=415111783&A=2&IG=31B594EB8C9D4B1DB9BDA58C6CFD6F39; MUID=196418ED32D66077102115A736D66479; SRCHD=AF=NOFORM; SRCHUID=V=2&GUID=DDFFA87D3A894019942913899F5EC316&dmnchg=1; ENSEARCH=BENVER=1; _HPVN=CS=eyJQbiI6eyJDbiI6MiwiU3QiOjAsIlFzIjowLCJQcm9kIjoiUCJ9LCJTYyI6eyJDbiI6MiwiU3QiOjAsIlFzIjowLCJQcm9kIjoiSCJ9LCJReiI6eyJDbiI6MiwiU3QiOjAsIlFzIjowLCJQcm9kIjoiVCJ9LCJBcCI6dHJ1ZSwiTXV0ZSI6dHJ1ZSwiTGFkIjoiMjAyMC0wMy0xNlQwMDowMDowMFoiLCJJb3RkIjowLCJEZnQiOm51bGwsIk12cyI6MCwiRmx0IjowLCJJbXAiOjd9; ABDEF=V=13&ABDV=11&MRNB=1614238717214&MRB=0; _RwBf=mtu=0&g=0&cid=&o=2&p=&c=&t=0&s=0001-01-01T00:00:00.0000000+00:00&ts=2021-02-25T07:47:40.5285039+00:00&e=; MUIDB=196418ED32D66077102115A736D66479; SerpPWA=reg=1; SRCHUSR=DOB=20190509&T=1614253842000&TPC=1614238646000; _SS=SID=375CD2D8DA85697D0DA0DD31DBAB689D; _EDGE_S=SID=375CD2D8DA85697D0DA0DD31DBAB689D&mkt=zh-cn; _FP=hta=on; SL_GWPT_Show_Hide_tmp=1; SL_wptGlobTipTmp=1; dsc=order=ShopOrderDefault; ipv6=hit=1614260171835&t=4; SRCHHPGUSR=CW=993&CH=919&DPR=1&UTC=480&WTS=63749850642&HV=1614256571&BRW=HTP&BRH=M&DM=0'
                    }

            for i in range(1, 2):  # 通过for in来翻页
                if i == 1:
                    url = bing_url
                else:
                    url = bing_url + '&qs=ds&first=' + str((i * 10) - 1) + '&FORM=PERE'
                content = requests.get(url=url, timeout=5, headers=headers)
                # 获取content中网页的url
                tree = etree.HTML(content.text)
                li = tree.xpath('//ol[@id="b_results"]//li[@class="b_algo"]')[0] # [0] query the first result

                try:
                    h3 = li.xpath('//h2/a')
                    for h in h3:
                        result_url = h.attrib['href'] # 获取网页的url
                        text = h.text # 获取网页的标题
                        if ('招生简章' in text or '研究生院' in text or '研究生招生' in text):
                            print(f'{text} {result_url}') # 写到文件中（因为最开始重定向了输出结果到./data/original_data.txt）
                    print('=======================')
                except Exception:
                    print('error')
```

最终得到原始URL文件，结果如下图所示：
![在这里插入图片描述](https://img-blog.csdnimg.cn/0aa354b37f6f4bd796fe96dad7077065.png)
### 2. 处理original_data文件

经过上一步骤后，得到了搜索引擎检索到的最可能包含博士招生网页的url，现在就需要对original_data文件进行处理。这里采用最笨的方法，手动筛选，直到找到想要的URL为止，这样省去了一个学校一个学校检索的步骤，相对省事了。（如果有大佬直到这一步怎么直接筛选得到招生网页，请联系我，感激不尽！）

经过处理后，得到了如下图所示内容：
![在这里插入图片描述](https://img-blog.csdnimg.cn/0f52e417021e419e82ffbc53dbeba3a6.png)

### 3. 转换成Markdown格式

为了方便自己和大家使用，转换成Markdown，然后发布在博客上，可以直接点击学校名字就能访问招生主页了。

Markdown超链接格式为：`[]()`，所以可以通过python很方便的直接处理URL得到想要的格式，代码如下：

```python
# process url to Markdown formate —— [infomation](url)

output_file_path = './data/url.md'
output_file = open(output_file_path, 'w', encoding='utf-8')
# read url from ./data/phd_url.txt
with open('./data/phd_url.txt', 'r', encoding='utf-8') as f:
    while True:

        url_list = f.readline()
        
        if not url_list: # 表明读取到文件末尾
            break
        url_list = url_list.strip()# 去掉末尾的换行符
        urls = url_list.split(' ')
        
        if (len(urls)==1): # 表明没有对应url
            output_file.write(urls[0]+'(待更新)')
            output_file.write('\n')
        elif (len(urls)==2):
            output_file.write('['+urls[0]+']('+urls[1]+')')
            output_file.write('\n')
        else:
            print('error: url format error')
```

整理好的博客在这里：
[全国各大985/211博士招生网站](https://blog.csdn.net/qq_32614873/article/details/128983071?csdn_share_tail=%7B%22type%22:%22blog%22,%22rType%22:%22article%22,%22rId%22:%22128983071%22,%22source%22:%22qq_32614873%22%7D)


## 开源资料

整理好的文档和python文件我开源在了自己的GitHub上：[AutoPhd](https://github.com/zh4men9/AutoPhd)


## 参考资料
[1] [python搜索引擎根据关键词爬取内容](https://blog.csdn.net/qq_39178473/article/details/105348291)
[2] [如何扩展关键词，以及使用python多线程爬取bing搜索结果](https://blog.csdn.net/cll_869241/article/details/114081292#:~:text=%E5%A6%82%E4%BD%95%E6%89%A9%E5%B1%95%E5%85%B3%E9%94%AE%E8%AF%8D%EF%BC%8C%E4%BB%A5%E5%8F%8A%E4%BD%BF%E7%94%A8python%E5%A4%9A%E7%BA%BF%E7%A8%8B%E7%88%AC%E5%8F%96bing%E6%90%9C%E7%B4%A2%E7%BB%93%E6%9E%9C%201%201.%E5%87%86%E5%A4%87%E5%9F%BA%E6%9C%AC%E7%9B%B8%E5%85%B3%E5%85%B3%E9%94%AE%E8%AF%8D%202%202.%E5%88%86%E6%9E%90bing%E6%90%9C%E7%B4%A2%E8%A7%84%E5%BE%8B%203,3.%E6%A0%B9%E6%8D%AE%E5%85%B3%E9%94%AE%E8%AF%8D%E7%94%9F%E6%88%90bing%20base_url%204%204.%E7%88%AC%E5%8F%96bing%E7%BB%93%E6%9E%9C%205%205.%E5%AD%98%E5%82%A8%E5%88%B0%E6%95%B0%E6%8D%AE%E5%BA%93%E4%B8%AD)
