"""
测试数据加载器
"""
import sys
sys.path.append('..')

from app.data.data_loader import DataLoader

if __name__ == "__main__":
    print("=" * 60)
    print("测试数据加载器")
    print("=" * 60)
    
    loader = DataLoader()
    
    # 获取数据
    print("\n正在获取历史数据...")
    df = loader.fetch_and_process_data("2010-01-01")
    
    if df is not None:
        print(f"\n✅ 数据获取成功!")
        print(f"数据行数: {len(df)}")
        print(f"\n前5行数据:")
        print(df.head())
        
        # 显示统计信息
        stats = loader.get_statistics()
        print("\n" + "=" * 60)
        print("📊 统计信息:")
        print("=" * 60)
        print(f"\n黄金 ETF:")
        print(f"  均值: {stats['gold']['mean']:.4f}")
        print(f"  25%分位(熊市): {stats['gold']['p25']:.4f}")
        print(f"  75%分位(牛市): {stats['gold']['p75']:.4f}")
        print(f"  标准差: {stats['gold']['std']:.4f}")
        
        print(f"\n纳斯达克 ETF:")
        print(f"  均值: {stats['nasdaq']['mean']:.4f}")
        print(f"  25%分位(熊市): {stats['nasdaq']['p25']:.4f}")
        print(f"  75%分位(牛市): {stats['nasdaq']['p75']:.4f}")
        print(f"  标准差: {stats['nasdaq']['std']:.4f}")
    else:
        print("❌ 数据获取失败!")
