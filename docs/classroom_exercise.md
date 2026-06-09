# 文献计量学课堂练习与流水线实验记录 (Classroom Exercise)

* **课程名称**: 文献计量学和前沿趋势追踪（2026春季学期）
* **授课教师**: 湖南大学 杨其晟副教授
* **项目定位**: 项目制 · 可复现 · 可二开
* **实验小组**: [填入你们组号]

---

## 实验一：研究问题拆解与检索式工程化 (Lesson 02 产出)

为防止布尔表达式范围爆炸或 NOT 误杀，本组拒绝盲目检索。通过对现有关键词共现图谱的中心节点进行反推，确立本项目的检索策略。

### 1. 核心概念同义词扩展表 (Synonym Map)
* **研究对象 (Object)**: 二氧化钛、氮化碳等半导体光催化剂
  * *关键词*: `titanium dioxide`, `TiO2`, `g-C3N4`, `graphlitic carbon nitride`, `semiconductor`
* **改性方法 (Method)**: 异质结网络构建
  * *关键词*: `heterojunction`, `heterostructure`, `S-scheme`, `Z-scheme`, `charge separation`
* **应用场景 (Context)**: 能源转化与环境降解
  * *关键词*: `hydrogen production`, `water splitting`, `photocatalytic degradation`

### 2. 工程化检索式配置 (`config/query.yaml`)
依据课件要求，严格固定检索参数，确保他人一键克隆项目后可完全复现：
```yaml
metadata:
  version: "0.1"
  database: "Web of Science Core Collection"
  edition: "SCI-EXPANDED"
  timestamp: "2026-06-09"

constraints:
  time_window: [2012, 2026]
  document_type: ["Article", "Review"]
  language: "English"

query_string: >-
  TS=(("titanium dioxide" OR "TiO2" OR "g-C3N4" OR "graphlitic carbon nitride") 
  AND ("heterojunction" OR "S-scheme" OR "charge separation") 
  AND ("hydrogen production" OR "degradation"))
