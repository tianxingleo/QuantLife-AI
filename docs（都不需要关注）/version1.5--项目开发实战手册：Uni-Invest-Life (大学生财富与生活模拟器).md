# 项目开发实战手册：Uni-Invest-Life (大学生财富与生活模拟器)--version1.5





## 1. 项目全景与架构设计 (Architecture Design)





### 1.1 核心设计理念



本项目是一个**混合型应用 (Hybrid Application)**：

- **计算密集型 (Compute Heavy)**：后端的蒙特卡洛模拟需要进行数万次迭代运算。
- **IO 密集型 (I/O Heavy)**：实时获取 ETF 行情数据。
- **交互密集型 (Interaction Heavy)**：前端需要实时响应参数调整并重绘复杂图表。



### 1.2 数据持久化方案 (轻量级混合架构)



根据您的需求，我们摒弃大型数据库，采用 **SQLite + JSON** 的混合存储模式，兼顾性能与便携性。

- **静态配置 (User Config) -> JSON 文件** (`config/user_profile.json`)
  - 存储内容：初始资金、入学/毕业日期、寒暑假区间、学费金额、生活费标准。
  - *理由：结构灵活，前端传参直接覆盖，读写频率低。*
- **市场数据 (Market Data) -> SQLite 数据库** (`data/market.db`)
  - 存储内容：纳指 ETF、黄金 ETF 的历史 OHLC (开高低收) 数据。
  - *理由：时间序列数据量大（数千行），SQL 查询（如 `SELECT \* FROM prices WHERE date > '2020-01-01'`）比 Pandas 解析 CSV 快得多，且支持增量更新。*

------



## 2. 后端开发路径 (FastAPI + Scientific Stack)





### 第一阶段：基础设施与数据层 (Infrastructure & Data)



**目标**：建立 Python 环境，能够从网络获取数据并存入 SQLite。

1. **项目初始化**

   Bash

   ```
   mkdir uni-invest-backend && cd uni-invest-backend
   python -m venv venv
   # Windows: venv\Scripts\activate
   pip install fastapi uvicorn pandas numpy akshare sqlalchemy pydantic loguru
   ```

2. **构建数据获取模块 (`services/market_data.py`)** 使用 `Akshare` (开源财经数据接口) 获取国内场内 ETF 数据（如华安黄金 518880, 国泰纳指 513100）。

   Python

   ```
   import akshare as ak
   import pandas as pd
   import sqlite3
   from datetime import datetime
   
   DB_PATH = "data/market.db"
   
   def init_db():
       """初始化 SQLite 表结构"""
       conn = sqlite3.connect(DB_PATH)
       cursor = conn.cursor()
       cursor.execute('''
           CREATE TABLE IF NOT EXISTS etf_history (
               date TEXT,
               symbol TEXT,
               close REAL,
               PRIMARY KEY (date, symbol)
           )
       ''')
       conn.commit()
       conn.close()
   
   def update_market_data(symbol: str, start_date="20100101"):
       """
       从 Akshare 获取数据并增量更新到 SQLite
       symbol 示例: '518880' (黄金ETF), '513100' (纳指ETF)
       """
       print(f"Fetching data for {symbol}...")
       try:
           # fund_etf_hist_em 接口获取场内ETF历史数据
           df = ak.fund_etf_hist_em(symbol=symbol, start_date=start_date, end_date=datetime.now().strftime("%Y%m%d"))
           # 数据清洗：重命名列，保留需要的字段
           df = df[['日期', '收盘']].rename(columns={'日期': 'date', '收盘': 'close'})
           df['symbol'] = symbol
   
           conn = sqlite3.connect(DB_PATH)
           # 使用 Pandas 的 to_sql 方法，if_exists='append' 实现增量(需处理主键冲突，这里简化为replace或先读后存)
           # 生产环境建议先读取库中最大日期，只下载新数据
           df.to_sql('etf_history', conn, if_exists='append', index=False, method="multi", chunksize=1000) 
       except Exception as e:
           print(f"Error updating {symbol}: {e}")
       finally:
           conn.close()
   ```



