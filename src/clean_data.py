import pandas as pd
import os

# ==================== 路径配置（已适配你的目录，无需修改） ====================
# 原始数据：raw 文件夹
RAW_CSV = r"D:\TMO_Hetero_Bib\data\raw\wos_raw.csv"
# 清洗后数据：自动保存到 processed 文件夹
PROCESSED_CSV = r"D:\TMO_Hetero_Bib\data\processed\wos_cleaned.csv"

def data_clean_dedup():
    print("========== WOS 数据清洗 + 去重工具 ==========\n")

    # 1. 读取原始数据
    try:
        df = pd.read_csv(RAW_CSV, encoding="utf-8")
        print(f"原始数据总条数：{len(df)}")
    except FileNotFoundError:
        print(f"错误：未找到原始文件 → {RAW_CSV}")
        return

    # 2. 统计关键字段缺失（DI=DOI，CR=参考文献，TI=标题）
    print("\n【关键字段缺失统计】")
    print(f"DOI(DI) 缺失条数：{df['DI'].isna().sum()}")
    print(f"参考文献(CR) 缺失条数：{df['CR'].isna().sum()}")
    print(f"标题(TI) 缺失条数：{df['TI'].isna().sum()}")

    # 3. 删除关键字段为空的无效行
    df = df.dropna(subset=["DI", "CR", "TI"])
    print(f"\n删除空值后剩余条数：{len(df)}")

    # 4. 基于DOI全局去重（保留第一条有效数据）
    df["DI"] = df["DI"].astype(str)  # 统一格式，避免类型报错
    df_clean = df.drop_duplicates(subset=["DI"], keep="first")
    print(f"去重后最终条数：{len(df_clean)}")
    print(f"累计删除重复数据：{len(df) - len(df_clean)} 条")

    # 5. 自动创建processed文件夹（不存在则新建）
    os.makedirs(os.path.dirname(PROCESSED_CSV), exist_ok=True)

    # 6. 保存清洗后的数据
    df_clean.to_csv(PROCESSED_CSV, index=False, encoding="utf-8")
    print(f"\n✅ 清洗完成！文件已保存至：{PROCESSED_CSV}")

if __name__ == "__main__":
    data_clean_dedup()