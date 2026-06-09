import pandas as pd
import numpy as np
import networkx as nx
from community import community_louvain
import os
import warnings
warnings.filterwarnings('ignore')

# 路径不用改
DATA_PATH = r"D:\TMO_Hetero_Bib\data\raw\wos_raw.csv"
OUTPUT_PATH = r"D:\TMO_Hetero_Bib\outputs"
MIN_REF = 5  # 把门槛从3提高到5，减少数据量

os.makedirs(OUTPUT_PATH, exist_ok=True)

print("正在读取数据...")
df = pd.read_csv(DATA_PATH, encoding='utf-8')
df = df.dropna(subset=["DI", "CR"])
print(f"✅ 有效文献数量：{len(df)} 篇")

# 1. 先做基础统计（一定能跑完）
print("\n正在计算基础统计...")
# 年度发文趋势
year_trend = df["PY"].value_counts().sort_index()
year_trend.to_csv(os.path.join(OUTPUT_PATH, "年度发文趋势.csv"))
# 高产作者
authors = []
for _, row in df.iterrows():
    for a in str(row["AF"]).split(";"):
        authors.append(a.strip())
pd.Series(authors).value_counts().head(20).to_csv(os.path.join(OUTPUT_PATH, "top20作者.csv"))
print("✅ 基础统计完成")

# 2. 作者合作网络（轻量版）
print("\n正在构建作者合作网络...")
G_auth = nx.Graph()
for _, row in df.iterrows():
    aus = str(row["AF"]).split(";")
    aus = [a.strip() for a in aus if len(a) > 2]
    for i in range(len(aus)):
        for j in range(i+1, len(aus)):
            a1, a2 = aus[i], aus[j]
            if G_auth.has_edge(a1, a2):
                G_auth[a1][a2]["weight"] += 1
            else:
                G_auth.add_edge(a1, a2, weight=1)

deg = nx.degree_centrality(G_auth)
bet = nx.betweenness_centrality(G_auth, k=100)  # 抽样计算，省内存
eig = nx.eigenvector_centrality(G_auth, max_iter=500)
auth_df = pd.DataFrame({
    "author": list(deg.keys()),
    "degree": list(deg.values()),
    "betweenness": list(bet.values()),
    "eigenvector": list(eig.values())
})
auth_df.to_csv(os.path.join(OUTPUT_PATH, "作者中心性分析.csv"), index=False)
print("✅ 作者合作网络完成")

# 3. 简化版共被引分析（不做大矩阵，只统计高频被引文献）
print("\n正在统计高频被引文献...")
ref_all = []
for _, row in df.iterrows():
    refs = str(row["CR"]).split(";")
    for r in refs:
        ref_all.append(r.strip())
ref_cnt = pd.Series(ref_all).value_counts()
ref_cnt[ref_cnt >= MIN_REF].head(50).to_csv(os.path.join(OUTPUT_PATH, "top50高频被引文献.csv"))
print("✅ 高频被引文献统计完成")

print("\n🎉 轻量版分析全部完成！结果在outputs文件夹")
print("生成文件：")
print("- 年度发文趋势.csv")
print("- top20作者.csv")
print("- 作者中心性分析.csv")
print("- top50高频被引文献.csv")