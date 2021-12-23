# instagram-crawler
针对Instagram的网络爬虫。  
## ins-img-downloader.py
爬取指定用户主页帖子里的所有图片（不论是单张还是多张），最多测试过4000个帖子可以稳定运行，下载过的图片不会被重复下载，报错可以自动从断点处继续。  
需要自行爬取开头为**?query_hash**的请求地址，以及其中的**cookie**。  
例：  
```
user_name = '……'  
url = 'https://www.instagram.com/graphql/query/?query_hash=……'  
cookie = 'mid=……'  
  
download_helper(user_name, url, cookie)  
```