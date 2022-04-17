# QTBridge
将 QQ 和 Telegram 群消息互相转发的轻量级机器人。

QQ 部分采用 [go-cqhttp](https://github.com/Mrs4s/go-cqhttp) 进行通信。

由于 Telegram 的 webhook 实现需要使用 https，考虑到通用性，故采用轮询的方式获取消息。考虑到一致性，QQ 部分也采用此方式。

## 运行
```
git clone <Placeholder>
docker run <Placeholder>
```

## Telegram 代理设置

## 添加关联群聊