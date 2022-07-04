FROM python:3.10.2-alpine3.15
WORKDIR /usr/src/app
ENV isdocker=1
RUN echo -e http://mirrors.ustc.edu.cn/alpine/v3.15/main/ > /etc/apk/repositories

RUN apk update && apk add tzdata

COPY . .

RUN pip install --no-cache-dir -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

CMD [ "python", "main.py" ]
