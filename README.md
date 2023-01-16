# chinese_gupiao_research

#### 
A股股票研究

流程：
1，从tushare获取数据，并存入本地MySQL数据库中。
2，从本地MySQL数据库中，读取所需数据。
3，分析数据。

todo：
1，如何从tushare获取数据（每日交易数据，股票列表）。
2，将从tushare获取的数据，存入本地MySQL数据库。
3，在Windows电脑上，使用计划任务，自动下载更新数据。

使用方法：
1，下载到本地。
2，将get_tushare_token.py文件中的token，替换成自己的tushare提供的token.
