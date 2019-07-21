### python实用小工具

## 1. 按层级爬取github链接
>log.py 日志输出与日志保存<br>
>crawl_github.py 爬取github并下载<br>
>存在问题:
>> 1. get_items_from_url()可能会发生超时异常
>> 2. 当下载失败时会写入到a.txt文件，缺少一个解析a.txt的功能
>> 3. 无多线下载
>> 4. 文件夹的path为空的问题
## 2. 换行字符 window linux切换
> change.py
> 编码(utf-8、gb2312等)和换行符的批量切换代码
> 存在问题：
> 1. 目前的换行符尚且存在问题