### 第二阶段：核心计算引擎 (Core Engine)



**目标**：实现“生活费模拟器”的数学逻辑。这是项目最复杂的部分。

创建一个类 `SimulationEngine`，输入为用户配置，输出为每日资产余额数组。

**核心算法逻辑 (`services/simulation.py`):**

1. **时间轴生成**：利用 Pandas `date_range` 生成从当前到毕业的所有日期。

2. **标记特殊日期**：

   - 创建掩码 `is_holiday`: 如果日期在 `user_config['holidays']` 区间内，标记为 True。
   - 创建掩码 `is_tuition_day`: 每年 9 月 1 日。

3. **向量化计算 vs 循环计算**：

   - *推荐方案*：为了处理复杂的“每日定投 + 账户余额判断”，使用 **Numpy 优化过的循环** 或 **Numba**。纯向量化很难处理“如果余额不足则停止定投”这种路径依赖逻辑。

   Python

   ```
   import numpy as np
   import pandas as pd
   
   def run_simulation(config, market_returns):
       """
       config: 用户配置 (Pydantic Model dict)
       market_returns: DataFrame, 包含历史/模拟的日收益率 (columns: ['gold_ret', 'nasdaq_ret'])
       """
       days = len(market_returns)
   
       # 初始化资产数组
       gold_balance = np.zeros(days)
       nasdaq_balance = np.zeros(days)
       safe_balance = np.zeros(days)
   
       gold_balance = config['assets']['gold']
       nasdaq_balance = config['assets']['nasdaq']
       safe_balance = config['assets']['safe']
   
       # 提取配置
       daily_sip = config['sip']['amount'] # 150元
       sip_limit = config['sip']['limit']  # 40000 or 60000
       monthly_spend = config['expenses']['monthly']
       tuition = config['expenses']['tuition']
   
       # 模拟循环 (Day 1 to End)
       for t in range(1, days):
           current_date = market_returns.index[t]
   
           # 1. 资产随市场波动
           gold_balance[t] = gold_balance[t-1] * (1 + market_returns['gold_ret'].iloc[t])
           nasdaq_balance[t] = nasdaq_balance[t-1] * (1 + market_returns['nasdaq_ret'].iloc[t])
           safe_balance[t] = safe_balance[t-1] * (1 + 0.00005) # 余额宝类固收
   
           # 2. 执行定投 (黄金 -> 纳指)
           # 条件：纳指未达上限 且 黄金余额充足
           if nasdaq_balance[t] < sip_limit and gold_balance[t] >= daily_sip:
               gold_balance[t] -= daily_sip
               nasdaq_balance[t] += daily_sip
   
           # 3. 扣除支出
           # A. 学费 (每年9月1日)
           if current_date.month == 9 and current_date.day == 1:
               # 扣款顺序：稳健 -> 黄金 -> 纳指
               if safe_balance[t] >= tuition:
                   safe_balance[t] -= tuition
               else:
                   #... 级联扣款逻辑...
                   pass
   
           # B. 生活费 (每月1日)
           if current_date.day == 1:
               # 判断是否假期 (需结合 config['holidays'] 判断)
               # spend_amount =...
               safe_balance[t] -= monthly_spend
   
       return pd.DataFrame({
           'gold': gold_balance, 
           'nasdaq': nasdaq_balance, 
           'safe': safe_balance,
           'total': gold_balance + nasdaq_balance + safe_balance
       }, index=market_returns.index)
   ```



### 第三阶段：API 接口开发



**目标**：暴露接口给前端。

1. **`POST /api/simulate`**: 接收前端的大型 JSON 配置，运行模拟，返回用于绘图的 JSON 数据（日期数组，资产曲线数组）。
2. **`GET /api/market/realtime`**: 获取当前最新的 ETF 估值（用于前端 Dashboard 实时展示）。
3. **`WS /ws/status`**: WebSocket 接口，如果需要推送实时计算进度或高频价格变动。

