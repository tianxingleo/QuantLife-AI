# 项目实施路线图 (Implementation Roadmap)

## 0. 项目初始化与目录结构设计

在开始编码前，确立清晰的项目结构。推荐采用 Monorepo 风格或前后端分离目录。

codeText



```
project-root/
├── backend/                # FastAPI (Python)
│   ├── app/
│   │   ├── main.py         # 入口文件
│   │   ├── core/           # 核心配置
│   │   ├── models/         # Pydantic 模型 (数据结构)
│   │   ├── services/       # 业务逻辑 (模拟引擎)
│   │   └── data/           # 数据获取与处理 (AkShare/yfinance)
│   ├── requirements.txt
│   └── data_cache/         # 本地存储清洗后的历史数据(CSV/Parquet)
├── frontend/               # Vue 3 + Vite
│   ├── src/
│   │   ├── components/     # ECharts组件, 控制面板
│   │   ├── api/            # Axios 封装
│   │   └── App.vue
│   └── package.json
└── README.md
```

------



## 第一阶段：数据获取与预处理 (后端)

**目标**：获取黄金和纳斯达克的历史数据，并计算出用于模拟的统计指标（分位数、均值）。

### 1.1 编写爬虫/数据获取脚本

- 
- **工具**：AkShare (国内基金数据方便) 或 yfinance (美股数据方便)。
- **任务**：
  - 
  - 获取 **黄金ETF** (如 518880 或 国际金价) 过去10-15年的日/月数据。
  - 获取 **纳斯达克ETF** (如 513100 或 QQQ/NDX指数) 过去10-15年的日/月数据。
- **具体实现**：
  - 
  - 创建一个 data_loader.py。
  - 将数据重采样 (Resample) 为**月度数据**（取每月第一个交易日的收盘价）。
  - 计算**月度涨跌幅 (Monthly Pct Change)**。

### 1.2 统计分析与数据缓存

- 
- **任务**：基于清洗后的月度涨跌幅，计算 PRD 要求的统计指标。
  - 
  - **牛市阈值**：计算历史涨跌幅的 75% 分位数。
  - **熊市阈值**：计算历史涨跌幅的 25% 分位数。
  - **均值**：计算历史涨跌幅的平均值。
- **输出**：将清洗后的数据保存为 history_data.csv，包含字段：Date, Gold_Pct_Change, Nasdaq_Pct_Change。避免每次重启服务都去爬数据。

------



## 第二阶段：核心模拟引擎开发 (后端)

**目标**：将 PRD 中的复杂业务逻辑转化为 Python 代码。这是项目的核心。

### 2.1 定义数据模型 (Pydantic Models)

在 app/models/ 中定义：

- 
- SimulationRequest: 前端传来的参数（如选择的情景模式、历史回测的开始年份）。
- SimulationResult: 返回给前端的数据结构（包含每月资产列表、生活费列表）。

### 2.2 实现模拟类 SimulationEngine

在 app/services/simulation.py 中编写逻辑（参考 PRD 中的 Python 代码原型，但需增强）：

1. 
2. **初始化状态**：
   - 
   - 设置初始资产：黄金 86000，纳指 16500，稳健 37600，现金 2300。
   - 设置时间轴：2025.12.01 至 2029.06.01。
3. **构建主循环 (按月迭代)**：
   - 
   - **步骤 1：生成涨跌幅**。根据用户选择的模式（牛/熊/均值/历史平移），从第一阶段的 CSV 中读取或生成对应的涨跌幅。
   - **步骤 2：计算分母**。编写函数 calculate_remaining_school_months(current_date)，逻辑必须排除 1月、2月、8月。
   - **步骤 3：资产增值**。应用涨跌幅。
   - **步骤 4：稳健理财赎回**。检查日期是否为 2026/2027/2028 的 9月，执行 1/3, 1/2, All 的赎回逻辑，并转入纳指。
   - **步骤 5：定投逻辑 (重点)**。
     - 
     - 判断 nasdaq_cost_basis < 60000。
     - 从黄金扣除 3150 (或余额)，加到纳指。
   - **步骤 6：生活费扣除 (重点)**。
     - 
     - 判断月份是否为寒暑假。如果是，跳过扣费。
     - 如果不是，执行扣费逻辑（先扣现金 -> 再看定投状态 -> 决定扣黄金还是按比例扣）。
   - **步骤 7：记录状态**。将当月数据 append 到结果列表。

