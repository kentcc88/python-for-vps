import paramiko

servers = [

    {"name": "美国", "hostname": "1.1.1.1", "port": 22, "username": "root", "password": "123456"},   
    {"name": "不丹", "hostname": "1.1.1.1", "port": 22, "username": "root", "password": "123456"},   
    {"name": "毛里求斯", "hostname": "1.1.1.1", "port": 22, "username": "root", "password": "123456"},   
    # 添加更多服务器

]


# 定义更新操作
def update_server(name, hostname, port, username, password):
    try:

        # 连接服务器
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(hostname, port=port, username=username, password=password)


        print(f" {name} 更新系统")
        stdin, stdout, stderr = client.exec_command("apt update -y  && apt upgrade -y && apt install -y curl wget sudo socat unzip tar htop")
        
        print(f"正在更新:")
        while not stdout.channel.exit_status_ready():
            if stdout.channel.recv_ready():
                print(stdout.channel.recv(1024).decode(), end="")

        # 检查执行状态
        if stderr.channel.recv_exit_status() == 0:
            print(f"更新成功")
        else:
            print(f"更新失败")
        
        print()

        print(f"{name} 安装 Docker")
        stdin, stdout, stderr = client.exec_command("curl -fsSL https://get.docker.com | sh")

        print(f"正在安装 Docker:")
        while not stdout.channel.exit_status_ready():
            if stdout.channel.recv_ready():
                print(stdout.channel.recv(1024).decode(), end="")

        # 检查执行状态
        if stderr.channel.recv_exit_status() == 0:
            print(f"安装 Docker 成功")
        else:
            print(f"安装 Docker 失败")

        print()

        print(f"{name} 安装 Docker Compose")
        stdin, stdout, stderr = client.exec_command('curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose && chmod +x /usr/local/bin/docker-compose')

        print(f"正在安装 Docker Compose:")
        while not stdout.channel.exit_status_ready():
            if stdout.channel.recv_ready():
                print(stdout.channel.recv(1024).decode(), end="")

        # 检查执行状态
        if stderr.channel.recv_exit_status() == 0:
            print(f"安装 Docker Compose 成功")
        else:
            print(f"安装 Docker Compose 失败")

        print()


        print(f"{name} 创建web目录")
        stdin, stdout, stderr = client.exec_command("cd /home && mkdir -p web/html web/mysql web/certs web/conf.d web/redis && touch web/docker-compose.yml")

        while not stdout.channel.exit_status_ready():
            if stdout.channel.recv_ready():
                print(stdout.channel.recv(1024).decode(), end="")

        # 检查执行状态
        if stderr.channel.recv_exit_status() == 0:
            print(f"创建目录成功")
        else:
            print(f"创建目录失败")

        print()

        print(f"{name} 配置docker-compose.yml")
        stdin, stdout, stderr = client.exec_command('wget -O /home/web/docker-compose.yml https://raw.githubusercontent.com/kejilion/docker/main/LNMP-docker-compose-4.yml')
        while not stdout.channel.exit_status_ready():
            if stdout.channel.recv_ready():
                print(stdout.channel.recv(1024).decode(), end="")

        # 检查执行状态
        if stderr.channel.recv_exit_status() == 0:
            print(f"配置成功")
        else:
            print(f"配置失败")

        print()

        print(f"{name} 启动环境")
        stdin, stdout, stderr = client.exec_command('cd /home/web && docker-compose up -d')
        print(f"启动中:")
        while not stdout.channel.exit_status_ready():
            if stdout.channel.recv_ready():
                print(stdout.channel.recv(1024).decode(), end="")

        # 检查执行状态
        if stderr.channel.recv_exit_status() == 0:
            print(f"启动成功")
        else:
            print(f"启动失败")

        print()

        print(f"{name} 安装PHP扩展配置参数")

        command = (
            "docker exec php apt update && "
            "docker exec php apt install -y libmariadb-dev-compat libmariadb-dev libzip-dev libmagickwand-dev imagemagick && "
            "docker exec php docker-php-ext-install mysqli pdo_mysql zip exif gd intl bcmath opcache && "
            "docker exec php pecl install imagick && "
            "docker exec php sh -c 'echo \"extension=imagick.so\" > /usr/local/etc/php/conf.d/imagick.ini' && "
            "docker exec php pecl install redis && "
            "docker exec php sh -c 'echo \"extension=redis.so\" > /usr/local/etc/php/conf.d/docker-php-ext-redis.ini'"
        )

        stdin, stdout, stderr = client.exec_command(command)

        while not stdout.channel.exit_status_ready():
            if stdout.channel.recv_ready():
                print(stdout.channel.recv(1024).decode(), end="")

        # 检查执行状态
        if stderr.channel.recv_exit_status() == 0:
            print(f"安装成功")
        else:
            print(f"安装失败")

        print()

        print(f"{name} 安装php74扩展配置参数")

        command = (
            "docker exec php74 apt update && "
            "docker exec php74 apt install -y libmariadb-dev-compat libmariadb-dev libzip-dev libmagickwand-dev imagemagick && "
            "docker exec php74 docker-php-ext-install mysqli pdo_mysql zip gd intl bcmath opcache && "
            "docker exec php74 pecl install imagick && "
            "docker exec php74 sh -c 'echo \"extension=imagick.so\" > /usr/local/etc/php/conf.d/imagick.ini' && "
            "docker exec php74 pecl install redis && "
            "docker exec php74 sh -c 'echo \"extension=redis.so\" > /usr/local/etc/php/conf.d/docker-php-ext-redis.ini'"
        )

        stdin, stdout, stderr = client.exec_command(command)

        while not stdout.channel.exit_status_ready():
            if stdout.channel.recv_ready():
                print(stdout.channel.recv(1024).decode(), end="")

        # 检查执行状态
        if stderr.channel.recv_exit_status() == 0:
            print(f"安装成功")
        else:
            print(f"安装失败")

        print()


        print(f"{name} 重启PHP")
        stdin, stdout, stderr = client.exec_command('docker restart php && docker restart php74')
        while not stdout.channel.exit_status_ready():
            if stdout.channel.recv_ready():
                print(stdout.channel.recv(1024).decode(), end="")

        # 检查执行状态
        if stderr.channel.recv_exit_status() == 0:
            print(f"搭建完成")
        else:
            print(f"搭建失败")

        print()

        print()
        print()

        # 关闭 SSH 连接
        client.close()


    except Exception as e:
        print(f"连接 {name} 失败")


# 遍历服务器列表，逐一更新
for server in servers:
    name = server["name"]
    hostname = server["hostname"]
    port = server["port"]
    username = server["username"]
    password = server["password"]
    update_server(name, hostname, port, username, password)

# 等待用户按下任意键后关闭窗口
input("按任意键关闭窗口...")


