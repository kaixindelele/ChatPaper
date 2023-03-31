FROM continuumio/miniconda3:4.10.3-alpine

WORKDIR /opt/chatpaper

# Need the following line in mainland China
# COPY ./docker/tsinghua.condarc /root/.condarc

COPY ./docker/conda_env.yml /opt/chatpaper/conda_env.yml


RUN conda env create -f conda_env.yml && conda clean -afy
RUN rm -f conda_env.yml

# Need to separate the pip from conda env yaml so we can specify the mirror for mainland China
RUN conda run --no-capture-output --name chatpaper pip install --no-cache-dir urllib3==1.26.8 arxiv==1.4.3 Pillow==9.4.0 pybase64==1.2.3 tiktoken==0.2.0 tenacity==8.2.2 numpy==1.24.2 PyMuPDF==1.21.1 openai==0.27.0 bs4==0.0.1 python-dateutil==2.8.2  openpyxl PyYAML==5.4.1 pytz==2022.05 retry -i https://pypi.tuna.tsinghua.edu.cn/simple

COPY . .

RUN rm -rf images export pdf_files

ENV NUM_PROCESS=2
ENV NUM_THREAD=2
ENV TIME_OUT=1800


CMD conda run --no-capture-output --name chatpaper uwsgi \
    --http 0.0.0.0:8088 \
    --uid root \
    --enable-threads \
    --lazy \
    --processes $NUM_PROCESS\
    --threads $NUM_THREAD \
    --logto /var/log/chatpaper.log \
    --protocol uwsgi \
    --http-timeout $TIME_OUT \
    --harakiri $TIME_OUT \
    --wsgi app:app