# 上线步骤

只有前两步和第四步需要你亲自操作，其余是核对。全程大约 15 分钟。

## 1. 建仓库并推上去（在 Claude Code CLI 里做，2 分钟）

把整个 `proven-investor-insights` 文件夹放到本地，然后在该目录下：

```bash
git init -b main
git add .
git commit -m "scaffold: static page + data.json + routine scripts"
gh repo create proven-investor-insights --public --source . --push
```

仓库设为 public：页面本来就是要给组织外的人看的，public 仓库的 Pages 也不需要付费 GitHub 计划。`index.html` 已加 `noindex`，搜索引擎不会收录。

注意 `main` 分支不要开 branch protection——Routine 需要直接推 main。

## 2. 打开 GitHub Pages（1 分钟）

仓库 Settings → Pages → Build and deployment：Source 选 "Deploy from a branch"，Branch 选 `main` / `(root)`，Save。

一两分钟后页面地址是：`https://<你的 GitHub 用户名>.github.io/proven-investor-insights/`

这就是可以直接发给任何人的固定链接。先打开确认能看到首期基线（10 位投资人、"本期无新增"、过往业绩记录表）。

## 3. 给 Claude Code 仓库访问权（2 分钟）

打开 https://claude.ai/code，如果还没连 GitHub，按提示安装 Claude GitHub App，并勾选 `proven-investor-insights` 这个仓库。

## 4. 创建 Routine（5 分钟）

打开 https://claude.ai/code/routines → New routine：

| 项目 | 填什么 |
|---|---|
| Name | Proven Investor Insights 双周更新 |
| Instructions | 粘贴 `ROUTINE_PROMPT.md` 横线以下的全部内容 |
| Model | 选最强的那档（检索质量比速度重要） |
| Repositories | `proven-investor-insights` |
| Environment | 新建一个，命名 `research-full`，Network access 选 **Full**（默认 Trusted 只放行包管理器等白名单，抓 Substack、X、播客页会被 403） |
| Trigger | Schedule → Weekly，周一早上（按你本地时间填，比如 06:00） |
| Connectors | 全部移除。这个任务只需要网络和 git，不需要 Gmail / Notion / Drive |

点 Create。

为什么选 Weekly 而不是两周：表单预设只有 hourly / daily / weekdays / weekly。prompt 第一步已经做了"距上次更新不足 12 天就跳过"的判断，所以每周触发、实际每两周执行一次，多出来的那次只消耗读一个文件的量。如果想精确到双周，之后可以在 CLI 里 `/schedule update` 设 cron（比如每月 1 号和 15 号），但那需要 CLI 用 claude.ai 账号登录，你现在是 API key，要先去掉 `ANTHROPIC_API_KEY` 再 `/login`。不急的话就用 Weekly。

## 5. 手动跑第一次（等 10–20 分钟）

在 Routine 详情页点 **Run now**。运行结束后：

- 打开那次 session，看最终输出：每位投资人找到几条、有没有网络拦截。
- 去仓库看 `main` 上多了一个 `update: ...` 的 commit，`data.json` 里 `latest[]` 有内容。
- 刷新 Pages 地址，"本期观点" 里应该有第一期内容，"往期" 还是空的（第二次更新后才会出现）。

绿色状态只代表 session 正常退出，不代表任务成功，一定要打开看一眼输出。

## 6. 之后

- 把 Pages 链接发出去即可，不再需要在 Claude 里点 Share 或切版本。
- 用量计入你的订阅额度，每天的 routine 运行次数上限远高于这里的用量。
- 想改追踪名单或页面：直接改 `data.json` / `index.html` 推到 main；或者在 Claude Code 里说"改一下 proven-investor-insights 的页面"。
- `data.json` 里的过往业绩记录是种子数据，把 Cowork artifact 里已核实的版本贴回去替换即可（结构见 CLAUDE.md）。
- 现在那个 Cowork artifact 可以留着当内部版本，也可以停掉那个 Cowork scheduled task，避免两边各跑一份。
