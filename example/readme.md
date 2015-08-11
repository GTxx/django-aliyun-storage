## 安装aliyun django oss库
git clone https://github.com/GTxx/django-aliyun-storage
cd django-aliyun-storage
python setup.py install

## 修改aliyun oss的配置
替换成自己的秘钥。
*ALIYUN_OSS_ACCESS_HOST*各个区域不一样，请根据自己oss所在地查询阿里云提供的地址。

## 运行
```
python manage.py syncdb
python manage.py runserver
```
上传后，可以到阿里云oss控制台查看文件是否正确上传。
