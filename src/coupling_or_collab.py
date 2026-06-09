# coupling_or_collab.py
import pandas as pd
import numpy as np
import networkx as nx
from scipy.sparse import csr_matrix
import warnings
from config_loader import CFG

warnings.filterwarnings('ignore')

def build_coupling():
    data_path = CFG["paths"]["raw_data"]
    encoding = CFG["basic"]["encoding"]
    split_char = CFG["basic"]["split_char"]
    min_len = CFG["basic"]["min_text_len"]
    min_couple = CFG["analysis"]["coupling_collab"]["min_couple_link"]

    df = pd.read_csv(data_path, encoding=encoding)
    df = df.dropna(subset=["DI", "CR"])

    cite_list = []
    for _, row in df.iterrows():
        did = row["DI"]
        refs = str(row["CR"]).split(split_char)
        for r in refs:
            rr = r.strip()
            if len(rr) > min_len:
                cite_list.append([did, rr])

    df_cite = pd.DataFrame(cite_list, columns=["citing", "cited"])
    citing_unique = df_cite["citing"].unique()
    cited_unique = df_cite["cited"].unique()

    row_idx = [list(citing_unique).index(x) for x in df_cite["citing"]]
    col_idx = [list(cited_unique).index(x) for x in df_cite["cited"]]
    spR = csr_matrix((np.ones(len(row_idx)), (row_idx, col_idx)))

    # 文献耦合矩阵
    B_sparse = spR @ spR.T
    B_mat = np.asarray(B_sparse.todense())
    return B_mat, citing_unique

def author_collab():
    data_path = CFG["paths"]["raw_data"]
    encoding = CFG["basic"]["encoding"]
    split_char = CFG["basic"]["split_char"]
    sample_num = CFG["analysis"]["centrality"]["between_sample"]
    eigen_iter = CFG["analysis"]["centrality"]["eigen_iter"]

    df = pd.read_csv(data_path, encoding=encoding)
    G_auth = nx.Graph()

    for _, row in df.iterrows():
        authors = str(row["AF"]).split(split_char)
        authors = [a.strip() for a in authors if len(a) > 2]
        for i in range(len(authors)):
            for j in range(i + 1, len(authors)):
                a1, a2 = authors[i], authors[j]
                if G_auth.has_edge(a1, a2):
                    G_auth[a1][a2]["weight"] += 1
                else:
                    G_auth.add_edge(a1, weight=1)

    # 中心性计算
    deg = nx.degree_centrality(G_auth)
    bet = nx.betweenness_centrality(G_auth, k=sample_num)
    eig = nx.eigenvector_centrality(G_auth, max_iter=eigen_iter)

    auth_df = pd.DataFrame({
        "author": list(deg.keys()),
        "degree": list(deg.values()),
        "betweenness": list(bet.values()),
        "eigenvector": list(eig.values())
    })
    return auth_df

if __name__ == "__main__":
    B_mat, paper_ids = build_coupling()
    auth_res = author_collab()
    out_path = CFG["paths"]["table_out"]
    pd.DataFrame(B_mat, index=paper_ids).to_csv(f"{out_path}/文献耦合矩阵.csv")
    auth_res.to_csv(f"{out_path}/作者中心性分析.csv", index=False)
    print("文献耦合、作者数据保存完成")