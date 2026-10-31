# EO-native QEC: four-body parity checks and encoded-flag fault suppression

**Working-paper research snapshot (1 November 2026). Not peer reviewed.**

This directory bundles a readable manuscript, its PDF rendering, selected Jenga-style physical pulse CSVs, original numerical-evidence JSON files, and a minimal structural verifier. It summarizes our numerical EO-native stabilizer research without claiming a demonstrated hardware QEC system or an independently certified fault-tolerant protocol.

## 中文摘要

我们提出并整理了仅依赖各向同性正交换脉冲、无物理单自旋 H/X/Z 的三自旋 EO 原生稳定子检测方案。已有数据支持在一个假设的二维最近邻布局中，用 **92P** 测量四个 EO 逻辑比特的 `ZZZZ`，另用 **92P** 测量逻辑坐标系旋转后的 `X̃X̃X̃X̃`。加入一个三自旋 EO flag 后，单次检测为 **140P/60D**。在一个受到严格限制的三次检测模拟中，276P 无 flag 与 324P 带 flag 的方案相比，后者接受后的编码逻辑错误概率从 **0.06682%** 降到 **0.03744%**，但接受率从 **88.70%** 降到 **86.24%**。这些是 **50 组相关静态 exchange-gain 抽样、固定码字和 gauge、理想读出/复位** 下的模型结果，绝非硬件实验、distance-3 纠错阈值或完整容错证明。

## Files

- [`PAPER.md`](PAPER.md) — English manuscript with mathematical definitions, methods, tables, limitations, and provenance.
- `PAPER.pdf` — typeset PDF available as a downloadable chat attachment. GitHub PDF upload is pending; the manuscript source is [`PAPER.md`](PAPER.md).
- [`EVIDENCE_LEDGER.md`](EVIDENCE_LEDGER.md) — result-by-result evidence and caveat ledger.
- [`sequences/`](sequences/) — selected EO pulse lists and planar coordinates.
- Original numerical evidence JSON is available in the full research ZIP attached in the ChatGPT conversation; see `EVIDENCE_LEDGER.md` for model boundaries.
- Original numerical study archives are downloadable from the ChatGPT conversation; not yet mirrored to GitHub.
- Pulse CSVs and hardware connectivity data are included for independent verification.
- Figures are available in the full research ZIP; not yet mirrored to GitHub.

## Reproduce the structural checks

```bash
python code/check_package.py
```

To reproduce the full 2^15 or 2^18 physical-spin tests, use the original research ZIP archives bundled in `source_archives/` and cited in `PAPER.md`, notably `EO_QEC_FLAGGED_LOGICAL_AUDIT_20261031.zip`. The lightweight checker here intentionally does **not** claim full physical-unitary or correlated-noise re-verification.

## Status

**Supported by prior numerical archives:** ideal nominal gauge-aware instruments; physical exchange pulse sequences; selected single-fault suppression; restricted multi-check correlated-noise comparison.

**Not established:** exhaustive physical fault tolerance, physical leakage-reduction, nonideal singlet/triplet measurement, deterministic correction, distance-three decoding, hardware QEC threshold, or verified priority over existing literature.

For the motivating SOEO+LD prior paper, see Heinz, Sharma and Kattemölle, [arXiv:2608.14214](https://arxiv.org/abs/2608.14214). Their physical-spin stabilizers are distinct from the logical-EO parity checks documented here.

> **GitHub publication status:** This folder was added on a standalone research branch as a draft work-in-progress; its PDF and source archive are separately available through the ChatGPT artifacts pending binary mirroring.
