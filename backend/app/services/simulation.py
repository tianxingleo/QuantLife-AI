"""
核心模拟引擎
实现资产模拟的所有业务逻辑
"""
import pandas as pd
import numpy as np
from datetime import date, timedelta
from dateutil.relativedelta import relativedelta
from typing import List, Dict, Tuple
from ..models.schemas import SimulationScenario, MonthlyData
from ..data.data_loader import DataLoader


class AssetConfig:
    """资产配置"""
    def __init__(self):
        # 初始资产
        self.gold_val = 86000.0
        self.nasdaq_val = 16500.0
        self.nasdaq_cost_basis = 16500.0  # 已投入成本
        self.safe_val = 37600.0
        self.cash_val = 2300.0
        
        # 策略参数
        self.safe_rate = 0.03  # 稳健投资年化3%
        self.nasdaq_max_investment = 60000.0  # 定投目标成本
        self.daily_investment = 150.0
        self.monthly_investment = self.daily_investment * 21  # 简化:每月21个交易日
        self.monthly_spend = 2000.0
        
        # 时间参数
        self.start_date = date(2025, 12, 1)
        self.end_date = date(2029, 6, 1)
        self.vacation_months = [1, 2, 8]  # 寒暑假月份
        self.safe_withdraw_month = 9  # 每年9月取出稳健理财