------



## 3. 前端开发路径 (Vue3 + Naive UI)





### 第一阶段：项目搭建与布局



1. **初始化**

   Bash

   ```
   npm create vite@latest uni-invest-frontend -- --template vue-ts
   npm install naive-ui vfonts echarts vue-echarts axios pinia date-fns
   ```

2. **布局设计 (App.vue)** 使用 Naive UI 的 `NLayout` 系统：

   - **Sidebar (`NLayoutSider`)**: 放置所有的输入控件（“控制台”）。
   - **Content (`NLayoutContent`)**: 放置大图表和统计卡片。



### 第二阶段：复杂表单开发 (控制台)



这是用户交互的核心。利用 Naive UI 组件构建配置表单：

- **资产输入**: `NInputNumber` (前缀图标 ¥)，绑定到 Pinia store 中的 `initialAssets`。
- **定投设置**:
  - `NSwitch`: "开启定投"。
  - `NSlider`: 每日定投金额 (0 - 1000)。
  - `NInputNumber`: 止盈/止投上限 (40000/60000)。
- **日期与假期**:
  - `NDatePicker` (Type: `daterange`): 选择寒暑假区间。支持多组区间（动态添加）。
- **模式微调**:
  - `NRadioGroup`: 市场情景选择 ("历史回测", "蒙特卡洛-牛市", "蒙特卡洛-熊市")。



### 第三阶段：可视化与ECharts集成



1. **资产堆叠图 (Stacked Area Chart)**:
   - 展示 黄金、纳指、现金 三种颜色的层叠面积。
   - **视觉重点**：用户能直观看到金色区域（黄金）随着时间推移变薄，蓝色区域（纳指）变厚，而总高度（总资产）在波动中变化。
2. **生活费“安全线”**:
   - 在总资产图上叠加一条红色的虚线，代表“维持生存的最低资金线”（即 剩余月数 * 最低月供）。如果总资产跌破红线，区域变红预警。

------



## 4. 关键功能实现的“黑科技”细节 (Pro Tips)





### A. 关于“排除假期”的算法实现



前端传来的假期是一个数组：`[{start: '2026-01-15', end: '2026-02-20'},...]`。 在后端 Python 中处理时：

1. 创建一个 Pandas `DatetimeIndex`。

2. 编写一个函数 `is_in_vacation(date)`。

3. 更高效的做法：生成一个全长度的 Boolean Series。

   Python

   ```
   # 预先生成每一天是否为假期的掩码
   vacation_mask = pd.Series(False, index=date_range)
   for vac in holidays:
       vacation_mask[vac.start : vac.end] = True
   
   # 在计算生活费时直接查表
   current_spend = base_spend if not vacation_mask[t] else 0
   ```



### B. “联网实时追踪”的实现



为了不因为频繁请求被封 IP，采用 **缓存策略**：

1. 前端请求 `/api/realtime`。
2. 后端检查 Redis (或内存字典) 中是否有 5 分钟内的数据。
3. 如果有，直接返回。
4. 如果没有，调用 Akshare 接口获取最新净值，存入缓存，并返回。
5. *高级玩法*：前端使用 WebSocket 监听，后端后台任务（APScheduler）每 30 秒刷新一次数据并广播给连接的客户端。



### C. 增加“固定时期的临时大额消费”



前端使用 **Naive UI 的 `NDynamicInput`** 组件。 用户可以点击“+”号添加多条记录：

- 日期：2027-06-01
- 金额：8000
- 备注：购买毕业设计电脑

后端接收到一个 `extra_expenses` 列表，在模拟循环中增加一个判断：

Python

```
if current_date_str in extra_expenses_dict:
    safe_balance[t] -= extra_expenses_dict[current_date_str]
```