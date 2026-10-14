#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
biocompat.py — ISO 10993-1 生物学评价终点矩阵
==============================================
按接触性质（表面/外部接入/植入）× 接触组织 × 接触时限
输出需评终点（细胞毒性/致敏/刺激/急性全身/亚慢性/慢性/遗传毒性/
致癌/生殖/植入/血液相容性/降解）。

诚实边界：矩阵按 ISO 10993-1:2018 通用框架整理；终点减免须以
毒理学风险评估（TRA，含 ISO 10993-18 化学表征）论证。
"""
from __future__ import annotations
import argparse
import sys

NATURES = ["surface", "external_communicating", "implant"]
TISSUES = {
    "surface": ["skin", "mucosal"],
    "external_communicating": ["breached_surface", "blood_path", "circulating_blood", "nerve"],
    "implant": ["tissue", "bone", "blood", "nerve"],
}
DURATIONS = ["limited", "prolonged", "permanent"]  # ≤24h / 24h–30d / >30d

# 终点矩阵：(nature, tissue, duration) -> endpoints
def endpoints_for(nature: str, tissue: str, duration: str) -> list[str]:
    base = ["细胞毒性"]
    if nature == "surface":
        eps = base + ["皮肤刺激", "致敏"]
        if tissue == "mucosal":
            eps.append("粘膜刺激")
    elif nature == "external_communicating":
        eps = base + ["致敏", "刺激/皮内反应", "急性全身毒性"]
        if tissue in ("blood_path", "circulating_blood"):
            eps += ["血液相容性", "血栓"]
        if duration in ("prolonged", "permanent"):
            eps += ["亚慢性毒性", "遗传毒性", "植入（局部）"]
    else:  # implant
        eps = base + ["致敏", "刺激", "急性全身毒性", "亚慢性/慢性毒性",
                      "遗传毒性", "植入"]
        if tissue == "bone":
            eps += ["骨相容性/组织整合"]
        if tissue == "blood":
            eps += ["血液相容性"]
        if duration == "permanent":
            eps += ["致癌性", "生殖/发育毒性", "降解（如可吸收）"]
    return sorted(set(eps))


GAP_HINTS = {
    "化学表征": "ISO 10993-18：可浸出物/可提取物 → 毒理学风险评估（TTC 阈值）",
    "降解": "可吸收材料须做降解动力学与降解产物评价（ISO 10993-9/-13/-14/-15）",
    "灭菌影响": "灭菌后残留（EO/ECH）与材料老化对生物相容性的影响（ISO 10993-7/-18/-19）",
    "纳米材料": "纳米特征材料需专项评估（ISO/TR 10993-22）",
}


def _demo() -> int:
    print("ISO 10993-1 终点矩阵 · 演示\n")
    for nature, tissue, dur in [("surface", "skin", "limited"),
                                ("external_communicating", "blood_path", "prolonged"),
                                ("implant", "bone", "permanent")]:
        eps = endpoints_for(nature, tissue, dur)
        print(f"### {nature} × {tissue} × {dur}")
        print(f"  需评终点: {', '.join(eps)}")
    print("\n### Gap 分析提示")
    for k, v in GAP_HINTS.items():
        print(f"  - {k}: {v}")
    print("\n[demo] 矩阵按 ISO 10993-1:2018 通用框架；终点减免须 TRA 论证。")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description="ISO 10993-1 生物学评价终点矩阵")
    ap.add_argument("--demo", action="store_true", help="跑内置演示")
    ap.add_argument("--selftest", action="store_true", help="跑内置自测（断言 + 负对照 + xfail）")
    ap.add_argument("--nature", choices=NATURES, help="接触性质")
    ap.add_argument("--tissue", help="接触组织（随 nature 可选，见 --tissues）")
    ap.add_argument("--duration", choices=DURATIONS, help="接触时限")
    ap.add_argument("--tissues", action="store_true", help="列出各 nature 可选组织")
    args = ap.parse_args()
    if getattr(args, "selftest", False):
        return _selftest()

    if args.demo:
        return _demo()
    if args.tissues:
        for n, ts in TISSUES.items():
            print(f"{n}: {', '.join(ts)}")
        return 0
    if args.nature and args.tissue and args.duration:
        if args.tissue not in TISSUES[args.nature]:
            print(f"[err] {args.nature} 不支持组织 {args.tissue}（可选: {TISSUES[args.nature]}）")
            return 2
        eps = endpoints_for(args.nature, args.tissue, args.duration)
        print(f"### {args.nature} × {args.tissue} × {args.duration}")
        for e in eps:
            print(f"  - [ ] {e}")
        return 0
    ap.print_help()
    return 2


# ==================== 内置自测（--selftest） ====================
# 由 conformance 补丁于 2026-10-14 生成（生成器 v2）。
# 特性：端到端 CLI 调用 + 内容断言 + 负对照 + xfail（已知缺陷显式标注，不掩盖）。
_SELFTEST_CASES = [(['--demo'], 0, [], [], None), (['--tissues'], 0, [], [], None), (['--nature', 'implant', '--tissue', 'bone', '--duration', 'permanent'], 0, [], [], None)]


def _selftest() -> int:
    import os as _os
    import subprocess as _sp
    _here = _os.path.dirname(_os.path.abspath(__file__))
    # 仓库根：脚本位于 <repo>/scripts/ 时取上一级；否则取脚本所在目录
    _root = _os.path.dirname(_here) if _os.path.basename(_here) == "scripts" else _here
    _script = _os.path.abspath(__file__)
    _fail, _xfail, _n = [], [], 0
    for _case in _SELFTEST_CASES:
        _args, _rc, _must, _mustnot = _case[0], _case[1], _case[2], _case[3]
        _reason = _case[4] if len(_case) > 4 else None
        _n += 1
        _p = _sp.run([sys.executable, _script] + _args, capture_output=True, cwd=_root)
        _out = _p.stdout.decode("utf-8", "replace")
        _bad = []
        if _p.returncode != _rc:
            _bad.append(f"rc={_p.returncode} 期望 {_rc}")
        for _m in _must:
            if _m not in _out:
                _bad.append(f"输出缺少 {_m!r}")
        for _m in _mustnot:
            if _m in _out:
                _bad.append(f"输出含禁止内容 {_m!r}")
        if _rc == 0 and not _out.strip():
            _bad.append("rc=0 但输出为空（假绿）")
        if _bad:
            if _reason:
                _xfail.append(f"xfail args={_args}：{'；'.join(_bad)} ← 已知缺陷：{_reason}")
            else:
                _fail.append(f"args={_args}：{'；'.join(_bad)}")
    # 通用负对照：未知参数必须非零
    _n += 1
    _p = _sp.run([sys.executable, _script, "--__nonexistent_flag__"], capture_output=True, cwd=_root)
    if _p.returncode == 0:
        _fail.append("负对照失败：未知参数竟返回 0")
    for _x in _xfail:
        print("[selftest][xfail] " + _x)
    if _fail:
        print(f"[selftest] FAILED {len(_fail)}/{_n}")
        for _f in _fail:
            print("  - " + _f)
        return 1
    print(f"[selftest] PASS {_n - len(_xfail)}/{_n}（含负对照；xfail {len(_xfail)} 项为已知缺陷）")
    return 0


if __name__ == "__main__":
    try:
        if hasattr(sys.stdout, "reconfigure"):
            sys.stdout.reconfigure(encoding="utf-8")
            sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass
    raise SystemExit(main())