class SimulationEngine:
    """模拟引擎"""
    
    def __init__(self):
        self.data_loader = DataLoader()
        self.market_data = self.data_loader.load_cached_data()
        self.stats = self.data_loader.get_statistics()
        
    def calculate_remaining_school_months(self, current_date: date, end_date: date, vacation_months: List[int]) -> int:
        """
        计算剩余在校月份(不包括寒暑假)
        
        Args:
            current_date: 当前日期
            end_date: 结束日期
            vacation_months: 假期月份列表
            
        Returns:
            剩余在校月数
        """
        remaining = 0
        temp_date = current_date
        
        while temp_date <= end_date:
            if temp_date.month not in vacation_months:
                remaining += 1
            temp_date += relativedelta(months=1)
            
        return max(remaining, 1)  # 避免除以0
    
    def get_market_rates(
        self, 
        scenario: SimulationScenario, 
        month_index: int,
        history_start_year: int = None,
        history_start_month: int = None
    ) -> Dict[str, float]:
        """
        获取市场涨跌幅
        
        Args:
            scenario: 模拟场景
            month_index: 当前月份索引(从0开始)
            history_start_year: 历史回测起始年份
            history_start_month: 历史回测起始月份
            
        Returns:
            {'gold': 涨跌幅, 'nasdaq': 涨跌幅}
        """
        if scenario == SimulationScenario.HISTORY:
            # 历史回测模式:直接映射历史数据
            if history_start_year and history_start_month:
                target_date = pd.Timestamp(year=history_start_year, month=history_start_month, day=1)
                target_date += pd.DateOffset(months=month_index)
                
                # 在历史数据中查找
                mask = (self.market_data['Date'].dt.year == target_date.year) & \
                       (self.market_data['Date'].dt.month == target_date.month)
                
                if mask.any():
                    row = self.market_data[mask].iloc[0]
                    return {
                        'gold': row['Gold_Pct_Change'],
                        'nasdaq': row['Nasdaq_Pct_Change']
                    }
        
        # 统计模拟模式
        gold_mu, gold_sigma = 0, self.stats['gold']['std']
        nasdaq_mu, nasdaq_sigma = 0, self.stats['nasdaq']['std']
        
        if scenario == SimulationScenario.BULL:
            # 牛市:使用75%分位数
            gold_mu = self.stats['gold']['p75']
            nasdaq_mu = self.stats['nasdaq']['p75']
        elif scenario == SimulationScenario.BEAR:
            # 熊市:使用25%分位数
            gold_mu = self.stats['gold']['p25']
            nasdaq_mu = self.stats['nasdaq']['p25']
        else:  # AVERAGE
            # 均值
            gold_mu = self.stats['gold']['mean']
            nasdaq_mu = self.stats['nasdaq']['mean']
        
        # 添加一些随机波动(但保持确定性,基于month_index)
        np.random.seed(month_index + 42)
        
        return {
            'gold': gold_mu + np.random.normal(0, gold_sigma * 0.3),
            'nasdaq': nasdaq_mu + np.random.normal(0, nasdaq_sigma * 0.3)
        }
    
    def run_simulation(
        self, 
        scenario: SimulationScenario,
        history_start_year: int = None,
        history_start_month: int = None
    ) -> List[MonthlyData]:
        """
        运行模拟
        
        Args:
            scenario: 模拟场景
            history_start_year: 历史回测起始年份
            history_start_month: 历史回测起始月份
            
        Returns:
            每月数据列表
        """
        config = AssetConfig()
        results = []
        
        current_date = config.start_date
        month_index = 0
        
        while current_date <= config.end_date:
            # 1. 计算剩余在校月份(分母)
            remaining_school_months = self.calculate_remaining_school_months(
                current_date, config.end_date, config.vacation_months
            )
            
            # 2. 记录本月月初状态(尚未扣费和增值)
            total_assets = config.gold_val + config.nasdaq_val + config.safe_val + config.cash_val
            theoretical_allowance = total_assets / remaining_school_months
            
            # 3. 资产增值(月初先增值)
            rates = self.get_market_rates(scenario, month_index, history_start_year, history_start_month)
            config.gold_val *= (1 + rates['gold'])
            config.nasdaq_val *= (1 + rates['nasdaq'])
            config.safe_val *= (1 + config.safe_rate / 12)  # 月化
            
            # 4. 稳健理财提取(每年9月,大二开始->2026年起)
            if current_date.month == config.safe_withdraw_month and current_date.year >= 2026:
                withdraw_ratio = 0
                if current_date.year == 2026:
                    withdraw_ratio = 1/3
                elif current_date.year == 2027:
                    withdraw_ratio = 0.5  # 剩余的一半
                elif current_date.year >= 2028:
                    withdraw_ratio = 1.0  # 全部
                
                amount_out = config.safe_val * withdraw_ratio
                config.safe_val -= amount_out
                config.nasdaq_val += amount_out
                # 注意:这里转入不算在定投成本内(根据需求)
            
            # 5. 黄金->纳斯达克 定投
            is_investing_period = config.nasdaq_cost_basis < config.nasdaq_max_investment
            
            if is_investing_period and config.gold_val > 0:
                invest_amt = config.monthly_investment
                # 不能超过剩余额度
                remaining_quota = config.nasdaq_max_investment - config.nasdaq_cost_basis
                invest_amt = min(invest_amt, remaining_quota)
                # 不能超过黄金余额
                invest_amt = min(invest_amt, config.gold_val)
                
                config.gold_val -= invest_amt
                config.nasdaq_val += invest_amt
                config.nasdaq_cost_basis += invest_amt
            
            # 6. 生活费扣除(2000)
            is_vacation = current_date.month in config.vacation_months
            
            if not is_vacation:
                to_spend = config.monthly_spend
                
                # 优先扣活期
                if config.cash_val >= to_spend:
                    config.cash_val -= to_spend
                else:
                    # 活期扣完,扣投资
                    remaining_spend = to_spend - config.cash_val
                    config.cash_val = 0
                    
                    if config.nasdaq_cost_basis < config.nasdaq_max_investment:
                        # 场景1:定投未满,全部从黄金扣
                        if config.gold_val >= remaining_spend:
                            config.gold_val -= remaining_spend
                        else:
                            # 黄金不够,扣纳斯达克
                            deduct_gold = config.gold_val
                            config.gold_val = 0
                            config.nasdaq_val -= (remaining_spend - deduct_gold)
                    else:
                        # 场景2:定投已满,按比例扣
                        total_invest = config.gold_val + config.nasdaq_val
                        if total_invest > 0:
                            gold_ratio = config.gold_val / total_invest
                            nasdaq_ratio = config.nasdaq_val / total_invest
                            
                            config.gold_val -= (remaining_spend * gold_ratio)
                            config.nasdaq_val -= (remaining_spend * nasdaq_ratio)
            
            # 7. 记录结果
            results.append(MonthlyData(
                date=current_date.strftime("%Y-%m"),
                total_assets=round(total_assets, 2),
                theoretical_living=round(theoretical_allowance, 2),
                gold=round(config.gold_val, 2),
                nasdaq=round(config.nasdaq_val, 2),
                safe=round(config.safe_val, 2),
                cash=round(config.cash_val, 2),
                is_vacation=is_vacation,
                nasdaq_cost_basis=round(config.nasdaq_cost_basis, 2)
            ))
            
            # 8. 下一个月
            current_date += relativedelta(months=1)
            month_index += 1
        
        return results


if __name__ == "__main__":
    # 测试模拟引擎
    engine = SimulationEngine()
    
    print("🚀 开始模拟...")
    results = engine.run_simulation(SimulationScenario.AVERAGE)
    
    print(f"\n📊 模拟结果:")
    print(f"初始总资产: ¥{results[0].total_assets:,.2f}")
    print(f"毕业时总资产: ¥{results[-1].total_assets:,.2f}")
    print(f"初始月生活费: ¥{results[0].theoretical_living:,.2f}")
    print(f"最后月生活费: ¥{results[-1].theoretical_living:,.2f}")
    
    # 显示几个关键时间点
    print(f"\n🎯 关键时间点:")
    for r in results:
        if r.date in ["2026-09", "2027-09", "2028-09", "2029-06"]:
            print(f"{r.date}: 总资产=¥{r.total_assets:,.2f}, 稳健=¥{r.safe:,.2f}, 纳指成本=¥{r.nasdaq_cost_basis:,.2f}")
