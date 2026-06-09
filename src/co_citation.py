# co_citation.py
import pandas as pd
import numpy as np
import networkx as nx  # 加上这行，导入networkx
from community import community_louvain
from scipy.sparse import csr_matrix
from sklearn.metrics.pairwise import cosine_similarity
import warnings
from config_loader import CFG  # 导入全局配置

warnings.filterwarnings('ignore')

def build_co_citation():
    # 从yml读取配置
    data_path = CFG["paths"]["raw_data"]
    min_ref = CFG["analysis"]["co_citation"]["min_ref_cite"]
    encoding = CFG["basic"]["encoding"]
    split_char = CFG["basic"]["split_char"]
    min_len = CFG["basic"]["min_text_len"]

    # 读取数据
    df = pd.read_csv(data_path, encoding=encoding)
    # 按配置清洗数据
    if CFG["data_clean"]["drop_empty_doi"]:
        df = df.dropna(subset=["DI"])
    if CFG["data_clean"]["drop_empty_cr"]:
        df = df.dropna(subset=["CR"])
    print(f"✅ 有效文献数量：{len(df)} 篇")

    # 拆分参考文献
    cite_list = []
    ref_all = []
    for _, row in df.iterrows():
        did = row["DI"]
        refs = str(row["CR"]).split(split_char)
        for r in refs:
            rr = r.strip()
            if len(rr) > min_len:
                cite_list.append([did, rr])
                ref_all.append(rr)

    # 筛选高频参考文献
    ref_cnt = pd.Series(ref_all).value_counts()
    keep_refs = ref_cnt[ref_cnt >= min_ref].index.tolist()
    df_cite = pd.DataFrame(cite_list, columns=["citing", "cited"])
    df_cite = df_cite[df_cite["cited"].isin(keep_refs)]

    # 构建稀疏矩阵
    citing_unique = df_cite["citing"].unique()
    cited_unique = df_cite["cited"].unique()
    citing_id = {v: i for i, v in enumerate(citing_unique)}
    cited_id = {v: i for i, v in enumerate(cited_unique)}

    row_idx = [citing_id[x] for x in df_cite["citing"]]
    col_idx = [cited_id[x] for x in df_cite["cited"]]
    spR = csr_matrix((np.ones(len(row_idx)), (row_idx, col_idx)))

    # 共被引矩阵
    C_sparse = spR.T @ spR
    C_mat = np.asarray(C_sparse.todense())
    sim_mat = cosine_similarity(C_mat)

    # 聚类（这里把nx加上了）
    G = nx.from_numpy_array(sim_mat)
    partition = community_louvain.best_partition(G)
    modularity = community_louvain.modularity(partition, G)
    print(f"✅ 共被引网络模块度：{round(modularity, 3)}")

    return C_mat, sim_mat, cited_unique

if __name__ == "__main__":
    C_mat, sim_mat, ref_names = build_co_citation()
    # 保存结果（读取配置路径）
    out_path = CFG["paths"]["table_out"]
    pd.DataFrame(C_mat, index=ref_names).to_csv(f"{out_path}/共被引矩阵.csv")
    print("共被引矩阵保存完成")