# EO / SOEO 交换量子门与纠错研究汇总

这是 2026 年 11 月 1 日整理的**科研工作稿**，并非正式发表论文或实验成果。英文论文在 [PAPER.md](PAPER.md)，排版 PDF 在同一下载包 `PAPER.pdf`。

主要结果：在严格单 bond、正 Heisenberg exchange 条件下，得到 11P 鲁棒 H、13P 鲁棒 S 和 Z（分别在三自旋 EO 的两个 gauge、四自旋 SOEO 的总自旋零编码空间复核）；四星形 SOEO 检测提供一阶静态增益抵消和 probabilistic S=0 检测，但要求四条耦合同时开启，**它是保护恒等操作，不是逻辑纠缠门**；六自旋 EO–EO 的 43P 到 41P 精确改写降低了所定义的静态噪声系数约 16.4%，跨 EO 的 J34 一阶误差仍未消除。

论文同时包含严格限定条件下的单次跨编码 exchange 泄漏限制、全 bond 鲁棒门的必要条件，以及与 XX/XXXX 稳定子测量和多轮 QEC 的关系。**目前没有得到所有 bond 一阶抵消的 CZ，也没有完成新的多轮 decoded logical error 验证。**

直接运行：`OPENBLAS_NUM_THREADS=1 python code/verify_all_physical.py`。其他验证见 `README.md`。