### 2.3 单元测试

- 
- 编写简单的测试脚本，打印出几个关键时间点（如 2026.09, 2029.06）的资产，人工核对是否符合逻辑（例如：稳健理财在2028.10是否应该为0？）。

------



## 第三阶段：API 接口开发 (后端)

**目标**：暴露接口供前端调用。

### 3.1 创建 FastAPI 路由

在 app/main.py 或 app/api/endpoints.py 中：

- 
- GET /api/simulation/run: 接收查询参数 scenario (enum: bull, bear, avg, history) 和 history_start_year。调用引擎，返回 JSON 数据。
- GET /api/meta/history-range: 返回可选的历史年份范围（用于前端滑块限制，例如数据只有 2010-2024，前端滑块就不能选 1990）。

------



## 第四阶段：前端搭建与组件开发 (前端)

**目标**：搭建 Vue3 框架，准备好图表库。

### 4.1 初始化 Vue 项目

- 
- 使用 npm create vite@latest。
- 安装依赖：npm install naive-ui axios echarts vue-echarts。
- 配置 TailwindCSS (可选，建议用于快速布局)。

### 4.2 布局设计

- 
- 使用 Naive UI 的 NLayout, NGrid。
- **顶部/左侧**：控制面板。包含：
  - 
  - 下拉菜单 (Select)：选择情景模式。
  - 滑块 (Slider)：仅在模式为“历史回测”时显示，选择年份。
  - 数据展示卡片：显示“毕业时预计总资产”、“平均月生活费”。
- **主体区域**：放置两个大的图表容器。

### 4.3 封装 Axios

- 
- 创建 src/api/index.js，封装 fetchSimulationData(params) 方法。

------



## 第五阶段：可视化与逻辑对接 (前端)

**目标**：将后端数据渲染到屏幕上。

### 5.1 开发 ECharts 组件

1. 
2. **资产堆叠图 (Stacked Bar Chart)**：
   - 
   - X轴：时间 (2025-12 ~ 2029-06)。
   - Y轴：金额。
   - Series：现金、稳健、黄金、纳指。
   - *细节*：设置 Tooltip trigger 为 axis，方便查看每月总和。
3. **生活费趋势图 (Line Chart)**：
   - 
   - X轴：时间。
   - Y轴：金额。
   - *细节*：添加一条 markLine 在 Y=2000 处，作为基准线。
   - *视觉映射*：可以使用 VisualMap，低于 2000 显示红色，高于 2000 显示绿色。

### 5.2 状态管理与交互

- 
- 在 App.vue 中使用 ref 或 reactive 存储参数。
- 监听下拉菜单和滑块的 change 事件，触发 API 请求。
- 获取数据后，更新 ECharts 的 option。

------



## 第六阶段：优化与验收

**目标**：处理边缘情况，提升用户体验。

### 6.1 细节完善

- 
- **加载状态**：请求 API 时，图表区域显示 Naive UI 的 NSpin 或 Skeleton。
- **日期格式化**：确保后端返回的日期格式（如 "2025-12"）在图表轴上显示美观。
- **寒暑假可视化**：在图表上可以用背景色带（MarkArea）标出每年的 1,2,8 月，直观展示哪些月份是不扣费的。

### 6.2 最终测试

1. 
2. **逻辑验证**：
   - 
   - 选择“均值”模式，手动计算前三个月的变化，核对页面显示。
   - 验证每年9月的稳健理财是否突然减少并转移到了纳指。
   - 验证纳指投入达到 60000 后，黄金是否停止定投。
3. **极端测试**：
   - 
   - 选择极差的熊市，看资产是否会耗尽（代码需处理资产 < 0 的情况，避免崩溃）。

------



## 推荐开发顺序清单 (Checklist)

1. 
2. [后端] 编写 Python 脚本爬取并清洗数据，存为 CSV。
3. [后端] 编写 SimulationEngine 类，实现核心数学逻辑。
4. [后端] 在控制台运行模拟，打印结果，验证逻辑（重点验证定投停止点和9月转账）。
5. [后端] 搭建 FastAPI，打通 /run 接口。
6. [前端] 搭建 Vue + Naive UI 页面骨架。
7. [前端] 调通 API，将返回的 JSON 打印在控制台。
8. [前端] 引入 ECharts，渲染“总资产”和“生活费”图表。
9. [前端] 增加 Slider 和 Select 控件，实现动态刷新图表。
10. [整体] 界面美化与文字说明补充。



