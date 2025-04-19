#!/bin/bash

# 启动 SSH 服务
service ssh start

# 保持容器运行状态
tail -f /dev/null
