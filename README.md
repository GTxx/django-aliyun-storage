django aliyun oss storage
==========================

[![Build Status](https://travis-ci.org/GTxx/django-aliyun-storage.svg?branch=master)](https://travis-ci.org/GTxx/django-aliyun-storage)

### 使用说明
在**settings.py**中加入
```python
ALIYUN_OSS_ACCESS_KEY_ID = 'your_key_id'
ALIYUN_OSS_ACCESS_KEY_SECRET = 'your_access_key'
ALIYUN_OSS_BUCKET_NAME = 'your_bucket_name'
ALIYUN_OSS_ACCESS_HOST = 'your_host_address'
# ALIYUN_OSS_FILE_OVERWRITE = True
DEFAULT_FILE_STORAGE = 'oss_storage.storage.AliyunStorage'
```

### NOTE:
存储使用[阿里云oss python sdk 0.3.7](http://docs.aliyun.com/?spm=5176.383663.9.4.HPtEmb#/oss/sdk/sdk-download&python)
