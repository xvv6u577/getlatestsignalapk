## 下载最新版 signal 的 web 服务，用 Flask 实现

- 可以下载 android 版，windows 版，mac 版的 signal。
- 2 种方式：从官网直接下载，或者通过中转（detour）服务器下载

### 环境

- 18.04.4 LTS
- Python 3.7.4
- pip 19.3.1

### 安装 & 运行

```
git clone git@github.com:caster8013/getlatestsignalapk.git
cd getlatestsignalapk

sudo apt update
sudo apt install software-properties-common
sudo add-apt-repository ppa:deadsnakes/ppa
sudo apt install python3.7 python3.7-dev
python3.7 -m venv venv
. venv/bin/activate

pip install -r requirement.txt

sudo cp ./getsignal.service /etc/systemd/system/

sudo systemctl start getsignal
sudo systemctl enable getsignal
sudo systemctl status getsignal


```

添加到 nginx 配置文件，/etc/nginx/sites-available/get.conf

```
server {
    listen 80;
    server_name your_domain www.your_domain;

    location ~ ^/(index|apk|mac|win) {
        include uwsgi_params;
        uwsgi_pass unix:/home/ubuntu/getlatestsignalapk/getsignal.sock;
    }
}
```

测试 nginx 配置文件，重新加载配置文件

```
sudo nginx -t
sudo nginx -s reload
```

### License

Under [GPLv3](https://www.gnu.org/licenses/gpl-3.0.html)
