# src/run.py
from co_citation import build_co_citation
from coupling_or_collab import build_coupling, author_collab
from config_loader import CFG
import os

# 自动创建输出文件夹
os.makedirs(CFG["paths"]["table_out"], exist_ok=True)
os.makedirs(CFG["paths"]["figure_out"], exist_ok=True)

if __name__ == "__main__":
    print("===== 开始执行文献计量全分析 =====")
    build_co_citation()
    build_coupling()
    author_collab()
    print("===== 所有分析执行完毕 =====")