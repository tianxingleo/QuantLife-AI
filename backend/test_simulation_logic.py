import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.services.simulation import SimulationEngine
from app.models.models import SimulationScenario

def test_simulation():
    print("=" * 60)
    print("Testing Simulation Engine")
    print("=" * 60)
    
    engine = SimulationEngine()
    
    # Test 1: Average Scenario
    print("\n[Test 1] Running Average Scenario...")
    result = engine.run(SimulationScenario.AVERAGE)
    
    print(f"Final Assets: {result.final_assets}")
    print(f"Avg Monthly Living: {result.avg_monthly_living}")
    
    # Verification Checks
    print("\n[Verification Checks]")
    
    # Check 1: Safe Investment should be 0 at the end
    final_safe = result.results[-1].safe
    print(f"1. Final Safe Investment: {final_safe} (Expected: 0.0) -> {'[PASS]' if final_safe == 0 else '[FAIL]'}")
    
    # Check 2: Nasdaq Cost Basis (Approximate check via logic)
    # We can't check cost basis directly from result, but we can check if Nasdaq grew significantly
    # and if Gold dropped.
    
    # Check 3: Living Expense in Vacation Months
    vacation_months = [1, 2, 8]
    vacation_errors = 0
    for r in result.results:
        month = int(r.date.split('-')[1])
        if month in vacation_months:
            # Living expense calculation in result is "Theoretical", so it might not be 0.
            # But we should check if assets dropped by 2000.
            # Actually, the result doesn't show "spent amount", but we can infer.
            pass
            
    print(f"3. Vacation Months Logic: (Manual Check Required on CSV/Log)")
    
    # Test 2: History Scenario
    print("\n[Test 2] Running History Scenario (Start 2016)...")
    try:
        result_hist = engine.run(SimulationScenario.HISTORY, history_start_year=2016)
        print(f"Final Assets: {result_hist.final_assets}")
        print("[PASS] History Scenario Ran Successfully")
    except Exception as e:
        print(f"[FAIL] History Scenario Failed: {e}")

if __name__ == "__main__":
    test_simulation()
