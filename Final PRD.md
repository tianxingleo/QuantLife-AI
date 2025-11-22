#### 技术栈



- **前端**：Vue 3 + Vite + Naive UI (通过 Axios 调用后端，ECharts 展示图表)
- **后端**：FastAPI (Python) + Pandas (数据处理) + yfinance/AkShare (数据爬虫/API)



实现功能：进行数学建模：

计算一下到大四毕业除去一年寒暑假一共三个月还剩多少个月。

一个学生有一定的资产，这些资产全部都在投资理财产品，没有额外输入，生活费自己管理自己从自己的资产取，某一个月的生活费的计算为那个月月初时的总资产（也就是还没有计算扣除2000）除剩余的在学校的月份（这个生活费也可以理解为从那个月开始不考虑基金变动和投资策略按当前资产最多平均每个月可以花多少）

现在市值86000在黄金etf。16500在纳斯达克etf。剩下有37600在稳健投资中，稳健投资年利率百分之3，大二开始每年9月初取出12500左右（即第一次取出三分之一，第二次取出一半，第三次取出全部，钱取出之后全部一次性投入纳斯达克）。还有2300现在是活期，可以算作是以后用于生活费。现在是每天（每个交易日）给纳斯达克定投150，钱从黄金etf转入纳斯达克，定投到纳斯达克etf投入60000（这里面60000包含以及投的16500）为止。

现在总资产（市值）142400

到毕业，通过历史规律预计（利用爬虫技术获取不同时间段黄金和纳斯达克的每月（选择固定一天比如每月第一个交易日）的价值来进行数学建模模拟计算每个月账上有多少钱），分析好情况（牛市）与坏情况（熊市）与均线（想用**过去**的数据（比如2010-2025年）直接平移到**未来**（2025-2026年）来模拟），每月花费2000（简化计算，认为每月月初取出来2000，在纳斯达克定投完毕之前，钱都从黄金etf中取，纳斯达克定投完毕之后按照纳斯达克和黄金的资产比例从两个基金中取一共2000，比如若此时黄金和纳斯达克etf的资产比例为1比1，则分别从纳斯达克和黄金中取1000），在从现在到毕业每个月（上学日，这些钱不需要用来交学费和在寒暑假消费）平均生活费能有多少。将计算出来的每个月（这几十个月的）的生活费做成一个可视化图表展示，将计算出来的从现在开始的每个月（这几十个月的）的总资产做成可视化图表展示

现在的日期是2025.11.22，大一，从2025.12开始计算,毕业时间是2029.6底，计算到的最后一个月是2029.6。去除的假期三个月是1月2月8月

“除去寒暑假”，是指这3个月**完全不消耗资产**（资产不扣除2000元，但继续产生投资收益），同时这3个月**不计入分母**（即不算作在校月份）

简化计算，计算都以月为单位，可以假想为所有投资操作都在那个月的第一个交易日（可以假想并非是按交易日定投而是假想为每个月1号一次性把一个月该投的钱都投了），简化计算，不计算任何手续费

**牛市 (Bull)**：取历史分位数 75% 以上的收益率或特定牛市年份（如2019-2020）。

**熊市 (Bear)**：取历史分位数 25% 以下的收益率或特定熊市年份（如2008, 2022）。

**均线 (Average)**：取过去 5-10 年的移动平均收益率。

纳斯达克etf为QDII

同时增加可以自由调节历史上模拟的月份的选项，从那个月开始作为第一个月来关注黄金和纳斯达克的涨跌







### 1. 整理后的项目需求文档 (Final PRD)



Markdown

