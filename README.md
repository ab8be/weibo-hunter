<p align="center">
  <img src="https://img.shields.io/badge/Python-3.8%2B-blue" alt="Python 3.8+">
  <img src="https://img.shields.io/badge/Framework-Scrapy-green" alt="Scrapy">
  <img src="https://img.shields.io/badge/Output-CSV%20%7C%20MySQL%20%7C%20MongoDB%20%7C%20SQLite-orange" alt="Output">
</p>

<h1 align="center">Weibo Hunter</h1>

<p align="center"><strong>微博关键词搜索采集工具</strong></p>

<p align="center">
  连续获取微博搜索结果，支持时间范围、地区、内容类型等多维筛选，结果写入 CSV / MySQL / MongoDB / SQLite。
</p>

---

## 项目由来

本项目 fork 自 [dataabc/weibo-search](https://github.com/dataabc/weibo-search)，原作者为 [dataabc](https://github.com/dataabc)。原项目年久失修，多项功能已无法正常使用，恰好我自己有微博搜索采集的需求，就用 AI 辅助修了一遍，让它能重新跑起来。

**本项目中的核心爬虫逻辑、数据解析、分页策略等均来自原项目**，本人仅做了修复和适配工作。如果你觉得这个工具对你有帮助，请务必给[原仓库](https://github.com/dataabc/weibo-search)一个 Star。

## 功能一览

| 能力 | 说明 |
|:-----|:-----|
| 关键词搜索 | 支持多关键词、话题（`#话题#`）、关键词文件 |
| 时间范围 | 指定起止日期，精确到天 |
| 地区筛选 | 按省/直辖市筛选微博发布地 |
| 内容筛选 | 原创 / 热门 / 关注人 / 认证用户 / 媒体 / 观点 |
| 媒体筛选 | 全部 / 含图片 / 含视频 / 含音乐 / 含链接 |
| 自动细分 | 结果超 50 页时自动按小时、分钟拆分，确保采集完整 |
| 多种输出 | CSV（默认）、MySQL、MongoDB、SQLite |
| 媒体下载 | 可选下载微博图片和视频 |
| 进度断点 | Scrapy JOBDIR 支持断点续爬 |
| AI 友好 | 专用 CLI 入口 + 环境变量配置，详见 [AI_AGENT_GUIDE.md](docs/AI_AGENT_GUIDE.md) |

## 快速开始

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 配置 Cookie

不要把真实 Cookie 写进代码或提交到 Git。运行前设置环境变量 `WEIBO_COOKIE`：

<table>
<tr><td>PowerShell</td><td>

```powershell
$env:WEIBO_COOKIE = "你的微博Cookie"
```

</td></tr>
<tr><td>cmd</td><td>

```cmd
set WEIBO_COOKIE=你的微博Cookie
```

</td></tr>
<tr><td>Linux/macOS</td><td>

```bash
export WEIBO_COOKIE="你的微博Cookie"
```

</td></tr>
</table>

如果没有配置 Cookie，爬虫启动时会给出明确错误并停止。

<details>
<summary>如何获取 Cookie（点击展开）</summary>

1. 用 Chrome 打开 https://weibo.com/
2. 点击"立即登录"，完成验证，进入新版微博
3. 按 F12 打开开发者工具 → Network → Name → weibo.cn → Headers → Request Headers
4. 找到 `Cookie:` 后的值，复制即可

</details>

### 3. 配置搜索条件

编辑 `weibo/settings.py`：

```python
KEYWORD_LIST = ['迪丽热巴']     # 搜索关键词
START_DATE = '2020-03-01'       # 起始日期
END_DATE = '2020-03-01'         # 结束日期
WEIBO_TYPE = 1                  # 1=原创
CONTAIN_TYPE = 0                # 0=全部
REGION = ['全部']                # 地区筛选
LIMIT_RESULT = 0                # 结果数量限制，0=不限
```

`KEYWORD_LIST` 也支持文本文件路径（每行一个关键词）和话题写法 `#话题#`。

### 4. 运行

**推荐方式** — 使用脚本入口：

```bash
python scripts/collect_weibo.py \
  --keyword 迪丽热巴 \
  --start-date 2020-03-01 \
  --end-date 2020-03-01 \
  --limit 100
```

**直接 Scrapy：**

```bash
scrapy crawl search -s JOBDIR=crawls/search
```

## 输出字段

默认输出到 `结果文件/<关键词>/<关键词>.csv`（编码 `utf-8-sig`）：

| 字段 | 说明 |
|:-----|:-----|
| `id` | 微博 ID |
| `bid` | 微博 BID |
| `text` | 微博正文 |
| `article_url` | 头条文章 URL |
| `pics` | 图片 URL（多张逗号分隔） |
| `video_url` | 视频 URL（多个分号分隔） |
| `location` | 发布位置 |
| `created_at` | 发布时间 |
| `reposts_count` | 转发数 |
| `comments_count` | 评论数 |
| `attitudes_count` | 点赞数 |
| `source` | 发布工具 |
| `topics` | 话题 |
| `at_users` | @的用户 |
| `retweet_id` | 原始微博 ID（转发微博特有） |
| `user_id` | 发布者 ID |
| `screen_name` | 发布者昵称 |
| `user_authentication` | 用户类型（蓝V/黄V/红V/金V/普通用户） |

## 配置详解

### 微博类型（`WEIBO_TYPE`）

| 值 | 含义 |
|:--|:-----|
| 0 | 全部微博 |
| 1 | 原创微博 |
| 2 | 热门微博 |
| 3 | 关注人微博 |
| 4 | 认证用户微博 |
| 5 | 媒体微博 |
| 6 | 观点微博 |

### 内容筛选（`CONTAIN_TYPE`）

| 值 | 含义 |
|:--|:-----|
| 0 | 不筛选 |
| 1 | 含图片 |
| 2 | 含视频 |
| 3 | 含音乐 |
| 4 | 含链接 |

### 细分阈值（`FURTHER_THRESHOLD`）

当搜索结果达到 50 页时，程序自动按更细粒度拆分（天→小时→分钟）。阈值建议设为 **40–46**：太大可能漏数据，太小会拖慢速度。

```python
FURTHER_THRESHOLD = 46
```

### 等待时间（`DOWNLOAD_DELAY`）

两次请求之间的等待秒数，默认 10 秒：

```python
DOWNLOAD_DELAY = 10
```

### IP 属地（可选）

默认关闭，避免每条微博额外请求拖慢速度。如需开启：

```powershell
$env:WEIBO_FETCH_IP = "1"
```

### 数据库（可选）

在 `weibo/settings.py` 中取消注释并配置对应的 Pipeline 和连接信息即可启用 MySQL / MongoDB / SQLite。

## 本地验证

无需访问微博即可验证基础功能：

```bash
python -m scrapy list          # 确认 spider 可被发现
python -m pytest -q            # 运行测试
python scripts/collect_weibo.py --keyword 测试 --start-date 2020-01-01 --end-date 2020-01-01 --limit 5 --dry-run
```

## 本次修复内容

- 补齐 `requirements.txt` 中缺失的 Scrapy、requests、pytest 依赖
- Cookie 改为环境变量 `WEIBO_COOKIE` 读取，避免泄露
- Spider 配置加载从类定义移到实例初始化，便于测试
- 增加启动期校验：关键词、日期、Cookie 缺失会明确报错
- 修复分页 `meta` 传递，翻页不再丢失上下文
- 默认关闭 IP 属地同步请求，可选开启并增加超时处理
- 加强解析容错：缺字段跳过并记日志，不崩整次抓取
- 统一 `pics` 字段处理，修复 CSV/SQLite/MySQL 管道兼容
- 修复 SQLite 管道标志名不一致和异常后未返回 item
- Scrapy `-s` 命令行覆盖现在正确生效
- 删除调试输出，统一使用 Scrapy logger
- 新增 pytest 覆盖工具函数、解析、去重、CSV 输出等

## 致谢 & 许可

- 本项目 fork 自 [dataabc/weibo-search](https://github.com/dataabc/weibo-search)，感谢原作者 dataabc 的开源贡献
- **原项目未附带开源许可证**（仓库根目录无 LICENSE 文件，README 也未声明）。按 GitHub 默认版权规则，原代码著作权仍归属原作者 dataabc，本仓库仅作为个人修复和维护用途公开，不主张任何再许可或再分发权利
- 完整说明见 [`NOTICE`](NOTICE)
- 如原作者提出任何要求，本人会积极配合
