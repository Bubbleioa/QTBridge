FROM python:3.10.2-alpine3.15
WORKDIR /usr/src/app

RUN apk update && apk add tzdata

COPY . .

RUN pip install --no-cache-dir -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

RUN apk del build-dependencies

CMD [ "python", "main.py" ]
