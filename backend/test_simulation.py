"""
测试模拟引擎
"""
import sys
sys.path.append('..')

from app.services.simulation import SimulationEngine
from app.models.schemas import SimulationScenario

if __name__ == "__main__":
    print("=" * 60)
    print("测试模拟引擎")
    print("=" * 60)
    
    engine = SimulationEngine()
    
    print("\n🚀 开始模拟(均值场景)...")
    results = engine.run_simulation(SimulationScenario.AVERAGE)
    
    print(f"\n" + "=" * 60)
    print("📊 模拟结果汇总")
    print("=" * 60)
    print(f"总月数: {len(results)}")
    print(f"初始总资产: ¥{results[0].total_assets:,.2f}")
    print(f"毕业时总资产: ¥{results[-1].total_assets:,.2f}")
    print(f"资产变化: {((results[-1].total_assets / results[0].total_assets - 1) * 100):.2f}%")
    print(f"\n初始月生活费: ¥{results[0].theoretical_living:,.2f}")
    print(f"最后月生活费: ¥{results[-1].theoretical_living:,.2f}")
    
    # 显示关键时间点
    print(f"\n" + "=" * 60)
    print("🎯 关键时间点检查")
    print("=" * 60)
    
    key_dates = ["2025-12", "2026-09", "2027-09", "2028-09", "2029-06"]
    
    for r in results:
        if r.date in key_dates:
            print(f"\n📅 {r.date}:")
            print(f"  总资产: ¥{r.total_assets:,.2f}")
            print(f"  黄金: ¥{r.gold:,.2f}")
            print(f"  纳指: ¥{r.nasdaq:,.2f}")
            print(f"  稳健: ¥{r.safe:,.2f}")
            print(f"  现金: ¥{r.cash:,.2f}")
            print(f"  纳指成本: ¥{r.nasdaq_cost_basis:,.2f}")
            print(f"  理论生活费: ¥{r.theoretical_living:,.2f}")
            if r.is_vacation:
                print(f"  🏖️ 假期")
    
    # 验证逻辑
    print(f"\n" + "=" * 60)
    print("✅ 逻辑验证")
    print("=" * 60)
    
    # 检查定投是否达到60000
    final_nasdaq_cost = results[-1].nasdaq_cost_basis
    print(f"\n定投检查:")
    print(f"  纳指最终成本: ¥{final_nasdaq_cost:,.2f}")
    print(f"  是否达到目标: {'✅ 是' if final_nasdaq_cost >= 60000 else '❌ 否'}")
    
    # 检查稳健投资在2028年9月后是否为0
    for r in results:
        if r.date >= "2028-10":
            if r.safe > 1:  # 允许小额误差
                print(f"\n⚠️ 警告: {r.date} 稳健投资未完全提取: ¥{r.safe:.2f}")
            break
    else:
        print(f"\n稳健投资提取: ✅ 正常")
    
    print("\n" + "=" * 60)
    print("测试完成!")
    print("=" * 60)
