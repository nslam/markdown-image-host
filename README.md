# markdown-image-host
自动将markdown中的本地图片上传到图床，并且进行url替换的小工具~

### 环境

- python 3.7.1

### 阿里云OSS图床配置

在`~/.ossconfig`下写下如下配置:

```
{
	"Bucket":"BUCKET",
	"EndPoint":"oss-cn-beijing.aliyuncs.com",
	"UrlPrefix":"https://image-host.nslamgg.com",
	"AccessKeyId":"YOURAKID",
	"AccessKeySecret":"YOURAKS"
}
```
### 运行

1. 确保是3.7.1的环境，然后运行`pip install -r requirements.txt`
2. 执行`python main.py PATH/TO/MARKDOWN/FILE`

会在同样路径下生成一个FILENAME.convert文件，即为自动上传图床后的markdown文件