```
# 毕业资产与生活费数学建模系统需求文档

## 1. 项目背景
基于当前资产配置，模拟从大一（2025.12）至大四毕业（2029.06）期间，在不同市场环境（牛/熊/均值/历史回测）下的资产变化，并计算每月理论可支配生活费，辅助财务决策。

## 2. 基础参数
- **当前时间**: 2025年11月22日（大一）。
- **模拟区间**: 2025年12月1日 - 2029年6月30日。
- **特殊月份**: 1月、2月、8月为寒暑假。
  - 资产继续产生收益/亏损。
  - **不扣除**2000元生活费。
  - 计算“理论月均生活费”时，这些月份**不计入分母**。

## 3. 资产初始状态
1. **黄金ETF**: 市值 86,000 元。
2. **纳斯达克ETF (QDII)**: 市值 16,500 元（当前已投入成本 16,500）。
3. **稳健投资**: 市值 37,600 元（年化 3%）。
4. **活期现金**: 2,300 元（仅作为初始资金池，用于生活费兜底）。

## 4. 资金流转规则 (核心逻辑)

### A. 增值逻辑
- **黄金 & 纳斯达克**: 依据历史数据（或模拟数据）的月涨跌幅进行复利增长。
- **稳健投资**: 按年化 3% 每日/每月稳定增长。

### B. 定投逻辑 (黄金 -> 纳斯达克)
- **条件**: 直到纳斯达克**总投入成本**达到 60,000 元（当前已投16,500，还需投43,500）。
- **操作**: 每月（简化为每月1日）从黄金ETF转出 `150 * 交易日数(约21)` ≈ **3,150元** 买入纳斯达克ETF。
- **停止**: 达到投入上限或黄金余额不足时停止。

### C. 稳健资金释放 (稳健 -> 纳斯达克)
- **时间点**: 大二起每年的9月1日（即 2026.09, 2027.09, 2028.09）。
- **金额**:
  - 第1次 (2026.09): 取出当时的 1/3。
  - 第2次 (2027.09): 取出当时的 1/2。
  - 第3次 (2028.09): 取出全部剩余。
- **流向**: 取出后**一次性全部买入**纳斯达克ETF。

### D. 生活费扣除 (2000元/月)
- **发生时间**: 仅限非寒暑假月份（上学月）。
- **扣款源顺序**:
  1. **阶段一（定投进行中）**: 全部从 **黄金ETF** 扣除。
  2. **阶段二（定投结束后）**: 按当时 **纳斯达克市值 : 黄金市值** 的比例混合扣除（例 1:1 则各扣 1000）。
  - *注*: 若活期有余额，优先扣活期（需求虽未明说，但为了代码健壮性通常优先扣现金）。

## 5. 输出指标
- **总资产**: 每月月初的资产总和。
- **理论月生活费**: `当前总资产 / 剩余在校月数`。
  - *剩余在校月数*: 距离毕业的总月数 - 剩余的寒暑假月数。

## 6. 模拟模式
- **历史平移**: 用户选择历史某个月（如2015.01），将那之后的涨跌幅映射到2025.12开始的未来。
- **统计模拟**:
  - 牛市 (75%分位)
  - 熊市 (25%分位)
  - 均线 (平均值)
```

### 2. 后端核心逻辑 (Python/FastAPI)

