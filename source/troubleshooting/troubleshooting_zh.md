# 疑难解答
## 代理相关问题

如果您在使用代理，你可能需要配置`chat_paper.py`，添加以下代码：

```python
os.environ["http_proxy"] = "http://<代理ip>:<代理端口号>"
os.environ["https_proxy"] = "http://<代理ip>:<代理端口号>"
```

如果您在使用 `pip` 安装依赖包，您可能需要在 `pip` 命令中添加 `--proxy` 参数，例如：

```bash
pip install -r requirements.txt --proxy http://<代理ip>:<代理端口号>
``` 

或者，使用镜像源，例如：

```bash
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
```

## OpenAI API 相关问题
如果您遇到以下错误信息：

```
openai.error.RateLimitError: Your access was terminated due to violation of our polices, please check your email for more information. if you believe this is in error and would like to appeal, please contact support@openai.com.
```

这说明您的 OpenAI API 密钥已被 OpenAI 封锁。您可以注册一个新的 OpenAI 账号并生成一个新的密钥，并将旧的密钥替换为`chat_paper.py`中的新密钥。
