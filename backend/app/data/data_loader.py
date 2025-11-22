"""
数据获取与预处理模块
使用 yfinance 获取黄金和纳斯达克的历史数据
"""
import pandas as pd
import yfinance as yf
from pathlib import Path
from datetime import datetime
import numpy as np

class DataLoader:
    def __init__(self, cache_dir: str = None):
        # 使用项目根目录的绝对路径
        if cache_dir is None:
            # 获取项目根目录
            current_file = Path(__file__).resolve()
            project_root = current_file.parent.parent.parent  # backend/app/data -> backend/app -> backend -> project_root
            cache_dir = project_root / "data_cache"
        else:
            cache_dir = Path(cache_dir)
        
        self.cache_dir = cache_dir
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        self.cache_file = self.cache_dir / "history_data.csv"
        
    def fetch_and_process_data(self, start_date: str = "2010-01-01", end_date: str = None):
        """
        获取并处理历史数据
        
        Args:
            start_date: 开始日期
            end_date: 结束日期,默认为今天
        """
        if end_date is None:
            end_date = datetime.now().strftime("%Y-%m-%d")
            
        print(f"正在获取 {start_date} 至 {end_date} 的历史数据...")
        
        # 获取黄金ETF数据 (GLD - SPDR Gold Shares)
        # 国内可用 518880.SS (华安黄金ETF)
        gold_ticker = "GLD"  # 美国黄金ETF
        nasdaq_ticker = "QQQ"  # 纳斯达克100 ETF
        
        try:
            # 下载数据
            gold_data = yf.download(gold_ticker, start=start_date, end=end_date, progress=False)
            nasdaq_data = yf.download(nasdaq_ticker, start=start_date, end=end_date, progress=False)
            
            # 重采样为月度数据(每月第一个交易日)
            gold_monthly = gold_data['Close'].resample('MS').first()
            nasdaq_monthly = nasdaq_data['Close'].resample('MS').first()
            
            # 计算月度涨跌幅
            gold_pct = gold_monthly.pct_change()
            nasdaq_pct = nasdaq_monthly.pct_change()
            
            # 合并数据
            df = pd.DataFrame({
                'Date': gold_pct.index,
                'Gold_Pct_Change': gold_pct.values.flatten(),
                'Nasdaq_Pct_Change': nasdaq_pct.values.flatten()
            })
            
            # 删除第一行(NaN)
            df = df.dropna()
            
            # 保存到CSV
            df.to_csv(self.cache_file, index=False)
            print(f"[Success] 数据已保存至 {self.cache_file}")
            print(f"[Info] 数据范围: {df['Date'].min()} 至 {df['Date'].max()}")
            print(f"[Info] 总计 {len(df)} 个月的数据")
            
            return df
            
        except Exception as e:
            print(f"[Error] 数据获取失败: {e}")
            return None
    
    def load_cached_data(self) -> pd.DataFrame:
        """加载缓存的数据"""
        if self.cache_file.exists():
            df = pd.read_csv(self.cache_file)
            df['Date'] = pd.to_datetime(df['Date'])
            return df
        else:
            print("[Warning] 未找到缓存数据,正在获取...")
            return self.fetch_and_process_data()
    
    def get_statistics(self) -> dict:
        """计算统计指标(分位数和均值)"""
        df = self.load_cached_data()
        
        stats = {
            'gold': {
                'mean': df['Gold_Pct_Change'].mean(),
                'p25': df['Gold_Pct_Change'].quantile(0.25),  # 熊市
                'p75': df['Gold_Pct_Change'].quantile(0.75),  # 牛市
                'std': df['Gold_Pct_Change'].std()
            },
            'nasdaq': {
                'mean': df['Nasdaq_Pct_Change'].mean(),
                'p25': df['Nasdaq_Pct_Change'].quantile(0.25),
                'p75': df['Nasdaq_Pct_Change'].quantile(0.75),
                'std': df['Nasdaq_Pct_Change'].std()
            }
        }
        
        return stats


if __name__ == "__main__":
    # 测试代码
    loader = DataLoader()
    
    # 获取数据
    df = loader.fetch_and_process_data("2010-01-01")
    
    # 显示统计信息
    if df is not None:
        stats = loader.get_statistics()
        print("\n[Stats] 统计信息:")
        print(f"黄金 - 均值: {stats['gold']['mean']:.4f}, 25%分位: {stats['gold']['p25']:.4f}, 75%分位: {stats['gold']['p75']:.4f}")
        print(f"纳斯达克 - 均值: {stats['nasdaq']['mean']:.4f}, 25%分位: {stats['nasdaq']['p25']:.4f}, 75%分位: {stats['nasdaq']['p75']:.4f}")
