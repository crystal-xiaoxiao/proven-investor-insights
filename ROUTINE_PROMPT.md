# Routine prompt（复制下面横线以下的全部内容到 claude.ai/code/routines 的 Instructions 框）

---

你在仓库 proven-investor-insights 里工作。这是一个 GitHub Pages 静态站点，页面 index.html 读取 data.json。你的任务是每两周更新一次 data.json，记录 10 位投资人在观察窗口内的公开发言。先读仓库根目录的 CLAUDE.md，里面有数据结构、写作规则和完整流程；本 prompt 是它的摘要，冲突时以 CLAUDE.md 为准。

第一步，判断是否需要运行：读 data.json 的 meta.last_updated。如果距今天不足 12 天，输出一句"距上次更新不足 12 天，本次跳过"，然后结束，不修改任何文件，不提交。

第二步，归档：运行 python3 scripts/archive.py。

第三步，检索。观察窗口 = 上一期 window_end 的次日到今天。对下列 10 位投资人逐一检索窗口内的公开发言（播客、X 帖子、Substack、媒体专访、财报会或股东会发言、会议演讲）。起点是 data.json 里每人的 sources[]，再用通用网络搜索补充。除徐新用中文检索外，其他人一律用英文检索。

- Vinod Khosla（Khosla Ventures）
- Brad Gerstner（Altimeter；BG2 Pod 是主要渠道）
- Gavin Baker（Atreides）
- Elad Gil（No Priors 播客、Elad Blog）
- Marc Andreessen（a16z、pmarca Substack）
- Philippe Laffont（Coatue；EMW 报告、专访）
- Josh Kushner（Thrive；公开发言极少）
- 孙正义（SoftBank 财报会、股东会、SoftBank World）
- 徐新（今日资本；演讲和专访，中文检索）
- Alex Sacerdote（Whale Rock；公开发言极少）

第四步，写入 data.json。每位投资人的 latest[] 整体替换为本期内容，每条含 date、source_type、source_label、url、headline、points[]，可选 original 和 topics[]。规则：
- 只写他们自己说过的话，每条必须有可打开的 https 出处链接。
- 窗口内找不到某人的公开发言就让 latest 为空数组。这是正确结果，不要为了填满而写背景或旧发言。
- 转述保留具体数字、公司名、时间判断和方向（看多 / 看空 / 观望）。
- 同一次播客或访谈合并成一条，points 里列 2–4 个要点。每人最多 5 条，按重要性排序。
- 更新 meta：last_updated 和 window_end 写今天，window_start 写上一期 window_end 的次日，period_summary 用 3–5 句只写本期窗口内的变化（谁的方向变了、谁新提了什么公司或主题、谁明确看空了什么），不写背景，不写"值得关注"。
- track_record 不动。sources 只在发现新的稳定渠道时追加。

第五步，校验：运行 python3 scripts/validate.py --strict。不通过就修正 data.json 再跑，直到通过。修不好就不要提交，把问题写在最终输出里。

第六步，提交：git add data.json history/ 然后 commit，信息格式 "update: <window_start>..<window_end>"，直接 push 到 main。不要开分支，不要开 PR，不要改 index.html 和 scripts/。

最终输出：一段简短的运行说明——本期窗口、每位投资人找到几条、跳过谁及原因、commit hash。如果检索中有网络被拦截或页面打不开的情况，列出来。
