FROM alpine:3.13
WORKDIR /usr/src/app

RUN apk update && apk add tzdata

COPY . .

CMD [ "./go-cqhttp" ]