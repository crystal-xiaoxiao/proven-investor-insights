# Proven Investor Insights — 仓库说明

这个仓库是一个静态 GitHub Pages 站点：`index.html` 读取 `data.json` 渲染页面。定时 Routine 每两周更新一次 `data.json`，其余文件不动。

## 文件

- `data.json` — 唯一的数据文件。Routine 只改这个文件（以及归档产生的 `history/`）。
- `index.html` — 页面。不要在更新数据时改它。
- `history/` — 往期快照。`scripts/archive.py` 自动维护，不要手工编辑。
- `scripts/archive.py` — 更新前先运行，把当前期归档。
- `scripts/validate.py` — 提交前必须通过。

## 目标

追踪 10 位「多次押中科技浪潮赢家」的投资人在观察窗口内的公开发言（播客、X、Substack、媒体专访、财报会 / 股东会），记录他们**自己说了什么**，作为研究方向的参考。

## data.json 结构

```
meta
  last_updated     本次更新日期 YYYY-MM-DD
  window_start     观察窗口起点（= 上一期 window_end 的次日）
  window_end       观察窗口终点（= 今天）
  period_summary   本期摘要，3–5 句
  notice           页面底部备注，一般不改
waves[]            浪潮定义，不改
investors[]        10 位投资人，顺序和 id 不改
  sources[]        该投资人的公开渠道，作为检索起点；发现新的稳定渠道可以追加
  latest[]         本期观点（每次更新整体替换，不追加旧的）
    date           发言日期 YYYY-MM-DD，必须在观察窗口内（前后 3 天容忍）
    source_type    podcast / x / substack / media / earnings / conference
    source_label   来源名称，如 "BG2 Pod E112"、"X 帖子"、"Bloomberg 专访"
    url            原始出处链接，必填，https
    headline       一句话概括这条观点（中文，≤ 40 字）
    points[]       2–4 条，他实际说的内容（中文转述，保留具体数字、公司名、时间判断）
    original       可选，一句最关键的英文原话（≤ 30 词）
    topics[]       可选，1–3 个标签，如 "AI 资本开支"、"推理成本"、"能源"
  track_record[]   过往业绩记录。日常更新不改；只有投资人本人公开确认了新的重大押注才追加一条
```

## 写作规则（必须遵守）

1. **只写投资人自己说过的话。** 每一条 `latest` 都要有可点开的 `url`。没有出处的观点不写。
2. **不做事后叙事，不做推演，不补写。** 观察窗口内找不到某位投资人的公开发言，就让 `latest` 为空数组，页面会显示「本期无新增」。这是正确结果，不是失败。
3. **转述要保留具体性**：数字、公司名、时间判断、方向词（看多 / 看空 / 观望）都要留下。不要压缩成"他看好 AI"。
4. **一条发言只记一次。** 同一次播客里的多个观点合并到一个 `latest` 项的 `points` 里，不要拆成多条。
5. **一位投资人一期最多 5 条**，按重要性排序。
6. **`period_summary` 只写本期窗口内的变化**：谁的方向变了、谁新提了什么公司或主题、谁明确看空了什么。不写背景介绍，不写"值得关注"。
7. 二手报道（"据报道 X 表示…"）可以用，但 `url` 要指向报道本身，`source_label` 写清是转述，并优先寻找原始录音 / 帖子替换。
8. 检索语言：所有投资人用英文检索；只有徐新用中文检索。
9. `track_record` 默认不动。

## 更新流程

```
1. 读 data.json 的 meta.last_updated；距今不足 12 天 → 直接结束，不做任何改动，不提交。
2. python3 scripts/archive.py           # 归档当前期
3. 逐位投资人检索观察窗口内的公开发言（起点是 sources[]，再用通用搜索补充）
4. 重写 data.json：更新 meta（last_updated / window_start / window_end / period_summary）和每位投资人的 latest[]
5. python3 scripts/validate.py --strict  # 不通过就修，修不好就不要提交
6. git add data.json history/ && git commit -m "update: <window_start>..<window_end>" && git push origin main
```

提交直接推到 `main`，GitHub Pages 会自动部署。不要开分支，不要开 PR。