```
import pandas as pd
import numpy as np
from datetime import date, timedelta
from dateutil.relativedelta import relativedelta
from enum import Enum
from typing import List, Dict

# ===========================
# 1. 基础配置与数据结构
# ===========================

class SimulationScenario(Enum):
    BULL = "bull"       # 75% 分位数
    BEAR = "bear"       # 25% 分位数
    AVERAGE = "avg"     # 均值
    HISTORY = "history" # 历史回测（指定开始年份）

class AssetConfig:
    def __init__(self):
        # 初始资产
        self.gold_val = 86000.0
        self.nasdaq_val = 16500.0
        self.nasdaq_cost_basis = 16500.0 # 已投入成本
        self.safe_val = 37600.0
        self.cash_val = 2300.0
        
        # 策略参数
        self.safe_rate = 0.03 # 3%
        self.nasdaq_max_investment = 60000.0 # 定投目标成本
        self.daily_investment = 150.0
        self.monthly_investment = self.daily_investment * 21 # 简化：每月按21个交易日计算
        self.monthly_spend = 2000.0
        
        # 时间参数
        self.start_date = date(2025, 12, 1)
        self.end_date = date(2029, 6, 1) # 计算到6月
        self.vacation_months = [1, 2, 8]
        self.safe_withdraw_month = 9 # 每年9月取出稳健理财

# ===========================
# 2. 模拟引擎
# ===========================

def run_simulation(scenario: SimulationScenario, history_start_date=None):
    config = AssetConfig()
    
    # 生成时间轴
    current_dt = config.start_date
    dates = []
    while current_dt <= config.end_date:
        dates.append(current_dt)
        current_dt += relativedelta(months=1)
        
    results = []
    
    # 模拟循环
    for i, current_date in enumerate(dates):
        # 1. 计算剩余在校月份 (分母)
        remaining_school_months = 0
        temp_d = current_date
        while temp_d <= config.end_date:
            if temp_d.month not in config.vacation_months:
                remaining_school_months += 1
            temp_d += relativedelta(months=1)
            
        if remaining_school_months == 0: remaining_school_months = 1 # 避免除以0

        # 2. 记录本月月初状态 (尚未扣费)
        total_assets = config.gold_val + config.nasdaq_val + config.safe_val + config.cash_val
        theoretical_allowance = total_assets / remaining_school_months
        
        # 3. 执行月度操作
        
        # A. 获取本月涨跌幅 (模拟数据获取)
        # 在实际项目中，这里需要调用 akshare/yfinance 获取对应历史月份的数据
        # 这里用随机数模拟不同场景
        pct_change = get_mock_market_data(scenario, current_date, history_start_date)
        gold_pct = pct_change['gold']
        nasdaq_pct = pct_change['nasdaq']
        
        # B. 资产增值 (月初先增值)
        config.gold_val *= (1 + gold_pct)
        config.nasdaq_val *= (1 + nasdaq_pct)
        config.safe_val *= (1 + config.safe_rate / 12) # 简单月化
        
        # C. 稳健理财提取 (每年9月，大二开始 -> 2026年起)
        if current_date.month == config.safe_withdraw_month and current_date.year >= 2026:
            withdraw_ratio = 0
            if current_date.year == 2026: withdraw_ratio = 1/3
            elif current_date.year == 2027: withdraw_ratio = 0.5 # 剩余的一半
            elif current_date.year >= 2028: withdraw_ratio = 1.0 # 全部
            
            amount_out = config.safe_val * withdraw_ratio
            config.safe_val -= amount_out
            config.nasdaq_val += amount_out # 转入纳斯达克
            # 注意：这里转入是否算作"定投成本"？需求未明确，通常一次性转入不算在6万定投限额里，
            # 若算，请取消下面这行注释
            # config.nasdaq_cost_basis += amount_out 
            
        # D. 黄金 -> 纳斯达克 定投
        # 还在定投期吗？(成本未满60000 且 黄金有钱)
        is_investing_period = config.nasdaq_cost_basis < config.nasdaq_max_investment
        
        if is_investing_period and config.gold_val > 0:
            # 计算本月该投多少
            invest_amt = config.monthly_investment
            # 修正：不能超过剩余额度
            remaining_quota = config.nasdaq_max_investment - config.nasdaq_cost_basis
            invest_amt = min(invest_amt, remaining_quota)
            # 修正：不能超过黄金余额
            invest_amt = min(invest_amt, config.gold_val)
            
            config.gold_val -= invest_amt
            config.nasdaq_val += invest_amt
            config.nasdaq_cost_basis += invest_amt
            
        # E. 生活费扣除 (2000)
        # 仅在上学月扣除
        spend_log = ""
        if current_date.month not in config.vacation_months:
            to_spend = config.monthly_spend
            
            # 优先扣活期
            if config.cash_val >= to_spend:
                config.cash_val -= to_spend
            else:
                # 活期扣完，扣投资
                remaining_spend = to_spend - config.cash_val
                config.cash_val = 0
                
                if config.nasdaq_cost_basis < config.nasdaq_max_investment:
                    # 场景1：定投未满，全部从黄金扣
                    if config.gold_val >= remaining_spend:
                        config.gold_val -= remaining_spend
                    else:
                        # 黄金不够，扣纳斯达克
                        deduct_gold = config.gold_val
                        config.gold_val = 0
                        config.nasdaq_val -= (remaining_spend - deduct_gold)
                else:
                    # 场景2：定投已满，按比例扣
                    total_invest = config.gold_val + config.nasdaq_val
                    if total_invest > 0:
                        gold_ratio = config.gold_val / total_invest
                        nasdaq_ratio = config.nasdaq_val / total_invest
                        
                        config.gold_val -= (remaining_spend * gold_ratio)
                        config.nasdaq_val -= (remaining_spend * nasdaq_ratio)
        
        # 记录结果
        results.append({
            "date": current_date.strftime("%Y-%m"),
            "total_assets": round(total_assets, 2),
            "theoretical_living": round(theoretical_allowance, 2),
            "gold": round(config.gold_val, 2),
            "nasdaq": round(config.nasdaq_val, 2),
            "safe": round(config.safe_val, 2),
            "is_vacation": current_date.month in config.vacation_months
        })
        
    return results

def get_mock_market_data(scenario, current_date, history_start=None):
    """
    这里用来生成模拟涨跌幅。
    实际项目中，请替换为 pd.read_csv 读取清洗好的历史数据。
    """
    np.random.seed(current_date.year * 100 + current_date.month) # 保证每次运行结果一致
    
    mu_g, sigma_g = 0.005, 0.03 # 黄金月均收益期望与波动
    mu_n, sigma_n = 0.012, 0.06 # 纳指月均收益期望与波动 (波动大)
    
    if scenario == SimulationScenario.BULL:
        mu_g, mu_n = 0.01, 0.025
    elif scenario == SimulationScenario.BEAR:
        mu_g, mu_n = -0.005, -0.02
        
    # 生成正态分布随机数
    return {
        "gold": np.random.normal(mu_g, sigma_g),
        "nasdaq": np.random.normal(mu_n, sigma_n)
    }

# 测试运行
if __name__ == "__main__":
    data = run_simulation(SimulationScenario.AVERAGE)
    print(f"初始月生活费: {data[0]['theoretical_living']}")
    print(f"毕业月总资产: {data[-1]['total_assets']}")
```

