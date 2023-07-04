# instagram-crawler
针对Instagram的爬虫工具。  
## ins_img_downloader.py（已失效）  
爬取指定用户主页所有帖子里的所有图片（不论是单张还是多张），最多测试过4000个帖子的主页可以稳定运行。  
下载过的图片不会被重复下载，报错可以自动从断点处继续。  
需要自行抓包，以获取到开头为 ```?query_hash=``` 的请求地址，和其请求头中的 ```cookie``` 。  
例：  
```
user_name = '……'  
url = 'https://www.instagram.com/graphql/query/?query_hash=……'  
cookie = 'mid=……'  
  
download_helper(user_name, url, cookie)  
```  
## get_single_image.py（已失效）  
爬取指定帖子里的所有图片（不论是单张还是多张）。  
下载过的图片不会被重复下载。  
需要自行抓包，以获取到自己的 ```cookie``` 。  
例：  
```
folder_name = 'single_img'
url = 'https://www.instagram.com/p/……/'
cookie = 'mid=……'

download_helper(folder_name, url, cookie)
```  
