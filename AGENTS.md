# AGENTS.md · biocompatibility-iso10993

> 机器可发现入口（AI 编码代理 / Codex / Claude / Cursor）。单一事实源：本文件。

## 这是什么
ISO 10993-1:2018 生物学评价终点判定矩阵：按接触性质（表面/外部接入/植入）× 接触组织（皮肤/粘膜/损伤皮肤/组织/骨/血液/神经）× 接触时限（有限 ≤24h / 24h–30d / >30d）输出需评终点（细胞毒性/致敏/刺激/急性/亚慢性/慢性/遗传毒性/致癌/生殖/植入/血液相容性/降解），并给出化学表征（ISO 10993-18）与 Gap 分析清单。

## 运行
```bash
python scripts/biocompat.py --demo
python scripts/biocompat.py --help
```

## 扩展契约（lgd-skeleton/1.0）
- **一切即插件**：仅依赖声明式 `module.json`，零配置。
- **按需装（lazy）**：仅 triggers 命中时加载。
- **可嵌套（nested）**：可被 `medical-ai-toolkit` 总入口路由。
- **扩展点**：`plugins/`(新增终点：在 ENDPOINT_MATRIX 加一行。)

## 红线
纯技术贡献，不含商业营销；MedXpert 仅作为贡献者署名（@stevenzhao07）。
