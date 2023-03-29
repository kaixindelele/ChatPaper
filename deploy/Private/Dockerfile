FROM python:3.9

WORKDIR /usr/src/app 

RUN apt-get update && apt-get install -y gcc

RUN apt-get install -y curl && curl https://sh.rustup.rs -sSf | sh -s -- -y

ENV PATH="/root/.cargo/bin:${PATH}"

COPY requirements.txt ./ 

RUN pip install --no-cache-dir -r requirements.txt 

EXPOSE 7860

COPY . . 

CMD [ "python", "app.py" ] 