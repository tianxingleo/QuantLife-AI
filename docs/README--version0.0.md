# 🎓 ScholarQuant (智学量化)

> **大学生全周期资产配置与生活费精算系统** *University Student Lifetime Expense & Asset Allocation Simulator*

## 📖 目录

- [1. 项目初衷与现实价值](https://www.google.com/search?q=%231-项目初衷与现实价值)
- [2. 核心功能详述 (MVP)](https://www.google.com/search?q=%232-核心功能详述-mvp)
- [3. 案例演示：2025届新生的财富推演](https://www.google.com/search?q=%233-案例演示2025届新生的财富推演)
- [4. 技术路径与可行性分析](https://www.google.com/search?q=%234-技术路径与可行性分析)
- [5. 头脑风暴与未来扩展](https://www.google.com/search?q=%235-头脑风暴与未来扩展)
- [6. 详细技术实现方案](https://www.google.com/search?q=%236-详细技术实现方案)

## 1. 项目初衷与现实价值

### 💡 设计灵感

大学生活费不仅仅是简单的“收支减法”，而是一个涉及**时间跨度（4年）**、**资产波动（投资）**与**非线性消费（寒暑假）**的复杂数学问题。 很多同学在进行基金定投（如黄金、纳斯达克 ETF）时，往往忽略了**“现金流断裂”**的风险——即虽然资产在增值，但手头没有现金吃饭了。

### 🎯 核心目标

本项目旨在打造一个**数学建模与可视化分析工具**，回答三个问题：

1. **生存底线**：除去学费和假期，我在学校每个月到底能花多少钱？
2. **策略验证**：如果我把手里的黄金通过定投慢慢换成纳斯达克，在这个过程中我的风险敞口有多大？
3. **市场联动**：如果未来四年是牛市/熊市，我的生活质量会有什么变化？

## 2. 核心功能详述 (MVP)

本版本专注于完成以下核心计算与可视化功能：

### 💰 资产与定投模型 (Input)

- **初始持仓录入**：支持输入黄金 ETF、纳斯达克 ETF、稳健理财（如余额宝）的当前市值与持仓成本。
- **高级定投策略**：
  - **资金流向**：支持从“黄金 ETF”逐步卖出并买入“纳斯达克 ETF”（资产轮动）。
  - **定投参数**：设定每日/每周定投金额（如 150元/天）。
  - **智能止盈/止投**：设定目标上限（如“纳指持仓达到 60,000 元停止定投”）。
  - **时间窗口**：自定义定投的起止日期。

### 📅 精细化时间轴与收支 (Timeline)

- **学制设定**：自定义入学年份至毕业年份（精确到日）。
- **假期模式**：
  - 自定义寒暑假时间段（如 1月15日-2月20日）。
  - **排除假期消费开关**：开启后，计算“在校月均生活费”时会自动剔除假期月份，避免平均数失真。
- **收支模型**：
  - **固定收支**：每月固定生活费支出、固定兼职收入。
  - **大额专项**：
    - **学费**：是否包含学费？学费金额多少？（每年9月自动扣除）。
    - **临时大额消费**：支持插入特定日期的支出（如大三买电脑、毕业旅行）。

### 📊 联网分析与可视化 (Output)

- **实时与历史追踪**：
  - 联网获取基金市场（ETF）实时数据，分析当前持仓的最新盈亏。
  - 基于历史股市数据（牛市/熊市/震荡市），回测当前模型在不同市场环境下的表现。
- **核心指标输出**：
  - **在校月均可支配资金**：除去学费、假期开销后，上学期间每个月能花多少钱？
  - **资产变动曲线**：可视化展示黄金减少、纳指增加的过程，以及总资产的波动范围。

## 3. 案例演示：2025届新生的财富推演

> **📝 数据样例背景**
>
> - **当前时间**：2025年11月20日（大一上学期）
> - **用户画像**：2025级新生，距离毕业还有约 43 个月。

### 3.1 初始状态 (Input)

| 资产类型     | 当前市值 (¥) | 收益率表现 | 备注               |
| ------------ | ------------ | ---------- | ------------------ |
| **黄金 ETF** | ***\*,000**  | 📈 +16.8%   | 避险底仓，收益颇丰 |
| **纳指 ETF** | ***\*,500**  | 📉 -1.6%    | 成长仓位，目前微亏 |
| **稳健理财** | ***\*,600**  | 📈 +0.4%    | 生活费蓄水池       |
| **总资产**   | ***\**,100** | -          | -                  |

**策略设定**：

- **定投操作**：每天卖出 ***\**** 元 黄金 ETF $\rightarrow$ 买入 ***\**** 元 纳指 ETF。
- **目标阈值**：直到纳指持仓达到 ***\*,000** 或 ***\*,000** 元时停止定投。

**支出设定**：

- **生活费**：预设每月硬性消费 ***,000** 元。
- **学费/假期**：排除假期消费，资金需优先覆盖未来3年的学费。

### 3.2 模拟分析结果 (Output Simulation)

系统基于历史数据（Historical Data）与蒙特卡洛（Monte Carlo）推演：

- **⏳ 时间计算**：
  - 距离毕业还剩 **43** 个月。
  - 除去每年3个月寒暑假（共约9-10个月），实际**在校月份**约为 **33** 个月。
- **📈 资产推演 (Projected)**：
  - **定投完成时间**：按每日 ***\**** 元计算，约需 **156** 个交易日（约7-8个月）将纳指从 ***.*** 万 加仓至 *** .*** 万。此时黄金将减少约 ***.*** 万 元。
  - **风险提示**：在大二上学期（定投结束期），账户波动率将显著上升。
- **💰 核心结论：每月能花多少钱？**
  - **悲观情况 (Bear Market)**：若未来三年遭遇类似 2022 年的回撤，在保证不破产的前提下，校内月均可支配额为 **¥\*,850**。
  - **中性情况 (Average)**：按历史平均年化计算，校内月均可支配额为 **¥\*,400**。
  - **乐观情况 (Bull Market)**：若科技股持续走牛，毕业时除覆盖所有开销外，预计结余 **¥\**,000+**。

## 4. 技术路径与可行性分析

### 🛠 技术栈选型

- **前端：Vue 3 + Vite + Naive UI**
  - **可行性**：Vue 3 的响应式系统非常适合处理这种“牵一发而动全身”的数值计算。Naive UI 提供了高质量的 `DataPicker` (日期范围) 和 `InputNumber` 组件，非常适合构建金融表单。
- **后端：FastAPI (Python)**
  - **可行性**：Python 是金融量化的母语。使用 `pandas` 处理时间序列（剔除周末、节假日），使用 `numpy` 进行定投的向量化计算，效率极高。FastAPI 能够轻松通过 WebSocket 推送实时股价。

### 🧠 实现难点与解决方案

1. **假期日期的动态排除**：
   - *方案*：建立一个 `TradingCalendar` 类，生成全量的日期序列，利用 `mask` (掩码) 标记出假期和周末，计算生活费时直接 `df[~mask].mean()`。
2. **定投逻辑的路径依赖**：
   - *方案*：由于定投是“每天”发生的，且依赖于“当天”的余额（是否达到6万），这无法简单的向量化。需要使用 Numba 加速的循环，或者在 Python 中优化迭代逻辑。
3. **实时数据获取**：
   - *方案*：接入 `Akshare` 或 `yfinance` 接口。为了防止接口卡顿，后端需设计一个缓存层（Redis/SQLite），每分钟更新一次最新价格，前端只读缓存。



## 5. 详细技术实现方案 (Implementation Steps)

### 1. 后端数据建模 (Pydantic & Schema)

为了确保计算引擎的稳定性，我们需要定义极其严格的数据输入/输出接口。

#### 1.1 策略配置模型 (Input Schema)

前端表单提交的 JSON 数据必须符合以下 Pydantic 模型。这个模型涵盖了资产、定投策略、时间轴和特殊支出。

```
from pydantic import BaseModel, Field
from datetime import date
from typing import List, Literal, Optional

# 定义假期区间
class DateRange(BaseModel):
    start: date
    end: date
    name: str = "寒假/暑假"

# 定义临时大额支出（如：大三买电脑）
class OneTimeExpense(BaseModel):
    date: date
    amount: float
    description: str

# 核心策略配置类
class SimulationConfig(BaseModel):
    # --- 1. 初始资产状态 (2025-11-20) ---
    initial_date: date = Field(..., description="模拟开始日期，通常为今天")
    graduation_date: date = Field(..., description="预期毕业日期")
    
    initial_assets: dict = Field(
        default={
            "gold": 86000.0,   # 黄金 ETF 市值
            "nasdaq": 16500.0, # 纳指 ETF 市值
            "cash": 37600.0    # 稳健理财/现金
        }
    )
    
    # --- 2. 定投策略 (SIP Strategy) ---
    sip_enabled: bool = True
    sip_amount: float = Field(150.0, description="单次定投金额")
    sip_frequency: Literal['daily', 'weekly', 'monthly'] = 'daily'
    sip_source: str = "gold"   # 资金从哪里扣
    sip_target: str = "nasdaq" # 资金买入什么
    sip_cap_target: float = Field(60000.0, description="止投上限：当纳指市值超过此数停止定投")
    
    # --- 3. 消费模型 (Expense Model) ---
    monthly_living_cost: float = 2000.0
    
    exclude_vacation: bool = True
    vacation_periods: List[DateRange] = [] # 前端传入具体的假期时间段
    vacation_living_cost: float = Field(500.0, description="假期时的低保生活费")
    
    include_tuition: bool = True
    tuition_amount: float = 6000.0
    tuition_payment_date: str = "09-01" # 每年9月1日
    
    extra_expenses: List[OneTimeExpense] = [] # 额外的大额支出列表

    # --- 4. 市场模拟参数 ---
    simulation_mode: Literal['historical_backtest', 'monte_carlo'] = 'monte_carlo'
    monte_carlo_simulations: int = 5000 # 模拟次数
```

### 2. 核心计算引擎 (The Simulation Engine)

这是项目的“心脏”。我们需要在一个 `SimulationEngine` 类中实现基于时间步（Time-step）的迭代逻辑。由于涉及复杂的“路径依赖”（即今天的操作取决于昨天的余额），纯向量化（Vectorization）较难实现，这里推荐使用 **Numba 加速的循环** 或 **Pandas 高效迭代**。

#### 2.1 算法伪代码逻辑

```
import pandas as pd
import numpy as np

class Engine:
    def run(self, config: SimulationConfig, market_data):
        # 1. 生成时间轴 (Business Days)
        timeline = pd.date_range(start=config.initial_date, end=config.graduation_date, freq='B')
        days_count = len(timeline)
        
        # 2. 预生成市场收益率矩阵 (Monte Carlo)
        # 形状: (天数, 模拟次数)
        # 使用几何布朗运动 (GBM) 生成纳指和黄金的随机涨跌幅
        gold_returns = self.generate_gbm_paths(days_count, config.monte_carlo_simulations, mu=0.06, sigma=0.15)
        nasdaq_returns = self.generate_gbm_paths(days_count, config.monte_carlo_simulations, mu=0.12, sigma=0.25)
        
        # 3. 初始化账户矩阵 (State Matrix)
        # gold_balance[t, n] 代表第 n 次模拟在第 t 天的黄金余额
        gold_balance = np.zeros((days_count, config.monte_carlo_simulations))
        nasdaq_balance = np.zeros((days_count, config.monte_carlo_simulations))
        cash_balance = np.zeros((days_count, config.monte_carlo_simulations))
        
        # 设置初始值
        gold_balance[0, :] = config.initial_assets['gold']
        nasdaq_balance[0, :] = config.initial_assets['nasdaq']
        cash_balance[0, :] = config.initial_assets['cash']
        
        # 4. 时间步迭代 (核心循环)
        for t in range(1, days_count):
            current_date = timeline[t]
            
            # A. 资产自然增值/贬值
            gold_balance[t] = gold_balance[t-1] * (1 + gold_returns[t])
            nasdaq_balance[t] = nasdaq_balance[t-1] * (1 + nasdaq_returns[t])
            cash_balance[t] = cash_balance[t-1] * (1 + 0.0001) # 余额宝微利
            
            # B. 执行定投策略 (SIP Logic)
            # 向量化判断：哪些模拟路径还没达到止盈线？
            active_mask = nasdaq_balance[t] < config.sip_cap_target
            # 且 黄金余额足够扣款
            fund_mask = gold_balance[t] > config.sip_amount
            # 最终执行掩码
            execute_mask = active_mask & fund_mask
            
            # 执行转仓：黄金减少，纳指增加
            gold_balance[t, execute_mask] -= config.sip_amount
            nasdaq_balance[t, execute_mask] += config.sip_amount
            
            # C. 计算当日应扣生活费 (Expense Logic)
            daily_expense = 0
            
            # C1. 判断是否为学费日 (9月1日)
            if config.include_tuition and current_date.month == 9 and current_date.day == 1:
                daily_expense += config.tuition_amount
                
            # C2. 判断是否为假期 (使用预处理的 holiday_mask 加速)
            if self.is_vacation(current_date, config.vacation_periods):
                if not config.exclude_vacation:
                     daily_expense += config.vacation_living_cost
            else:
                # 在校期间，正常扣费
                daily_expense += config.monthly_living_cost
                
            # C3. 扣除额外大额支出
            extra = self.get_extra_expense(current_date, config.extra_expenses)
            daily_expense += extra
            
            # D. 资金扣除与自动变现 (Waterfall Mechanism)
            # 优先扣现金
            cash_balance[t] -= daily_expense
            
            # 现金若为负，触发变现逻辑
            insolvent_mask = cash_balance[t] < 0
            
            # 第一轮：卖黄金补现金
            shortfall = -cash_balance[t, insolvent_mask] # 缺口金额
            # ... (此处省略具体的向量化补仓代码，逻辑是：min(gold_balance, shortfall)) ...
            
            # 第二轮：卖纳指补现金 (如果黄金卖光了还不够)
            # ...
            
        return {
            "timeline": timeline,
            "gold_paths": gold_balance, 
            "nasdaq_paths": nasdaq_balance,
            "cash_paths": cash_balance
        }
```

### 3. 数据管道与缓存策略 (Data Pipeline)

为了避免重复请求 API 导致封禁，并确保模拟基准（Historical Data）的准确性，我们需要一个轻量级的 ETL 流程。

#### 3.1 SQLite 数据库设计

我们仅需一张核心表来存储清洗后的行情数据。

```
CREATE TABLE IF NOT EXISTS etf_history (
    symbol TEXT NOT NULL,       -- 代码: '518880', '513100'
    date TEXT NOT NULL,         -- 日期: '2023-01-01'
    close REAL,                 -- 收盘价
    daily_return REAL,          -- 预计算的日涨跌幅
    PRIMARY KEY (symbol, date)
);
```

#### 3.2 更新策略 (Python Logic)

```
import akshare as ak
import sqlite3

def fetch_and_cache_market_data(symbol="518880"):
    # 1. 检查数据库最新日期
    last_date = db.query(f"SELECT MAX(date) FROM etf_history WHERE symbol='{symbol}'")
    
    # 2. 如果数据过旧（比如是昨天的），调用 API
    if last_date < today:
        # 调用 Akshare 接口
        df = ak.fund_etf_hist_em(symbol=symbol, start_date=last_date, adjust="qfq")
        
        # 3. 写入数据库
        df.to_sql('etf_history', if_exists='append')
        print(f"Updated {symbol} data.")
```

### 4. 前端架构 (Vue 3 + Naive UI)

前端不仅仅是展示，更是**状态管理器**。

#### 4.1 目录结构

```
frontend/
├── src/
│   ├── api/                # Axios 请求封装
│   ├── components/
│   │   ├── ConfigForm.vue  # 左侧配置面板 (Naive UI Form)
│   │   ├── AssetChart.vue  # ECharts 组件
│   │   └── DataStats.vue   # 关键指标卡片
│   ├── stores/
│   │   └── simulation.ts   # Pinia 状态管理 (存放 assets, simulationResults)
│   ├── utils/
│   │   └── format.ts       # 金额格式化 (¥12,345.00)
│   └── App.vue
```

#### 4.2 关键交互逻辑

- **防抖计算 (Debounce)**: 用户拖动“每日定投金额”滑块时，不要每 1ms 就请求一次后端。使用 `lodash.debounce` 设置 500ms 的延迟，待用户松手后再发送计算请求。
- **Web Worker (可选)**: 如果要在前端进行简单回测，可以将计算逻辑放入 Web Worker，避免阻塞 UI 线程。但在本项目中，主要计算在后端 FastAPI 完成。

### 5. 可视化实现 (ECharts Configuration)

为了直观展示“黄金 -> 纳指”的资金流动，推荐使用 **堆叠河流图 (ThemeRiver)** 或 **堆叠面积图 (Stacked Area)**。

#### ECharts 配置代码片段：

```
option = {
  tooltip: {
    trigger: 'axis',
    axisPointer: { type: 'cross' }
  },
  legend: {
    data: ['纳斯达克 ETF', '黄金 ETF', '稳健理财']
  },
  xAxis: {
    type: 'category',
    boundaryGap: false,
    data: timeline // ['2025-11-20', '2025-11-21', ...]
  },
  yAxis: {
    type: 'value',
    name: '总资产 (CNY)'
  },
  series: [
    {
      name: '纳斯达克 ETF',
      type: 'line',
      stack: 'Total', // 开启堆叠
      areaStyle: {},  // 填充颜色
      data: nasdaq_values,
      color: '#5470C6' // 蓝色
    },
    {
      name: '黄金 ETF',
      type: 'line',
      stack: 'Total',
      areaStyle: {},
      data: gold_values,
      color: '#FFD700' // 金色
    },
    {
      name: '稳健理财',
      type: 'line',
      stack: 'Total',
      areaStyle: {},
      data: cash_values,
      color: '#91CC75' // 绿色
    }
  ]
};
```

### 6. 部署与优化

#### 6.1 Dockerfile

为了确保环境一致性，特别是 numpy/pandas 的版本，使用 Docker 部署是最佳实践。

```
FROM python:3.9-slim

WORKDIR /app

# 安装依赖
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 复制源码
COPY . .

# 暴露端口
EXPOSE 8000

# 启动命令
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

#### 6.2 性能优化点

1. **静态资源压缩**: 前端 Vite build 时开启 Gzip 压缩。
2. **Numba JIT**: 如果蒙特卡洛模拟次数超过 10000 次，给核心循环加上 `@jit(nopython=True)` 装饰器，Python 代码将编译为机器码执行，速度提升 50 倍以上。
3. **Redis 缓存**: 对于相同的输入参数（比如用户未修改配置，只是刷新页面），后端直接返回 Redis 中的计算结果，无需重新运行模拟。