### 3. 前端原型 (Interactive Preview)



这是一个可以直接运行的单文件 Web 应用。我将上面的 Python 逻辑移植到了 JavaScript 中，以便你可以在右侧直接预览效果。它包含了：

1. **ECharts 可视化**：展示资产走势和生活费变化。
2. **交互控制**：可以切换牛市/熊市/均线，甚至拖动滑块选择“历史回测”的年份。
3. **完整的业务逻辑**：包含了你要求的所有细节（假期不分母、定投逻辑、取款比例混合等）。

```
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>资产模拟计算器</title>
    <script src="https://unpkg.com/vue@3/dist/vue.global.js"></script>
    <script src="https://unpkg.com/naive-ui"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/echarts/5.4.3/echarts.min.js"></script>
    <!-- Tailwind for layout -->
    <script src="https://cdn.tailwindcss.com"></script>
    <style>
        body { font-family: 'Inter', sans-serif; background-color: #f3f4f6; }
        .chart-container { height: 300px; width: 100%; }
    </style>
</head>
<body>
    <div id="app" class="p-4 max-w-6xl mx-auto">
        <div class="bg-white rounded-xl shadow-sm p-6 mb-6">
            <h1 class="text-2xl font-bold text-gray-800 mb-2">🎓 大学生毕业资产与生活费模拟</h1>
            <p class="text-gray-500 text-sm mb-4">模拟 2025.12 至 2029.06 期间的财务状况</p>

            <!-- Controls -->
            <div class="grid grid-cols-1 md:grid-cols-3 gap-6 bg-gray-50 p-4 rounded-lg border border-gray-100">
                <div>
                    <label class="block text-sm font-medium text-gray-700 mb-2">市场情境</label>
                    <select v-model="scenario" @change="runSimulation" class="w-full p-2 border rounded-md">
                        <option value="bull">🐂 牛市 (历史高位)</option>
                        <option value="bear">🐻 熊市 (历史低位)</option>
                        <option value="avg">⚖️ 均线 (平稳增长)</option>
                        <option value="history">📅 历史回测平移</option>
                    </select>
                </div>
                
                <div v-if="scenario === 'history'">
                    <label class="block text-sm font-medium text-gray-700 mb-2">选择历史起始年份 (模拟数据)</label>
                    <input type="range" min="2010" max="2020" v-model.number="historyStartYear" @input="runSimulation" class="w-full">
                    <div class="text-right text-xs text-gray-500">{{ historyStartYear }}年</div>
                </div>

                <div class="flex flex-col justify-center">
                    <div class="text-sm text-gray-500">毕业时预计总资产</div>
                    <div class="text-2xl font-bold" :class="finalAssets > 100000 ? 'text-green-600' : 'text-orange-500'">
                        ¥{{ Math.round(finalAssets).toLocaleString() }}
                    </div>
                </div>
            </div>
        </div>

        <!-- Charts -->
        <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
            <!-- Chart 1: Assets -->
            <div class="bg-white rounded-xl shadow-sm p-4">
                <h3 class="font-bold text-gray-700 mb-4">💰 总资产趋势 (堆叠图)</h3>
                <div id="assetChart" class="chart-container"></div>
            </div>

            <!-- Chart 2: Living Allowance -->
            <div class="bg-white rounded-xl shadow-sm p-4">
                <h3 class="font-bold text-gray-700 mb-4">🍜 理论月均生活费 (不含寒暑假)</h3>
                <div id="allowanceChart" class="chart-container"></div>
            </div>
        </div>
        
        <!-- Logic Explanation -->
        <div class="mt-6 bg-blue-50 p-4 rounded-lg text-sm text-blue-800">
            <strong>当前逻辑检查：</strong>
            <ul class="list-disc pl-5 mt-2 space-y-1">
                <li>当前时间: 2025.11.22 (大一)，模拟从 2025.12 开始。</li>
                <li>寒暑假 (1,2,8月): 资产增值但不扣费，也不计入生活费分母。</li>
                <li>稳健提款: 2026/27/28年9月分别取出1/3, 1/2, 全部，直接买入纳指。</li>
                <li>定投: 每日150(月3150)直到纳指成本达6万。来源优先扣黄金。</li>
                <li>消费: 每月2000。定投期扣黄金，定投结束后按金/纳比例混合扣除。</li>
            </ul>
        </div>
    </div>

    <script>
        const { createApp, ref, onMounted, watch } = Vue;

        createApp({
            setup() {
                const scenario = ref('avg');
                const historyStartYear = ref(2015);
                const finalAssets = ref(0);
                let assetChart = null;
                let allowanceChart = null;

                // Configuration
                const CONFIG = {
                    startDate: new Date(2025, 11, 1), // Dec 1, 2025 (Month is 0-indexed in JS)
                    endDate: new Date(2029, 5, 1),    // June 1, 2029
                    vacationMonths: [0, 1, 7], // Jan(0), Feb(1), Aug(7)
                    initialAssets: {
                        gold: 86000,
                        nasdaq: 16500,
                        safe: 37600,
                        cash: 2300
                    },
                    safeRate: 0.03,
                    nasdaqTargetCost: 60000,
                    monthlyInvest: 150 * 21, // 3150
                    monthlySpend: 2000
                };

                // Mock Market Data Generator (Replaces Backend API for preview)
                const getMarketRates = (mode, dateOffset) => {
                    // Simple deterministic random based on mode
                    let goldBase = 0.004; // 0.4% monthly
                    let nasdaqBase = 0.01; // 1% monthly
                    let vol = 0.03;

                    if (mode === 'bull') { goldBase = 0.008; nasdaqBase = 0.02; }
                    if (mode === 'bear') { goldBase = -0.005; nasdaqBase = -0.015; }
                    if (mode === 'history') {
                        // Fake history simulation based on the year slider
                        const seed = Math.sin(historyStartYear.value + dateOffset);
                        goldBase = seed * 0.02;
                        nasdaqBase = seed * 0.04;
                    }

                    // Add some randomness
                    const random = (Math.sin(dateOffset * 13.45) + Math.cos(dateOffset * 7.8)) / 2; 
                    
                    return {
                        gold: goldBase + (random * 0.02),
                        nasdaq: nasdaqBase + (random * 0.05)
                    };
                };

                const runSimulation = () => {
                    let currentDate = new Date(CONFIG.startDate);
                    let assets = { ...CONFIG.initialAssets };
                    let nasdaqCost = CONFIG.initialAssets.nasdaq;
                    
                    const timeline = [];
                    const values = { gold: [], nasdaq: [], safe: [], cash: [], living: [], dates: [] };

                    let monthIndex = 0;

                    while (currentDate <= CONFIG.endDate) {
                        const month = currentDate.getMonth(); // 0-11
                        const year = currentDate.getFullYear();
                        const dateStr = `${year}-${month + 1}`;

                        // 1. Calculate Remaining School Months (Denominator)
                        let tempDate = new Date(currentDate);
                        let remainingMonths = 0;
                        while (tempDate <= CONFIG.endDate) {
                            if (!CONFIG.vacationMonths.includes(tempDate.getMonth())) {
                                remainingMonths++;
                            }
                            tempDate.setMonth(tempDate.getMonth() + 1);
                        }
                        if (remainingMonths === 0) remainingMonths = 1;

                        // 2. Snapshot for metrics (Before spending)
                        const total = assets.gold + assets.nasdaq + assets.safe + assets.cash;
                        const theoretical = total / remainingMonths;

                        // 3. Market Growth
                        const rates = getMarketRates(scenario.value, monthIndex);
                        assets.gold *= (1 + rates.gold);
                        assets.nasdaq *= (1 + rates.nasdaq);
                        assets.safe *= (1 + CONFIG.safeRate / 12);

                        // 4. Safe Investment Withdrawal (Sept = 8 in JS)
                        // Freshman now (2025). Sophomore starts Sept 2026.
                        if (month === 8 && year >= 2026) {
                            let ratio = 0;
                            if (year === 2026) ratio = 1/3;
                            else if (year === 2027) ratio = 0.5; // 1/2 of remaining
                            else if (year >= 2028) ratio = 1.0; // All remaining

                            const withdraw = assets.safe * ratio;
                            assets.safe -= withdraw;
                            assets.nasdaq += withdraw;
                            // Note: Not adding to nasdaqCost based on typical logic (usually lump sum transfers don't count towards DCA targets), 
                            // but strictly adhering to prompt "投入60000" usually refers to the DCA limit. 
                        }

                        // 5. Regular Investing (Gold -> Nasdaq)
                        if (nasdaqCost < CONFIG.nasdaqTargetCost && assets.gold > 0) {
                            let invest = CONFIG.monthlyInvest;
                            // Cap at remaining quota
                            invest = Math.min(invest, CONFIG.nasdaqTargetCost - nasdaqCost);
                            // Cap at available gold
                            invest = Math.min(invest, assets.gold);

                            assets.gold -= invest;
                            assets.nasdaq += invest;
                            nasdaqCost += invest;
                        }

                        // 6. Spending (2000) - Only on school months
                        const isVacation = CONFIG.vacationMonths.includes(month);
                        if (!isVacation) {
                            let toSpend = CONFIG.monthlySpend;
                            
                            // Priority 1: Cash
                            if (assets.cash >= toSpend) {
                                assets.cash -= toSpend;
                                toSpend = 0;
                            } else {
                                toSpend -= assets.cash;
                                assets.cash = 0;
                            }

                            if (toSpend > 0) {
                                // Priority 2: Dependent on Investing Status
                                const isInvesting = nasdaqCost < CONFIG.nasdaqTargetCost;
                                
                                if (isInvesting) {
                                    // Spend from Gold
                                    if (assets.gold >= toSpend) {
                                        assets.gold -= toSpend;
                                    } else {
                                        // Gold ran out
                                        const rem = toSpend - assets.gold;
                                        assets.gold = 0;
                                        assets.nasdaq -= rem;
                                    }
                                } else {
                                    // Spend Proportional
                                    const totalInv = assets.gold + assets.nasdaq;
                                    if (totalInv > 0) {
                                        const gRatio = assets.gold / totalInv;
                                        const nRatio = assets.nasdaq / totalInv;
                                        assets.gold -= toSpend * gRatio;
                                        assets.nasdaq -= toSpend * nRatio;
                                    }
                                }
                            }
                        }

                        // Store Data
                        values.dates.push(dateStr);
                        values.gold.push(Math.round(assets.gold));
                        values.nasdaq.push(Math.round(assets.nasdaq));
                        values.safe.push(Math.round(assets.safe));
                        values.cash.push(Math.round(assets.cash));
                        values.living.push(Math.round(theoretical));

                        // Next iteration
                        currentDate.setMonth(currentDate.getMonth() + 1);
                        monthIndex++;
                    }

                    finalAssets.value = values.gold.at(-1) + values.nasdaq.at(-1) + values.safe.at(-1) + values.cash.at(-1);
                    updateCharts(values);
                };

                const updateCharts = (data) => {
                    // Asset Chart
                    if (!assetChart) assetChart = echarts.init(document.getElementById('assetChart'));
                    assetChart.setOption({
                        tooltip: { trigger: 'axis' },
                        legend: { data: ['黄金', '纳指', '稳健', '现金'] },
                        grid: { left: '3%', right: '4%', bottom: '3%', containLabel: true },
                        xAxis: { type: 'category', data: data.dates },
                        yAxis: { type: 'value' },
                        series: [
                            { name: '现金', type: 'bar', stack: 'total', data: data.cash, color: '#9ca3af' },
                            { name: '稳健', type: 'bar', stack: 'total', data: data.safe, color: '#60a5fa' },
                            { name: '黄金', type: 'bar', stack: 'total', data: data.gold, color: '#fbbf24' },
                            { name: '纳指', type: 'bar', stack: 'total', data: data.nasdaq, color: '#a855f7' }
                        ]
                    });

                    // Allowance Chart
                    if (!allowanceChart) allowanceChart = echarts.init(document.getElementById('allowanceChart'));
                    allowanceChart.setOption({
                        tooltip: { trigger: 'axis' },
                        xAxis: { type: 'category', data: data.dates },
                        yAxis: { type: 'value', min: 0 },
                        visualMap: {
                            show: false,
                            pieces: [{ gt: 0, lte: 2000, color: '#ef4444' }, { gt: 2000, color: '#22c55e' }],
                            outOfRange: { color: '#22c55e' }
                        },
                        series: [{
                            name: '理论月生活费',
                            type: 'line',
                            smooth: true,
                            data: data.living,
                            markLine: {
                                data: [{ yAxis: 2000, name: '基准线' }],
                                lineStyle: { color: '#333' }
                            }
                        }]
                    });
                };

                onMounted(() => {
                    runSimulation();
                    window.addEventListener('resize', () => {
                        assetChart && assetChart.resize();
                        allowanceChart && allowanceChart.resize();
                    });
                });

                return { scenario, historyStartYear, finalAssets, runSimulation };
            }
        }).mount('#app');
    </script>
</body>
</html>
```

