import pandas as pd
import numpy as np
from datetime import date, timedelta
from dateutil.relativedelta import relativedelta
from typing import List, Dict
from app.models.models import SimulationScenario, SimulationResult, MonthlyResult
from app.data.data_loader import DataLoader

class AssetConfig:
    def __init__(self):
        # Initial Assets
        self.gold_val = 86000.0
        self.nasdaq_val = 16500.0
        self.nasdaq_cost_basis = 16500.0 # Invested cost
        self.safe_val = 37600.0
        self.cash_val = 2300.0
        
        # Strategy Parameters
        self.safe_rate = 0.03 # 3% annualized
        self.nasdaq_max_investment = 60000.0 # Target cost
        self.daily_investment = 150.0
        self.monthly_investment = self.daily_investment * 21 # Simplified: 21 trading days/month
        self.monthly_spend = 2000.0
        
        # Time Parameters
        self.start_date = date(2025, 12, 1)
        self.end_date = date(2029, 6, 1) # Calculate until June
        self.vacation_months = [1, 2, 8]
        self.safe_withdraw_month = 9 # Withdraw safe investment every Sept

class SimulationEngine:
    def __init__(self):
        self.loader = DataLoader()
        self.stats = self.loader.get_statistics()
        self.history_df = self.loader.load_cached_data()

    def run(self, scenario: SimulationScenario, history_start_year: int = None) -> SimulationResult:
        config = AssetConfig()
        
        # Generate Timeline
        current_dt = config.start_date
        dates = []
        while current_dt <= config.end_date:
            dates.append(current_dt)
            current_dt += relativedelta(months=1)
            
        results = []
        
        # Simulation Loop
        for i, current_date in enumerate(dates):
            # 1. Calculate Remaining School Months (Denominator)
            remaining_school_months = 0
            temp_d = current_date
            while temp_d <= config.end_date:
                if temp_d.month not in config.vacation_months:
                    remaining_school_months += 1
                temp_d += relativedelta(months=1)
                
            if remaining_school_months == 0: remaining_school_months = 1 # Avoid division by zero

            # 2. Snapshot Beginning of Month Status (Before Spending)
            total_assets = config.gold_val + config.nasdaq_val + config.safe_val + config.cash_val
            theoretical_allowance = total_assets / remaining_school_months
            
            # 3. Execute Monthly Operations
            
            # A. Get Monthly Pct Change
            pct_change = self._get_market_data(scenario, current_date, history_start_year, i)
            gold_pct = pct_change['gold']
            nasdaq_pct = pct_change['nasdaq']
            
            # B. Asset Appreciation (Start of Month)
            config.gold_val *= (1 + gold_pct)
            config.nasdaq_val *= (1 + nasdaq_pct)
            config.safe_val *= (1 + config.safe_rate / 12) # Simple monthly rate
            
            # C. Safe Investment Withdrawal (Sept, Sophomore+ -> 2026+)
            if current_date.month == config.safe_withdraw_month and current_date.year >= 2026:
                withdraw_ratio = 0
                if current_date.year == 2026: withdraw_ratio = 1/3
                elif current_date.year == 2027: withdraw_ratio = 0.5 # Half of remaining
                elif current_date.year >= 2028: withdraw_ratio = 1.0 # All remaining
                
                amount_out = config.safe_val * withdraw_ratio
                config.safe_val -= amount_out
                config.nasdaq_val += amount_out # Transfer to Nasdaq
                # Note: Lump sum transfer usually doesn't count towards DCA cost basis limit
                
            # D. Gold -> Nasdaq DCA
            # Is investing period active? (Cost < 60000)
            is_investing_period = config.nasdaq_cost_basis < config.nasdaq_max_investment
            
            if is_investing_period and config.gold_val > 0:
                invest_amt = config.monthly_investment
                # Cap at remaining quota
                remaining_quota = config.nasdaq_max_investment - config.nasdaq_cost_basis
                invest_amt = min(invest_amt, remaining_quota)
                # Cap at gold balance
                invest_amt = min(invest_amt, config.gold_val)
                
                config.gold_val -= invest_amt
                config.nasdaq_val += invest_amt
                config.nasdaq_cost_basis += invest_amt
                
            # E. Living Expense Deduction (2000)
            # Only in school months
            if current_date.month not in config.vacation_months:
                to_spend = config.monthly_spend
                
                # Priority 1: Cash
                if config.cash_val >= to_spend:
                    config.cash_val -= to_spend
                else:
                    # Cash empty, deduct from investments
                    remaining_spend = to_spend - config.cash_val
                    config.cash_val = 0
                    
                    if config.nasdaq_cost_basis < config.nasdaq_max_investment:
                        # Scenario 1: DCA ongoing, deduct all from Gold
                        if config.gold_val >= remaining_spend:
                            config.gold_val -= remaining_spend
                        else:
                            # Gold empty, deduct from Nasdaq
                            deduct_gold = config.gold_val
                            config.gold_val = 0
                            config.nasdaq_val -= (remaining_spend - deduct_gold)
                    else:
                        # Scenario 2: DCA done, deduct proportionally
                        total_invest = config.gold_val + config.nasdaq_val
                        if total_invest > 0:
                            gold_ratio = config.gold_val / total_invest
                            nasdaq_ratio = config.nasdaq_val / total_invest
                            
                            config.gold_val -= (remaining_spend * gold_ratio)
                            config.nasdaq_val -= (remaining_spend * nasdaq_ratio)
            
            # Record Results
            results.append(MonthlyResult(
                date=current_date.strftime("%Y-%m"),
                total_assets=round(total_assets, 2),
                theoretical_living=round(theoretical_allowance, 2),
                gold=round(config.gold_val, 2),
                nasdaq=round(config.nasdaq_val, 2),
                safe=round(config.safe_val, 2),
                cash=round(config.cash_val, 2),
                is_vacation=current_date.month in config.vacation_months
            ))
            
        final_assets = results[-1].total_assets
        avg_living = sum([r.theoretical_living for r in results]) / len(results)
        
        return SimulationResult(
            results=results,
            final_assets=round(final_assets, 2),
            avg_monthly_living=round(avg_living, 2)
        )

    def _get_market_data(self, scenario: SimulationScenario, current_date: date, history_start_year: int, month_index: int) -> dict:
        """Generate monthly pct change based on scenario"""
        
        if scenario == SimulationScenario.HISTORY:
            # Historical Backtest
            if not history_start_year:
                history_start_year = 2015 # Default
                
            # Find corresponding historical date
            # Logic: Map current_date (2025.12) to history_start_year.12
            # month_index 0 -> 2015.12
            # month_index 1 -> 2016.01
            
            start_dt = date(history_start_year, 12, 1) # Start from Dec of that year to match Dec start
            target_date = start_dt + relativedelta(months=month_index)
            
            # Find in dataframe
            # Ensure date format matches
            # The dataframe Date is likely timestamp, we need to match Y-M
            
            # Filter by Year-Month
            mask = (self.history_df['Date'].dt.year == target_date.year) & (self.history_df['Date'].dt.month == target_date.month)
            row = self.history_df[mask]
            
            if not row.empty:
                return {
                    'gold': row.iloc[0]['Gold_Pct_Change'],
                    'nasdaq': row.iloc[0]['Nasdaq_Pct_Change']
                }
            else:
                # Fallback if history out of range: use Average
                return self._get_market_data(SimulationScenario.AVERAGE, current_date, history_start_year, month_index)

        elif scenario == SimulationScenario.BULL:
            return {
                'gold': self.stats['gold']['p75'],
                'nasdaq': self.stats['nasdaq']['p75']
            }
        elif scenario == SimulationScenario.BEAR:
            return {
                'gold': self.stats['gold']['p25'],
                'nasdaq': self.stats['nasdaq']['p25']
            }
        else: # AVERAGE
            return {
                'gold': self.stats['gold']['mean'],
                'nasdaq': self.stats['nasdaq']['mean']
            }
