from pydantic import BaseModel
from enum import Enum
from typing import List, Optional
from datetime import date

class SimulationScenario(str, Enum):
    BULL = "bull"       # 75% percentile
    BEAR = "bear"       # 25% percentile
    AVERAGE = "avg"     # Mean
    HISTORY = "history" # Historical backtest

class SimulationRequest(BaseModel):
    scenario: SimulationScenario
    history_start_year: Optional[int] = None # Required if scenario is HISTORY

class MonthlyResult(BaseModel):
    date: str
    total_assets: float
    theoretical_living: float
    gold: float
    nasdaq: float
    safe: float
    cash: float
    is_vacation: bool

class SimulationResult(BaseModel):
    results: List[MonthlyResult]
    final_assets: float
    avg_monthly_living: float
