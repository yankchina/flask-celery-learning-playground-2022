# 学习笔记

## 技术要点

## 文件目录架构

- `docker-compose.yml` 启动整个系统的 `docker` 配置文件，该系统有多个镜像，其中包含了
  - `worker` 容器，就是 `website` 镜像
  - `game-server` 容器
  - `radis` 容器，其用于消息管理
  - `mongo` 容器，非对象数据库存储

### `website` 目录

- `.dockerignore` 建立镜像的忽略配置
- `config.py` 系统的配置类
- `Dockerfile` 镜像生成脚本
- `init_celery.py` 初始化 `celery` 服务，？为什么要初始化
- `requirements.txt` 安装必备的第三方 python 库
- `run_celery.py` 启动 `celery` 服务，? 与 `init_celery.py` 有什么不同
- `website.py` 系统主程序
- `wsgi.py` 第三方 `wsgi` 服务器启动的入口程序，其实就是 -> `website.py` 中的 `app` 函数。
  - 从 `requirements.txt` 中分析可知其用的是 `gunicorn` 作为 `wsgi` 服务器

#### `app` 目录

这是主程序目录，其采用 `flask` 的现代结构来组织文件

文件列表如下:

- `__init__.py` python 模块入口文件
- `log.log` 日志文件

子目录列表如下:

- `blueprints` 蓝图目录，其中存储不同模块的类
- `helpers` 帮助函数目录，存储全局函数
- `models` 模型类目录
- `static` 静态文件目录
- `templates` 渲染模块文件目录

#### `tests`目录


### `game-server` 目录