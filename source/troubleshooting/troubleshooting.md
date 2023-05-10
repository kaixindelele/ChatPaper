# Troubleshoting
## Proxy-related issues
If you are behind a proxy, you may need to configure `chat_paper.py` and add the following line:

```python
os.environ["http_proxy"] = "http://<proxy_ip>:<proxy_port>" 
os.environ["https_proxy"] = "http://<proxy_ip>:<proxy_port>"
```

## OpenAI API issues
If you are encountering the below error message:
```
openai.error.RateLimitError: Your access was terminated due to violation of our polices, please check your email for more information. if you believe this is in error and would like to appeal, please contact support@openai.com.
```
It means that your OpenAI API key has been revoked. You may register a new one and replace the old one in `chat_paper.py`.