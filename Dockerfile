# 使用包含Java 11环境的官方AdoptOpenJDK镜像作为基础镜像
FROM adoptopenjdk:11-jre-hotspot-bionic

# 设置工作目录
WORKDIR /app

# 克隆GitHub仓库
RUN apt-get update
RUN apt-get install -y git
# 下载和安装 Python 3.9
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
    wget \
    build-essential \
    zlib1g-dev \
    libncurses5-dev \
    libgdbm-dev \
    libnss3-dev \
    libssl-dev \
    libreadline-dev \
    libffi-dev \
    && wget https://www.python.org/ftp/python/3.9.16/Python-3.9.16.tgz \
    && tar -xvf Python-3.9.16.tgz \
    && cd Python-3.9.16 \
    && ./configure --enable-optimizations \
    && make altinstall \
    && cd .. \
    && rm -rf Python-3.9.16 \
    && rm Python-3.9.16.tgz \
    && apt-get remove -y \
    wget \
    build-essential \
    zlib1g-dev \
    libncurses5-dev \
    libgdbm-dev \
    libnss3-dev \
    libssl-dev \
    libreadline-dev \
    libffi-dev \
    && rm -rf /var/lib/apt/lists/*

# COPY start.sh /app/start.sh
RUN rm -rf * && git clone https://github.com/kaixindelele/ChatPaper.git .

# 安装Python依赖
# 基于Debian或Ubuntu的Docker镜像
RUN apt-get update && \
    apt-get install -y python3-pip

# Check Python version
RUN python3.9 --version && sleep 10

RUN pip3 install --no-cache-dir -r requirements.txt

# 进入scipdf_parser-master文件夹并安装依赖
WORKDIR /app/scipdf_parser-master
RUN pip3 install --no-cache-dir -r requirements.txt

# 检查Java版本
RUN java -version

# 复制启动脚本到容器中
COPY start.sh /start.sh
RUN chmod +x /start.sh

# 启动应用
CMD ["/start.sh"]