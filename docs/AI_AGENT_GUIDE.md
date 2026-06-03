# AI Agent Guide

> 面向 Claude Code、Codex、Cursor、Copilot 等 AI 工具的使用指南。
> 本文档的目标是让 AI 在 **无需人类干预** 的情况下完成一次完整的微博搜索采集。

## 这个项目是什么

一个基于 Scrapy 的微博搜索爬虫。给定关键词和时间范围，从 `s.weibo.com` 采集微博帖子，输出 CSV 文件。

**人类 = 原作者 dataabc**，本项目 fork 自 [dataabc/weibo-search](https://github.com/dataabc/weibo-search)，仅做修复适配。

## 前置条件

| 条件 | 说明 |
|:-----|:-----|
| Python 3.8+ | 运行环境 |
| 有效的微博 Cookie | 通过 `WEIBO_COOKIE` 环境变量提供 |
| 网络访问 | 需能访问 `s.weibo.com` |

## 项目结构（30 秒定位）

```
weibo-hunter/
├── scripts/
│   └── collect_weibo.py      ← 【主入口】AI 优先使用这个
├── weibo/
│   ├── settings.py            ← 运行时配置（环境变量优先）
│   ├── items.py               ← 数据字段定义
│   ├── pipelines.py           ← CSV/MySQL/MongoDB/SQLite 管道
│   ├── spiders/
│   │   └── search.py          ← 爬虫核心：请求构造 + 页面解析
│   └── utils/
│       └── region.py          ← 地区名称映射
├── tests/                     ← pytest 测试
├── docs/
│   ├── AI_AGENT_GUIDE.md      ← 你正在读的这个文件
│   └── COLLECTION_CONTRACT.md ← 输入输出契约（机器可读）
└── requirements.txt
```

## 快速操作流程

### 第一步：验证环境

```bash
python -m scrapy list
python -m pytest -q
```

两个命令都通过，说明环境 OK。

### 第二步：设置 Cookie

```bash
# Linux/macOS
export WEIBO_COOKIE="从浏览器复制的完整 Cookie 字符串"

# PowerShell
$env:WEIBO_COOKIE = "从浏览器复制的完整 Cookie 字符串"
```

**绝对不要**把 Cookie 写进 `weibo/settings.py` 或任何会被 git 跟踪的文件。

### 第三步：执行采集

```bash
python scripts/collect_weibo.py \
  --keyword 迪丽热巴 \
  --start-date 2020-03-01 \
  --end-date 2020-03-01 \
  --limit 100
```

### 第四步：确认结果

```bash
# 检查输出文件是否存在
ls "结果文件/迪丽热巴/迪丽热巴.csv"

# 查看前几行
head -5 "结果文件/迪丽热巴/迪丽热巴.csv"
```

成功标志：
- 命令退出码为 `0`
- CSV 文件存在且非空
- 第一行为表头，后续行为数据

## CLI 参数完整参考

```
python scripts/collect_weibo.py [OPTIONS]
```

| 参数 | 必填 | 默认值 | 说明 |
|:-----|:-----|:-------|:-----|
| `--keyword` | 是* | — | 搜索关键词，可重复指定多个 |
| `--keywords-file` | 是* | — | 关键词文件路径（每行一个） |
| `--start-date` | 是 | — | 起始日期 `yyyy-mm-dd`（含） |
| `--end-date` | 是 | — | 结束日期 `yyyy-mm-dd`（含） |
| `--limit` | 否 | 20 | 最大采集条数，`0` 不限 |
| `--weibo-type` | 否 | 1 | 0全部 1原创 2热门 3关注 4认证 5媒体 6观点 |
| `--contain-type` | 否 | 0 | 0全部 1图片 2视频 3音乐 4链接 |
| `--region` | 否 | 全部 | 地区筛选，可重复 |
| `--download-delay` | 否 | 1.0 | 请求间隔秒数 |
| `--log-level` | 否 | INFO | DEBUG/INFO/WARNING/ERROR/CRITICAL |
| `--jobdir` | 否 | — | 断点续爬目录 |
| `--dry-run` | 否 | — | 只打印命令不执行，用于验证 |

> `--keyword` 和 `--keywords-file` 至少提供一个。

## 环境变量参考

| 变量名 | 用途 | 示例值 |
|:-------|:-----|:-------|
| `WEIBO_COOKIE` | 微博登录 Cookie（必须） | 浏览器中复制 |
| `WEIBO_KEYWORDS` | JSON 数组或逗号分隔 | `["迪丽热巴","杨幂"]` |
| `WEIBO_START_DATE` | 起始日期 | `2020-03-01` |
| `WEIBO_END_DATE` | 结束日期 | `2020-03-02` |
| `WEIBO_LIMIT_RESULT` | 最大条数 | `100` |
| `WEIBO_TYPE` | 微博类型 | `1` |
| `WEIBO_CONTAIN_TYPE` | 内容筛选 | `0` |
| `WEIBO_REGION` | 地区（JSON 或逗号分隔） | `["北京","上海"]` |
| `WEIBO_FETCH_IP` | 补充 IP 属地 | `0` 或 `1` |

> 使用 `scripts/collect_weibo.py` 时，CLI 参数会自动设置对应的环境变量，无需手动配置。

## 输出格式

CSV 文件路径：`结果文件/<关键词>/<关键词>.csv`

编码：`utf-8-sig`（Excel 兼容）

每条记录的字段：

```python
{
    "id": "微博ID",
    "bid": "微博BID",
    "user_id": "用户ID",
    "screen_name": "用户昵称",
    "text": "微博正文",
    "article_url": "头条文章URL",
    "location": "发布位置",
    "at_users": "@用户",
    "topics": "话题",
    "reposts_count": "转发数",
    "comments_count": "评论数",
    "attitudes_count": "点赞数",
    "created_at": "发布时间",
    "source": "发布工具",
    "pics": "图片URL列表",
    "video_url": "视频URL",
    "retweet_id": "原始微博ID",
    "ip": "IP属地",
    "user_authentication": "用户认证类型",
    "vip_type": "会员类型",
    "vip_level": "会员等级"
}
```

## 常见工作流

### 工作流 1：采集单个关键词

```bash
export WEIBO_COOKIE="你的Cookie"
python scripts/collect_weibo.py \
  --keyword 人工智能 \
  --start-date 2024-01-01 \
  --end-date 2024-01-31 \
  --limit 500
```

### 工作流 2：采集多个关键词

```bash
python scripts/collect_weibo.py \
  --keyword 迪丽热巴 \
  --keyword 杨幂 \
  --start-date 2024-01-01 \
  --end-date 2024-01-01 \
  --limit 100
```

### 工作流 3：使用关键词文件

```bash
# 创建关键词文件
echo -e "人工智能\nChatGPT\n大模型" > keywords.txt

python scripts/collect_weibo.py \
  --keywords-file keywords.txt \
  --start-date 2024-01-01 \
  --end-date 2024-01-31 \
  --limit 200
```

### 工作流 4：筛选特定地区的原创微博

```bash
python scripts/collect_weibo.py \
  --keyword 美食 \
  --start-date 2024-06-01 \
  --end-date 2024-06-01 \
  --region 北京 \
  --weibo-type 1 \
  --limit 50
```

### 工作流 5：断点续爬

```bash
# 首次运行，Ctrl+C 停止后进度保存在 crawls/food 目录
python scripts/collect_weibo.py \
  --keyword 美食 \
  --start-date 2024-01-01 \
  --end-date 2024-12-31 \
  --limit 0 \
  --jobdir crawls/food

# 恢复爬取
python scripts/collect_weibo.py \
  --keyword 美食 \
  --start-date 2024-01-01 \
  --end-date 2024-12-31 \
  --limit 0 \
  --jobdir crawls/food
```

### 工作流 6：Dry-run 验证（不实际采集）

```bash
python scripts/collect_weibo.py \
  --keyword 测试 \
  --start-date 2020-01-01 \
  --end-date 2020-01-01 \
  --limit 5 \
  --dry-run
```

输出示例：
```
COMMAND=python -m scrapy crawl search -s LIMIT_RESULT=5 ...
ENV={"WEIBO_KEYWORDS":"[\"测试\"]","WEIBO_START_DATE":"2020-01-01",...}
COOKIE_PRESENT=true
```

## 错误排查

| 错误现象 | 原因 | 解决方法 |
|:---------|:-----|:---------|
| `WEIBO_COOKIE is empty` | 未设置环境变量 | 设置 `WEIBO_COOKIE` |
| 采集 0 条结果 | Cookie 过期 | 从浏览器重新获取 Cookie |
| 采集 0 条结果（Cookie 有效） | 筛选条件无匹配 | 调整关键词/日期/类型/地区 |
| 请求被拦截/频繁 | 请求过快 | 增大 `--download-delay` |
| 页面解析失败 | 微博页面改版 | 更新 `weibo/spiders/search.py` 中的选择器 |
| `ModuleNotFoundError` | 依赖未安装 | `pip install -r requirements.txt` |

## AI 行为规范

如果你是 AI agent，在操作本仓库时请遵守：

1. **不要**将 Cookie 写入任何文件或 git 提交
2. **不要**将 `结果文件/` 和 `crawls/` 目录提交到 git
3. 修改解析逻辑后，运行 `python -m pytest -q` 确保测试通过
4. 修改 spider 或 pipeline 后，运行 `--dry-run` 验证
5. 每次采集都设置 `--limit`，除非用户明确要求不限量
6. 采集完成后向用户报告：关键词、时间范围、实际条数、输出路径
