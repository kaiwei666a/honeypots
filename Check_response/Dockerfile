FROM ubuntu:22.04

# 安装 openssh-server 和其他基本工具
RUN apt-get update && apt-get install -y openssh-server sudo vim net-tools

# 创建 sshd 运行目录
RUN mkdir /var/run/sshd

# 设置 root 密码
RUN echo 'root:rootpassword' | chpasswd

# 允许 root 用户通过 SSH 登录（默认禁用）
RUN sed -i 's/#PermitRootLogin prohibit-password/PermitRootLogin yes/' /etc/ssh/sshd_config

# 允许密码认证
RUN sed -i 's/#PasswordAuthentication yes/PasswordAuthentication yes/' /etc/ssh/sshd_config

# 启动脚本
COPY setup.sh /setup.sh
RUN chmod +x /setup.sh

EXPOSE 22

CMD ["/setup.sh"]
