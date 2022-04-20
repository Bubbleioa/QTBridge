## TODO

没有打算按照 onebot11 文档中提到的 通过 `.handle-quick_opeartion` API伪造快速操作，而是在接收到上报后重新调用 API 实现转发。

`event.message.format` where to config?

## 模块介绍

借鉴了别人写法，待修改（等我把逻辑理清楚了再往异步和框架里套55）

- `ini` : initialize module
- `receive` : receive message and wrap into json file
- `api` 
    - `send_msg` : receive response dictionary and send corresponding message
    - `send_item` : wrap special item into message form
- `bot` 
    - wrap received message (need wrap form)
    - forward wrapped message into qq group