# Project Implementation Roadmap

## 0. Project Initialization & Directory Structure

Before coding, establish a clear project structure. A Monorepo style or a standard separated Frontend/Backend structure is recommended.

codeText



```
project-root/
├── backend/                # FastAPI (Python)
│   ├── app/
│   │   ├── main.py         # Entry file
│   │   ├── core/           # Core configuration
│   │   ├── models/         # Pydantic models (Data structures)
│   │   ├── services/       # Business logic (Simulation Engine)
│   │   └── data/           # Data acquisition & processing (AkShare/yfinance)
│   ├── requirements.txt
│   └── data_cache/         # Local storage for cleaned history data (CSV/Parquet)
├── frontend/               # Vue 3 + Vite
│   ├── src/
│   │   ├── components/     # ECharts components, Control panels
│   │   ├── api/            # Axios encapsulation
│   │   └── App.vue
│   └── package.json
└── README.md
```

------



## Phase 1: Data Acquisition & Preprocessing (Backend)

**Goal**: Acquire historical data for Gold and Nasdaq, and calculate statistical metrics (Percentiles, Mean) for the simulation.

### 1.1 Develop Scraper/Data Acquisition Scripts

- 
- **Tools**: AkShare (Convenient for Chinese funds) or yfinance (Convenient for US stocks).
- **Tasks**:
  - 
  - Fetch **Gold ETF** (e.g., 518880 or International Spot Gold) daily/monthly data for the past 10-15 years.
  - Fetch **Nasdaq ETF** (e.g., 513100 or QQQ/NDX Index) daily/monthly data for the past 10-15 years.
- **Implementation Details**:
  - 
  - Create a data_loader.py.
  - **Resample** data to **Monthly Resolution** (take the closing price of the first trading day of each month).
  - Calculate **Monthly Percentage Change**.

### 1.2 Statistical Analysis & Data Caching

- 
- **Tasks**: Calculate the statistical metrics required by the PRD based on the cleaned monthly data.
  - 
  - **Bull Market Threshold**: Calculate the 75th percentile of historical returns.
  - **Bear Market Threshold**: Calculate the 25th percentile of historical returns.
  - **Average**: Calculate the mean of historical returns.
- **Output**: Save the cleaned data as history_data.csv containing fields: Date, Gold_Pct_Change, Nasdaq_Pct_Change. This prevents re-scraping data on every service restart.

------



## Phase 2: Core Simulation Engine (Backend)

**Goal**: Translate the complex business logic from the PRD into Python code. This is the core of the project.

### 2.1 Define Data Models (Pydantic Models)

Define in app/models/:

- 
- SimulationRequest: Parameters sent from the frontend (e.g., selected Scenario, Start Year for historical backtest).
- SimulationResult: Data structure returned to the frontend (List of monthly assets, List of living expenses).

### 2.2 Implement SimulationEngine Class

Write the logic in app/services/simulation.py (referencing the Python prototype in the PRD, but enhanced):

1. 
2. **Initialize State**:
   - 
   - Set initial assets: Gold 86,000, Nasdaq 16,500, Conservative 37,600, Cash 2,300.
   - Set timeline: 2025.12.01 to 2029.06.01.
3. **Build Main Loop (Iterate by Month)**:
   - 
   - **Step 1: Generate Returns**. Read or generate percentage changes based on the user-selected mode (Bull/Bear/Avg/History) using the CSV from Phase 1.
   - **Step 2: Calculate Denominator**. Write function calculate_remaining_school_months(current_date), ensuring logic excludes Jan, Feb, and Aug.
   - **Step 3: Asset Appreciation**. Apply percentage changes to asset values.
   - **Step 4: Conservative Redemption**. Check if the date is September of 2026/2027/28. Execute the 1/3, 1/2, All redemption logic and transfer funds to Nasdaq.
   - **Step 5: DCA Logic (Crucial)**.
     - 
     - Check if nasdaq_cost_basis < 60000.
     - Deduct 3150 (or remaining balance/quota) from Gold and add to Nasdaq.
   - **Step 6: Living Expense Deduction (Crucial)**.
     - 
     - Check if the month is a holiday. If yes, skip deduction.
     - If no, execute deduction logic (Priority: Cash -> Check DCA status -> Deduct from Gold OR Proportional deduction).
   - **Step 7: Record Status**. Append the current month's data to the results list.

