# src/config_loader.py
import yaml
import os

# 加载全局配置
def load_config():
    # 直接写死绝对路径，不用相对路径
    config_path = r"D:\TMO_Hetero_Bib\config\config.yml"
    with open(config_path, "r", encoding="utf-8") as f:
        cfg = yaml.safe_load(f)
    return cfg

# 全局配置变量
CFG = load_config()