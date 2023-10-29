# FROM grobid/grobid:0.8.0-SNAPSHOT
FROM lfoppiano/grobid:0.7.1

# 克隆GitHub仓库
RUN apt-get update --allow-releaseinfo-change
RUN apt-get install -y git --fix-missing

# RUN python -V
# # Install dependencies
# RUN apt-get update && \
#     apt-get install -y build-essential zlib1g-dev libncurses5-dev libgdbm-dev libnss3-dev libssl-dev libreadline-dev libffi-dev wget

# # Download and install Python 3.9.16
# RUN wget https://www.python.org/ftp/python/3.9.16/Python-3.9.16.tgz && \
#     tar -xvf Python-3.9.16.tgz && \
#     cd Python-3.9.16 && \
#     ./configure --enable-optimizations && \
#     make altinstall

# Install dependencies, including libbz2-dev for bz2 support
# RUN apt-get update --fix-missing
RUN apt-get install -y build-essential zlib1g-dev libncurses5-dev libgdbm-dev libnss3-dev libssl-dev libreadline-dev libffi-dev 
RUN apt-get install -y wget libbz2-dev

# Download and install Python with bz2 support
RUN wget https://www.python.org/ftp/python/3.9.16/Python-3.9.16.tgz && \
    tar -xvf Python-3.9.16.tgz && \
    cd Python-3.9.16 && \
    ./configure --enable-optimizations --with-bz2 && \
    make altinstall

RUN python3.9 -V

# Install pip
RUN apt-get install -y python3-pip --fix-missing

# 设置工作目录
WORKDIR /app
RUN git clone --depth=1 https://github.com/kaixindelele/ChatPaper.git .
# 创建符号链接
RUN update-alternatives --install /usr/bin/python3 python3 /usr/local/bin/python3.9 1
# RUN ln -s /usr/local/bin/python3.9 /usr/bin/python
RUN pip3 install -r requirements.txt

# 进入scipdf_parser-master文件夹并安装依赖
WORKDIR /app/scipdf_parser-master
RUN pip3 install -r requirements.txt
RUN python3.9 setup.py install
RUN sed -i 's/\r$//' serve_grobid.sh

# 复制启动脚本到容器中
COPY start.sh /start.sh
RUN chmod +x /start.sh

# 启动应用
CMD ["/start.sh"]