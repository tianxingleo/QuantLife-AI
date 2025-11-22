"""
Pydantic数据模型
"""
from pydantic import BaseModel
from typing import List, Optional
from enum import Enum
from datetime import date


class SimulationScenario(str, Enum):
    """模拟场景"""
    BULL = "bull"       # 牛市 (75%分位)
    BEAR = "bear"       # 熊市 (25%分位)
    AVERAGE = "avg"     # 均值
    HISTORY = "history" # 历史回测


class SimulationRequest(BaseModel):
    """模拟请求参数"""
    scenario: SimulationScenario = SimulationScenario.AVERAGE
    history_start_year: Optional[int] = None  # 历史回测的起始年份
    history_start_month: Optional[int] = None  # 历史回测的起始月份


class MonthlyData(BaseModel):
    """每月数据"""
    date: str
    total_assets: float
    theoretical_living: float
    gold: float
    nasdaq: float
    safe: float
    cash: float
    is_vacation: bool
    nasdaq_cost_basis: float  # 纳斯达克累计投入成本


class SimulationResult(BaseModel):
    """模拟结果"""
    monthly_data: List[MonthlyData]
    final_assets: float
    initial_assets: float
    scenario: str
    
    
class HistoryRangeResponse(BaseModel):
    """历史数据范围响应"""
    min_year: int
    max_year: int
    min_month: int
    max_month: int
