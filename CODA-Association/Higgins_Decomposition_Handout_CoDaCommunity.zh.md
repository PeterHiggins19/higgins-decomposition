# HIGGINS DECOMPOSITION (Hˢ) — 中文版（简体）

> **翻译状态：草稿 — 等待中文母语专家审校。** 依据 `HCI-CNQ/wrappers/WRAPPER_SCHEMA.md §11.1`。英文版本（`Higgins_Decomposition_Handout_CoDaCommunity.md`）为规范文本；如有歧义以英文为准。目标语域：科学普通话（简体中文）。

---

**组分数据分析的运维化 —— 面向研究者及其所选 AI 助手的可执行标准**

*"单纯形上的能源结构漂移之组分监测"*
**CoDaWork 2026 · 葡萄牙·科英布拉 · 6 月 1–5 日**
Peter Higgins · Rogue Wave Audio / Binaural Test Lab · 加拿大·安大略省·马卡姆

---

## 关键数字

| 11 | 101 | 44 | 3 | 22 + 66 | ~220 |
|:--:|:--:|:--:|:--:|:--:|:--:|
| 已验证领域 | 参考数据集 | 跨越数量级 | IEEE 浮点底层物理验证 | 幻灯片 — 演讲 + 影院滚屏 | 词汇表 v3.0 词条 |

---

## 这是什么

Aitchison 在 1986 年为本领域奠定了几何基础；CoDaWork 已培养四十年的方法学者。**Hˢ 将当前与发展中的 CoDa 方法封装为一项可执行的运维化标准** —— 七个阶段，两个人工关卡，确定性的、带哈希链的输出，无论按键来自研究者还是 AI 助手，结果完全一致。数学是标准的；运维化的框架可能是新的。

---

## 为何要将组分分析运维化

- **可测性。** 将理论上的组分结构转化为每步可复现的诊断量：helmsman（CLR 运动的手性）、Power Share、Activation Coefficient、导航方位。可量化、可比较、可审计。
- **一致性。** 固定模式（CNT v3.1.0 / CNQ v2.0.0）、固定管线、跨机器、跨操作系统、跨 BLAS、跨年份按字节相同的复跑。同输入同输出，始终如一。
- **假设检验。** 同一引擎在产生结果的同时也产生用于推翻它的可证伪框架（MC-4 —— 四条具名的反驳路径）。没有不可证伪的发表。

---

## 相对临时拼凑式 CoDa 管线的数值与运维优势

- **Helmert-ILR 正交归一坐标** —— 无平衡选择的任意性；团队间确定性基底。
- **针对 helmsman 与导航角的 atan2** —— 在 ±π 邻域安全；在周期边界无精度损失或符号跳变。
- **哈希链溯源** —— SHA-256 从原始 CSV 贯穿到 CNT JSON、图版、投影器与论文插图。2030 年的审稿人仍可证明一切未变。
- **跨平台 IEEE 浮点底层确定性** —— 同输入同输出，逐机器、逐次一致。已在 Backblaze 硬盘遥测、Planck CMB 偏振、标准模型中微子振荡上验证。
- **一致量程准则（CRD-1.0）** —— 多载体比较在所有成员量程的交集上计算；非对称漂移伪影被消除。
- **带模式版本号的输出** —— 每个 JSON 声明其模式；会议语料锁定于 `3.1.0` / `cnq/2.0.0`，不随引擎版本漂移而失读。

---

## 三层运维化标准

| 层 | 角色 | 作用 |
|---|---|---|
| **CNT v3.1.0** | 测量 | 闭合 → CLR → Helmert-ILR → 每步组分度量、helmsman、Power Share、Activation Coefficient、导航、诊断、哈希。当前源 v3.2.0 新增 `navigation_2d`，用于 Helmert-ILR PCA 重心轨迹。 |
| **CNQ v2.0.0** | 命名代数 | 四元数视角的仪表盘与高阶结构诊断（CHSH 联合相干、D=8 下满足 Tsirelson 界的双四元数因子分解）。CNT 的代数伴体。 |
| **CCTT v1.0** | 运维化 | 可执行的标准。七个阶段（诊断 → 适配器 *关卡* → 引擎 → 输出 → 渲染 → 自验证 *关卡* → 呈现 + 日志）。两个人工关卡；其余一律确定性。**仓库同时训练研究者与 AI 助手 —— 同一协议，同一可哈希验证的输出。** |

