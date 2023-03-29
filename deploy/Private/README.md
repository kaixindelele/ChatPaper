# 简介

这是ChatPaper的私有化部署方案

# 步骤

1. 修改`apikey.ini`中的`OPENAI_API_KEYS`，这里允许您装载多个API账号，填入方式：
```python
OPENAI_API_KEYS = [sk-vxotnVJ6LKf40p9KCX5XXXXXXXXXXXXXXXXXXX, sk-qbsY4V9i9XXXXXXXXXXXXXXXXXXXXXXXXXXX]
```

2. 如果您使用[Hugging Face](https://huggingface.co/) 部署您的私有化方案，您应该保持Space为`Private` 状态，则您可以使用该服务。Hugging Face部署只需要将该工程目录下文件全部上传到自己的Space即可。

3. 使用公有云服务部署，则您可以在`app.py`的第632行gradio.Interface中添加账号和密码访问。

4. 若部署在docker中，因为localhost回环地址无法被外界访问，您需要将`app.py`的第635行interface.launch()中添加参数server_name="0.0.0.0"进而实现外部设备的监听。