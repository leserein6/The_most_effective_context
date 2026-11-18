# 测试工程参考依据与适用边界

原始标准与研究用于界定测试设计方法，而不是证明本仓库的 Agent 协议已在真实生产环境成功。

1. ISTQB, Certified Tester Foundation Level Syllabus v4.0.1 (2024), https://istqb.org/wp-content/uploads/2024/11/ISTQB_CTFL_Syllabus_v4.0.1.pdf —— EP、BVA、决策表、状态迁移、结构覆盖、测试过程。
2. Goodenough & Gerhart, Toward a Theory of Test Data Selection (1975), DOI:10.1109/TSE.1975.6312834 —— 测试选择准则与充分性理论；不意味着有限测试证明无缺陷。
3. DeMillo, Lipton & Sayward, Hints on Test Data Selection: Help for the Practicing Programmer (1978), https://doi.org/10.1109/COMPSAC.1978.810434 —— 变异测试思想。
4. Claessen & Hughes, QuickCheck: A Lightweight Tool for Random Testing of Haskell Programs (ICFP 2000), https://doi.org/10.1145/351240.351266 —— 基于性质的自动化生成与反例。
5. NISTIR 8397, Guidelines on Minimum Standards for Developer Verification of Software (2021), https://doi.org/10.6028/NIST.IR.8397 —— 黑盒/结构/历史测试、fuzz、安全与静态分析组合。
6. NIST ACTS combinatorial testing FAQ, https://csrc.nist.gov/projects/automated-combinatorial-testing-for-software/faqs —— t-way 覆盖数组与条件交互。
7. NASA SWE-052 / SWE-067 / SWE-141, https://swehb.nasa.gov/ —— 需求双向追踪、实现验证和独立 V&V。
8. NASA NPR 7150.2C, https://nodis3.gsfc.nasa.gov/displayAll.cfm?Internal_ID=N_PR_7150_002C_ —— 安全等级/结构覆盖与软件工程要求；本项目仅借鉴方法，不冒用认证状态。
9. FAA AC 20-115D, https://www.faa.gov/documentLibrary/media/Advisory_Circular/AC_20-115D.pdf —— 机载软件发展保证及 DO-178C 认可；航空要求有适用范围，不是普通后端的普遍合规义务。
10. UTBoost (ACL 2025), https://aclanthology.org/2025.acl-long.189/ —— 测试对 AI 生成补丁的约束能力与局限；实证结论应限定研究数据和设置。
11. Meta TestGen-LLM (2024), https://arxiv.org/abs/2402.09171 —— 工业化候选测试生成与可执行过滤；过滤不等于规格验证。

研究结论和工程约束要分开：以上资料支持采用多种测试技术、可追溯性和风险分级；**本仓库的具体方法选择表、JSON 格式、门禁状态与实现代码是工程设计，需要经真实项目评估**。