---

## CCTT 七阶段协议

`[1] 诊断` → `[2] 适配器（关卡）` → `[3] 引擎` → `[4] 输出` → `[5] 渲染` → `[6] 自验证（关卡）` → `[7] 呈现 + 日志`

---

## 演讲中的五个视角

- **组分** —— 每个载体所占的份额。
- **Helmsman** —— 单步内最大的 CLR 位移。
- **Helmsman 轨迹** —— 主导方向何时切换。
- **Power Share** —— 每个载体贡献了多少 CLR 平方运动。
- **Activation Coefficient** —— Power Share ÷ 起始份额 = "酵母系数"。

---

## 运维证据 —— 标准所揭示的事实

载体可以份额很小，却承担巨大的结构性工作。**USA Solar 2012 → 2013：** 起始份额 0.107%，结构性 Power Share 占 81.7%，**Activation Coefficient ≈ 760×**。

跨国"欺骗性漂移"特征在 **9 国中 5 国**（AUS、CHN、GBR、IND、JPN）触发，而在 DEU（年频）、FRA、USA 与 WLD *未* 触发。协议具有区分力；不会误触发。**对原始份额做回归不会发现这两项结果。**

---

## 标准入门 —— 选择您的入口

1. **会议参会者：** `CODA-Association/CONFERENCE_ATTENDEES.md` —— 幻灯片逐张跟读。
2. **可视化探索（无需安装）：** `CODA-Association/CODAwork2026/data_outputs/codawork2026_projector.html`。
3. **运行您自己的组分数据：** `QUICKSTART.md` + `ai-refresh/CCTT_QUICKSTART.md` —— 七阶段操作手册，可手动或借助 AI。
4. **核对已发表数字：** 论文 + 补充材料 + 各国 JSON + 哈希链。
5. **术语查询：** `HCI-CNT/handbook/GLOSSARY.md` v3.0（约 220 条：PCA、SVD、CLR/ILR、Helmert、CHSH、Tsirelson、Activation Coefficient、MC-1..MC-4）。

---

## 联系与采纳

| 项目 | 详情 |
|---|---|
| **演讲** | *"单纯形上的能源结构漂移之组分监测"*，CoDaWork 2026，科英布拉，6 月 1–5 日。会场间与 Q&A 期间欢迎找到 Peter —— 乐意现场演示投影器。 |
| **联系方式** | Peter Higgins — **PeterHiggins@RogueWaveAudio.com** · Rogue Wave Audio / Binaural Test Lab，加拿大安大略省马卡姆 |
| **代码库** | `github.com/PeterHiggins19/higgins-decomposition` · 社区目录：`CODA-Association/` · 会议目录：`CODA-Association/CODAwork2026/` |
| **如何引用** | Higgins, P. (2026). *Compositional monitoring of energy-mix drift on the simplex.* CoDaWork 2026, Coimbra. 代码库：github.com/PeterHiggins19/higgins-decomposition（提交号见 `HS_FAST_REFRESH.json`）。 |
| **如何采纳** | Fork 仓库，对您的组分数据执行 7 阶段 CCTT，提交 `JOURNAL.md`。AI 助手遵循同样的关卡。结构化采纳测试见 `ai-refresh/COMMUNITY_TEST_PACKET.json`。 |
| **许可** | Apache-2.0（代码）· CC BY 4.0（文档与图表）。完全开源 —— 可自由 fork、审计、扩展、署名。 |

---

*仪器读取。专家判定。哈希承载凭证。词汇守住底线。AI 遵循同一协议。*