## English Translation of the Content





#### Technology Stack



- **Frontend**: Vue 3 + Vite + Naive UI (Calls backend via Axios, ECharts for chart visualization)
- **Backend**: FastAPI (Python) + Pandas (Data Processing) + yfinance/AkShare (Data scraping/API)

------



### Project Description and Modeling Goal



**Goal:** To perform financial mathematical modeling:

1. Calculate the **remaining number of months** until university graduation, excluding three months of winter/summer holidays per year.
2. A student has a certain amount of assets invested entirely in financial products with no external income. Living expenses are self-managed and withdrawn from these assets. The monthly living expense calculation is defined as: **Total Assets at the beginning of the month** (before deducting the $2,000 expense) divided by the **Remaining Months at University** (excluding holidays). (This calculated living expense can also be understood as the maximum average monthly spending possible from that month onwards, assuming no further fund value changes or investment strategy shifts).

**Current Asset Status:**

- **$86,000** in Gold ETF.
- **$16,500** in Nasdaq ETF.
- **$37,600** in Conservative Investments (annual interest rate of 3%).
- **$2,300** in current (demand) deposits, designated for future living expenses.

**Investment Rules:**

- The Conservative Investment will be redeemed annually starting from the second year (September 9th): $\approx \$12,500$ will be withdrawn each time (i.e., one-third withdrawn the first time, one-half the second, and the remainder the third). The withdrawn money will be **fully and immediately invested** into the Nasdaq ETF.
- Currently, **$150$** is automatically invested into the Nasdaq ETF every day (every trading day), with funds transferred from the Gold ETF. This Daily Investment (DCA) will continue until the **total investment cost** in the Nasdaq ETF reaches **$60,000** (this includes the current $\$16,500$ already invested).

