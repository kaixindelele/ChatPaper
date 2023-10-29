#!/bin/bash
# 后台启动scipdf服务
nohup bash serve_grobid.sh &

# 启动python程序
python chat_translate.py