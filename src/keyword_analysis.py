import os
import pandas as pd
import matplotlib.pyplot as plt
from collections import Counter

def main():
    # ========== 完全适配你的项目路径 ==========
    # 项目根目录（自动定位，不用手动改）
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    
    # 数据文件路径（你的清洗后数据）
    data_path = os.path.join(project_root, "data", "processed", "wos_cleaned.csv")
    
    # 输出文件夹（自动创建）
    output_dir = os.path.join(project_root, "outputs")
    os.makedirs(output_dir, exist_ok=True)
    
    # 输出文件路径
    csv_out = os.path.join(output_dir, "top20_keywords.csv")
    img_out = os.path.join(output_dir, "top20_keywords.png")

    # 检查数据文件是否存在
    if not os.path.exists(data_path):
        print(f"❌ 找不到数据文件！请确认文件存在：{data_path}")
        return

    # ========== 读取并处理关键词 ==========
    df = pd.read_csv(data_path)
    print(f"✅ 成功读取数据，总文献数：{len(df)} 篇")

    # 存储所有关键词
    all_keywords = []
    # 遍历DE列（WOS标准关键词/描述词列），剔除空值
    for kw_text in df["DE"].dropna():
        # 按英文分号拆分关键词，去除首尾空格，统一转为小写（避免大小写重复统计）
        kw_list = [k.strip().lower() for k in kw_text.split(";")]
        all_keywords.extend(kw_list)

    # 统计词频，取Top20高频关键词
    kw_counter = Counter(all_keywords)
    top20_kw = kw_counter.most_common(20)

    # ========== 保存结果 ==========
    # 1. 保存为CSV表格（可直接用于报告）
    kw_df = pd.DataFrame(top20_kw, columns=["Keyword", "Frequency"])
    kw_df.to_csv(csv_out, index=False, encoding="utf-8-sig")
    print(f"✅ 关键词频次表格已保存：{csv_out}")

    # 2. 绘制横向柱状图（学术报告专用，高清300DPI）
    words, counts = zip(*top20_kw)
    plt.figure(figsize=(14, 9))
    plt.barh(words, counts, color="#3474A7")
    plt.xlabel("Frequency", fontsize=12)
    plt.ylabel("Keywords", fontsize=12)
    plt.title("Top 20 Core Keywords Distribution", fontsize=14, pad=20)
    plt.grid(axis="x", alpha=0.3)
    plt.tight_layout()
    plt.savefig(img_out, dpi=300, bbox_inches="tight")
    plt.close()
    print(f"✅ 关键词柱状图已保存：{img_out}")

    # 控制台打印结果，方便快速查看
    print("\n========== 二维过渡金属氧化物异质结领域 Top20 核心关键词 ==========")
    for idx, (word, cnt) in enumerate(top20_kw, 1):
        print(f"{idx:2d}. {word:<35} {cnt} 次")

if __name__ == "__main__":
    main()