### 2.3 Unit Testing

- 
- Write simple test scripts to print assets at key time points (e.g., 2026.09, 2029.06) and manually verify logic (e.g., "Did the Conservative Investment balance hit 0 in Oct 2028?").

------



## Phase 3: API Development (Backend)

**Goal**: Expose endpoints for frontend consumption.

### 3.1 Create FastAPI Routes

In app/main.py or app/api/endpoints.py:

- 
- GET /api/simulation/run: Accepts query parameters scenario (enum: bull, bear, avg, history) and history_start_year. Calls the engine and returns JSON data.
- GET /api/meta/history-range: Returns the available range of historical years (for frontend slider limits, e.g., if data is only available for 2010-2024).

------



## Phase 4: Frontend Setup & Component Development

**Goal**: Set up the Vue 3 framework and prepare the charting library.

### 4.1 Initialize Vue Project

- 
- Use npm create vite@latest.
- Install dependencies: npm install naive-ui axios echarts vue-echarts.
- Configure TailwindCSS (Optional, recommended for rapid layout).

### 4.2 Layout Design

- 
- Use Naive UI's NLayout and NGrid.
- **Top/Left**: Control Panel. Includes:
  - 
  - Select Menu: Choose Market Scenario.
  - Slider: Choose Year (only visible when "Historical Backtest" is selected).
  - Data Cards: Display "Projected Assets at Graduation", "Avg Monthly Allowance".
- **Main Area**: Place two large chart containers.

### 4.3 Encapsulate Axios

- 
- Create src/api/index.js and encapsulate the fetchSimulationData(params) method.

------



## Phase 5: Visualization & Logic Integration (Frontend)

**Goal**: Render backend data onto the screen.

### 5.1 Develop ECharts Components

1. 
2. **Asset Stacked Bar Chart**:
   - 
   - X-Axis: Time (2025-12 ~ 2029-06).
   - Y-Axis: Amount (Currency).
   - Series: Cash, Conservative, Gold, Nasdaq.
   - *Detail*: Set Tooltip trigger to axis for easy viewing of monthly totals.
3. **Living Expense Trend Chart (Line)**:
   - 
   - X-Axis: Time.
   - Y-Axis: Amount.
   - *Detail*: Add a markLine at Y=2000 as the baseline.
   - *Visual Map*: Use VisualMap to color the line Red if < 2000 and Green if > 2000.

### 5.2 State Management & Interaction

- 
- Use ref or reactive in App.vue to store parameters.
- Watch for change events on the Select menu and Slider to trigger API requests.
- Update ECharts option upon receiving data.

------



## Phase 6: Optimization & Acceptance

**Goal**: Handle edge cases and improve user experience.

### 6.1 Refinement

- 
- **Loading State**: Display Naive UI's NSpin or Skeleton while requesting the API.
- **Date Formatting**: Ensure backend date formats (e.g., "2025-12") look clean on chart axes.
- **Holiday Visualization**: Use background colored zones (MarkArea in ECharts) to highlight Jan, Feb, and Aug of each year, visually indicating non-deduction months.

### 6.2 Final Testing

1. 
2. **Logic Verification**:
   - 
   - Select "Average" mode, manually calculate the first 3 months, and verify against the UI.
   - Verify if the Conservative Investment drops suddenly in September each year and shifts to Nasdaq.
   - Verify if Gold DCA stops once Nasdaq investment hits 60,000.
3. **Extreme Testing**:
   - 
   - Select a severe Bear Market scenario to see if assets run out (Code must handle assets < 0 gracefully without crashing).

------



## Recommended Development Checklist

1. 
2. [Backend] Write Python scripts to scrape and clean data; save as CSV.
3. [Backend] Write the SimulationEngine class implementing core math logic.
4. [Backend] Run simulation in the console, print results, and verify logic (focus on DCA stop point and September transfers).
5. [Backend] Set up FastAPI and open the /run endpoint.
6. [Frontend] Set up Vue + Naive UI page skeleton.
7. [Frontend] Connect API and print returned JSON to the browser console.
8. [Frontend] Import ECharts; render "Total Assets" and "Living Expense" charts.
9. [Frontend] Add Slider and Select controls; implement dynamic chart refreshing.
10. [Overall] UI polishing and adding explanatory text/tooltips.