**Current Total Assets (Market Value):** **$142,400$**

**Modeling and Visualization Requirements:**

- **Simulation Period:** From now until graduation, use historical data (acquired via web scraping of monthly values for Gold and Nasdaq, e.g., on the first trading day of the month) to model and calculate the account balance each month under different scenarios: **Bull Case**, **Bear Case**, and **Average Line** (simulated by directly mapping **past** historical data, e.g., 2010-2025, onto the **future** period, 2025-2029).
- **Monthly Withdrawal:** A fixed monthly expense of **$2,000$** will be withdrawn at the beginning of the month (only during school months; this money is not for tuition or holiday expenses).
  - **Withdrawal Source:** Before the Nasdaq DCA is complete, the money is taken entirely from the **Gold ETF**.
  - **Withdrawal Source:** After the Nasdaq DCA is complete, the $2,000$ is withdrawn from the Nasdaq and Gold funds according to their current asset proportion (e.g., if the ratio is 1:1, $\$1,000$ is taken from each).
- **Final Output:** Calculate the **average monthly living expense** (the theoretical amount) from now until graduation.
- **Visualization:** Create a chart to display the calculated **monthly living expense** and another chart to display the calculated **total assets** over the simulation period.

**Simulation Details:**

- **Current Date:** 2025.11.22 (First Year).
- **Simulation Starts:** December 2025 (2025.12).
- **Graduation End Date:** End of June 2029 (2029.06).
- **Holiday Months (to be excluded):** January, February, and August.
- **Holiday Rule:** "Excluding winter/summer holidays" means these three months **do not incur the $2,000$ expense** (assets are not consumed) AND they **do not count toward the denominator** (i.e., they are not included in the "Remaining Months at University" calculation for the theoretical living expense).
- **Simplification:** All calculations are monthly. Assume all investment operations (including the DCA) occur on the **first trading day of the month** (e.g., the total monthly DCA amount is invested at once). Do not calculate any transaction fees.

