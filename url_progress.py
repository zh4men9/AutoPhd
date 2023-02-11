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