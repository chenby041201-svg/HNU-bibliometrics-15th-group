## 项目名称 二位过渡金属氧化物异质结研究

## 团队分工

| 成员 | 角色 | 职责 |
| :--- | :--- | :--- |
| **吴量** | 可视化与分析 | 知识图谱矩阵构建、图拓扑指标计算（中心性分析）、可视化产出 |
| **陈伯言** | 数据处理 | 数据获取与去重、归一化清洗、数据字段质量检查 |
| **陈宇浩** | 检索式设计 | 核心概念四元组拆解、布尔检索式构建、PRISMA 筛选流程制定 |
| **武思远** | 文档撰写 | 报告与论文撰写、证据链构建、文献引用管理、答辩 PPT 制作 |

---

## 1. 项目环境与依赖 (Requirements)

为了能够复现或查看本项目的分析图谱与底层数据，建议使用以下环境配置：
* **操作系统**：Windows 10/11 或 macOS
* **计量分析工具**：VOSviewer (Version 1.6.19 或更高版本)
* **数据处理环境**：Microsoft Excel / WPS Office (用于查看 CSV 报表)
* **文本阅读器**：支持 Markdown 语法的编辑器（如 VS Code / Typora）

---

## 2. 数据来源与检索策略 (Data Source)

本项目所有的文献计量样本均来源于权威核心数据库，以确保分析的科学性与代表性：
* **数据库**：Web of Science (WoS) 核心合集 / Scopus
* **时间跨度**：2012 年 —— 2025 年
* **核心关键词**：`photocatalysis`, `TiO2`, `g-C3N4`, `heterojunction`, `hydrogen production`
* **样本总量**：经去重、规范化清洗后，共计保留有效核心文献样本若干篇。

---

## 3. 规范化仓库目录结构 (Directory Structure)

本仓库严格遵循模块化与可重复性科研的标准进行组织，具体结构如下：

```text
my_bibliometrics_project/
│
├── data/                    # 底层数据文件夹
│   └── processed/           # 存放清洗、计算后的中间网络配置文件 (VOSviewer 底层数据)
│       └── vosviewer_networks/
│
├── docs/                    # 项目综合文档夹
│   └── literature_review_report.md  # 综合文献计量学分析报告（论文雏形）
│
├── outputs/                 # 核心产出成果文件夹（★核心检查入口）
│   ├── M2_产出清单_完整报告.md # M2阶段全局产出成果总览与综合摘要
│   │
│   ├── 01_trends/            # 维度一：年度发文量趋势分析（数量线与时间线）
│   │   ├── annual_publication_trend.csv
│   │   ├── annual_trend_chart.jpg
│   │   └── trends_analysis.md
│   │
│   ├── 02_authors_institutions/ # 维度二：核心作者与学术合作网络（大牛圈子）
│   │   ├── top20_authors.csv
│   │   ├── author_centrality_analysis.csv
│   │   ├── author_coauthorship_network.jpg
│   │   └── authors_analysis.md
│   │
│   ├── 03_keywords_hotspots/ # 维度三：关键词共现与研究热点板块
│   │   ├── keyword_cooccurrence.jpg
│   │   └── keywords_analysis.md
│   │
│   └── 04_citations_intellect/ # 维度四：高被引奠基文献与引文双向网络（共被引与耦合）
│       ├── top50_highly_cited_docs.csv
│       ├── document_cocitation_network.jpg
│       ├── document_coupling_network.jpg
│       └── citations_analysis.md
│
└── README.md                # 本说明文件
