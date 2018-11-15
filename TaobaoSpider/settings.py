# -*- coding: utf-8 -*-

# Scrapy settings for TaobaoSpider project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://doc.scrapy.org/en/latest/topics/settings.html
#     https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://doc.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'TaobaoSpider'
SPIDER_MODULES = ['TaobaoSpider.spiders']
NEWSPIDER_MODULE = 'TaobaoSpider.spiders'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
# USER_AGENT = 'TaobaoSpider (+http://www.yourdomain.com)'
# 远程调试数据库
# DOWNLOAD_DELAY = 2
db_host = 'rm-bp1582z2vc8ca63txo.mysql.rds.aliyuncs.com'
db_user = 'shengdun'
db_pawd = 'SdPQ_!)@$-1024'
db_name = 'shengdun'
db_port = 3306

# REDIS_HOST = '47.98.205.93'
REDIS_HOST = '127.0.0.1'
REDIS_PORT = 6379

# 代理池相关配置
USE_PROXY = False
REDIS_DB_PROXY = 15  # 代理IP池所使用的DB
REDIS_DB_KEY = "proxy_key"  # 代理IP池所使用的 redis key
# Obey robots.txt rules
ROBOTSTXT_OBEY = False
# REDIS 相关配置  分布式Reids配置
DUPEFILTER_CLASS = "scrapy_redis.dupefilter.RFPDupeFilter"
SCHEDULER = "scrapy_redis.scheduler.Scheduler"
SCHEDULER_PERSIST = True
from scrapy.core.scheduler import Scheduler
from scrapy_redis.scheduler import Scheduler
# Configure maximum concurrent requests performed by Scrapy (default: 16)
# CONCURRENT_REQUESTS = 1
# CONCURRENT_REQUESTS_PER_DOMAIN = 1
# CONCURRENT_REQUESTS_PER_IP = 1
# Configure a delay for requests for the same website (default: 0)
# See https://doc.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
# The download delay setting will honor only one of:

# Disable cookies (enabled by default)
# COOKIES_ENABLED = True
# HTTPERROR_ALLOWED_CODES = [302, ]
# Disable Telnet Console (enabled by default)
# TELNETCONSOLE_ENABLED = False

# Override the default request headers:
# DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
# }

# Enable or disable spider middlewares
# See https://doc.scrapy.org/en/latest/topics/spider-middleware.html
# SPIDER_MIDDLEWARES = {
#    'TaobaoSpider.middlewares.TaobaospiderSpiderMiddleware': 543,
# }

# Enable or disable downloader middlewares
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
   'TaobaoSpider.middlewares.TaobaospiderDownloaderMiddleware': 543,
}

# Enable or disable extensions
# See https://doc.scrapy.org/en/latest/topics/extensions.html
# EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
# }

# Configure item pipelines
# See https://doc.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
    'TaobaoSpider.pipelines.TaobaospiderPipeline': 300,

}

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/autothrottle.html
# AUTOTHROTTLE_ENABLED = True
# The initial download delay
# AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
# AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
# AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
# AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
# HTTPCACHE_ENABLED = True
# HTTPCACHE_EXPIRATION_SECS = 0
# HTTPCACHE_DIR = 'httpcache'
# HTTPCACHE_IGNORE_HTTP_CODES = []
# HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'
