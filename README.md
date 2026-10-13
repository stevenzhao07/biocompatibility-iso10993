# biocompatibility-iso10993

> **Contributed by [@stevenzhao07](https://github.com/stevenzhao07) · Affiliation: MedXpert (medical-device RA & regulatory consultancy) · Pure technical input, no commercial promotion.**

ISO 10993-1:2018 生物学评价终点判定矩阵：按接触性质（表面/外部接入/植入）× 接触组织（皮肤/粘膜/损伤皮肤/组织/骨/血液/神经）× 接触时限（有限 ≤24h / 24h–30d / >30d）输出需评终点（细胞毒性/致敏/刺激/急性/亚慢性/慢性/遗传毒性/致癌/生殖/植入/血液相容性/降解），并给出化学表征（ISO 10993-18）与 Gap 分析清单。

这是 MedXpert 把"医疗 AI 信任"方法论工程化落地的可插拔模块之一——把抽象的合规要求变成一条可重复运行的命令或参考实现。方法论四要素（白话版）：**治理守护者 XCGS** ＝ 为 AI 留下可核验的治理证据；**立法者 A³ Laws** ＝ 给自主系统划权限 / 监督 / 追责三条硬边界；**护照官 AI 护照** ＝ 为模型签发可追溯的身份凭证；**人机共存** ＝ 明确人类与 AI 的分工与兜底。

---

## 可插拔模块契约（lgd-skeleton/1.0）

本仓库是一个 **`lgd-skeleton/1.0` 可插拔模块**：

- **一切即插件**：仅依赖声明式 `module.json`，零配置；
- **按需装（lazy）**：仅 triggers 命中时加载；
- **可嵌套（nested）**：可被 `medical-ai-toolkit` 总入口路由发现；
- **扩展点**：`plugins/`(新增终点：在 ENDPOINT_MATRIX 加一行。)。

机器可发现入口：`AGENTS.md` · `CLAUDE.md` · `llms.txt`。

## 特性

- 终点矩阵：接触性质 × 接触组织 × 时限 → 必评/条件评终点清单
- 植入类扩展：骨/组织/血液接触的植入专项终点
- 化学表征挂点：ISO 10993-18 可浸出物/毒理学风险评估阈值（TTC）提示
- Gap 分析：已有报告 vs 需评终点缺口输出

## 内容说明

矩阵按 ISO 10993-1:2018 通用框架整理；具体产品的终点减免须以毒理学风险评估（TRA/化学表征）论证。

## 免责声明

本工具仅提供结构化模板与计算能力，**不构成法规建议、临床建议或产品合规结论**。具体产品的注册、临床评价、灭菌验证、风险分析、软件分级等决策，须由合资格人员依据目标辖区（NMPA / FDA / EU MDR / PMDA）最新法规文本作出；条款与限值以官方发布文本为准。使用本工具产生的一切后果由使用者自行承担。

## 使用

```bash
python scripts/biocompat.py --demo
python scripts/biocompat.py --nature implant --tissue bone --duration permanent
```

## 快速开始（30 秒）

```bash
git clone https://github.com/stevenzhao07/biocompatibility-iso10993.git && cd biocompatibility-iso10993
python scripts/biocompat.py --demo
```

> 想参与或遇到问题？[提 Issue](https://github.com/stevenzhao07/biocompatibility-iso10993/issues) · 完整《AI 参与指南》见 [medical-ai-toolkit](https://github.com/stevenzhao07/medical-ai-toolkit)。

## 路由（总入口）

本模块由 **[medical-ai-toolkit](https://github.com/stevenzhao07/medical-ai-toolkit)** 作为 `lgd-skeleton/1.0` 总入口自动路由发现。

## 关联模块

- [sterilization-validation](https://github.com/stevenzhao07/sterilization-validation)
- [design-controls-toolkit](https://github.com/stevenzhao07/design-controls-toolkit)
- [manufacturing-gmp](https://github.com/stevenzhao07/manufacturing-gmp)

## 许可

CC-BY-4.0 — 见 [LICENSE](./LICENSE)。

## 关联（方法论来源）

- 理念溯源：个人专家关于医疗 AI 信任与治理的公开方法论（个人观点，不构成标准）
- 同账号系列：见 `medical-ai-toolkit` 导航