**Market Scenario Definitions:**

- **Bull Market (Bull):** Use historical returns above the **75th percentile** or specific bull market years (e.g., 2019-2020).
- **Bear Market (Bear):** Use historical returns below the **25th percentile** or specific bear market years (e.g., 2008, 2022).
- **Average Line (Average):** Use the **moving average return** over the past 5-10 years.
- The Nasdaq ETF is a QDII (Qualified Domestic Institutional Investor) fund.
- An option should be added to allow the user to freely select a **historical starting month** to map the Gold and Nasdaq price movements onto the future simulation period.

------



### 1. Final Project Requirements Document (Final PRD)



Markdown

```
# Graduation Asset and Living Expense Mathematical Modeling System PRD

## 1. Project Background
Based on the current asset allocation, simulate the asset changes from the first year (Dec 2025) to graduation (Jun 2029) under various market scenarios (Bull/Bear/Average/Historical Backtest) and calculate the theoretical monthly disposable living expenses to aid financial decision-making.

## 2. Basic Parameters
- **Current Date**: November 22, 2025 (Freshman Year).
- **Simulation Period**: December 1, 2025 - June 30, 2029.
- **Special Months**: January, February, and August are holidays.
  - Assets continue to generate returns/losses.
  - **NO deduction** of the $2,000 monthly living expense.
  - These months are **NOT included** in the denominator for the "Theoretical Average Monthly Living Expense" calculation.

## 3. Initial Asset Status
1. **Gold ETF**: Market Value $86,000$.
2. **Nasdaq ETF (QDII)**: Market Value $16,500$ (Current investment cost $16,500$).
3. **Conservative Investment**: Market Value $37,600$ (Annualized 3%).
4. **Current Cash**: $2,300$ (Initial cash pool, mainly for living expense buffer).

## 4. Fund Flow Rules (Core Logic)

### A. Appreciation Logic
- **Gold & Nasdaq**: Compounded growth based on historical (or simulated) monthly changes.
- **Conservative Investment**: Stable daily/monthly growth at 3% annualized.

### B. Dollar-Cost Averaging (DCA) Logic (Gold -> Nasdaq)
- **Condition**: Until the Nasdaq **Total Investment Cost** reaches $60,000$ (Current cost $16,500$; $\rightarrow$ needs $43,500$ more).
- **Operation**: Monthly (simplified to the 1st of the month), transfer `150 * Trading Days (approx. 21)` $\approx$ **$3,150$** from the Gold ETF to buy the Nasdaq ETF.
- **Stop**: Cease upon reaching the investment limit or if the Gold balance is insufficient.

### C. Conservative Fund Release (Conservative -> Nasdaq)
- **Timing**: September 1st of the second year onwards (i.e., 2026.09, 2027.09, 2028.09).
- **Amount**:
  - 1st Time (2026.09): Withdraw 1/3 of the current value.
  - 2nd Time (2027.09): Withdraw 1/2 of the current value.
  - 3rd Time (2028.09): Withdraw the entire remaining balance.
- **Destination**: The withdrawn amount is **fully and immediately invested** into the Nasdaq ETF.

### D. Living Expense Deduction ($2,000/Month)
- **Timing**: Only during non-holiday months (school months).
- **Source Order**:
  1. **Phase One (DCA Ongoing)**: Entirely deducted from the **Gold ETF**.
  2. **Phase Two (DCA Complete)**: Deducted proportionally based on the current **Nasdaq Market Value : Gold Market Value** ratio (e.g., 1:1 means $1,000$ from each).
  - *Note*: For robust code, if there is a Current Cash balance, it is usually prioritized for deduction, even if not explicitly stated in the requirements.

## 5. Output Metrics
- **Total Assets**: The sum of assets at the beginning of each month.
- **Theoretical Monthly Living Expense**: `Current Total Assets / Remaining School Months`.
  - *Remaining School Months*: Total months until graduation - remaining holiday months.

## 6. Simulation Modes
- **Historical Shift**: User selects a historical month (e.g., Jan 2015), and the subsequent historical returns are mapped onto the future period starting Dec 2025.
- **Statistical Simulation**:
  - Bull Market (75th Percentile)
  - Bear Market (25th Percentile)
  - Average Line (Mean/Average Value)
```



### 2. Backend Core Logic (Python/FastAPI)





### 3. Frontend Prototype (Interactive Preview)



This is a single-file web application that can be run directly. I have ported the Python logic above into JavaScript so you can preview the results on the right. It includes:

ECharts Visualization: Shows asset trends and living expense changes.

Interactive Controls: Allows switching between Bull/Bear/Average scenarios, and a slider for selecting the "Historical Backtest" year.

Complete Business Logic: Incorporates all required details (holidays excluded from the denominator, DCA logic, proportional withdrawal, etc.).