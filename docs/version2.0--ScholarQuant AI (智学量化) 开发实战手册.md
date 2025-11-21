# ScholarQuant AI (智学量化) 开发实战手册 V2.0





## 1. 项目全景与核心价值



**ScholarQuant AI** 不仅仅是一个简单的记账工具，它是一个**智能化的金融数字孪生系统**。它利用蒙特卡洛模拟预测未来，利用实时数据锚定当下，并利用大语言模型（LLM）降低专业门槛，通过自然语言交互帮助大学生进行复杂的资产配置决策。



### 1.1 核心差异化功能 (V2.0 新增)



- **🗣️ 自然语言配置 (Natural Language Configuration)**：用户无需理解复杂的表单，只需说“我有一万块，想一半买黄金一半存余额宝”，AI 自动将其转化为系统参数。
- **🧠 自动化风险研报 (Auto-Insight)**：系统不再只输出冷冰冰的图表，而是生成“人话”版的风险提示，如“⚠️ 警告：你的方案在在大三下学期有 15% 的概率破产”。
- **🌪️ 生成式情景压力测试 (Generative Stress Testing)**：支持“假如明年发生金融危机”这样的假设性提问，AI 自动调整数学模型的参数（漂移率、波动率）进行重新推演。

------



## 2. 系统架构设计 (System Architecture)



采用 **FastAPI + Vue 3** 的前后端分离架构，并新增 **AI Agent Orchestration (AI 编排层)**。



### 2.1 技术栈清单



- **前端 (Frontend)**:
  - 框架: **Vue 3** (Composition API) + **Vite**
  - UI 库: **Naive UI** (极简风格，适合数据密集型应用)
  - 可视化: **ECharts 5** (处理复杂的堆叠图与置信区间带)
  - Markdown 渲染: **Markdown-It** (用于流式渲染 AI 的分析报告)
- **后端 (Backend)**:
  - 核心框架: **FastAPI** (高性能异步支持)
  - AI 编排: **LangChain** 或 **Instructor** (结构化输出控制)
  - 数据计算: **NumPy** + **Pandas** (向量化金融计算)
  - 流式传输: **SSE (Server-Sent Events)** (用于 LLM 打字机效果)
- **数据与存储 (Data & Storage)**:
  - 时序数据: **SQLite** (存储 ETF 历史净值，轻量且支持 SQL)
  - 用户配置: **JSON 文件** (灵活存储复杂的嵌套配置)
  - 向量数据库 (可选): **ChromaDB** (用于 RAG，存储金融知识库)
- **AI 模型层 (Model Layer)**:
  - API 接入: OpenAI (GPT-4o) 或 DeepSeek-R1 (擅长数学与逻辑推理，成本极低)

------



## 3. 核心功能模块实现路径





### 模块一：AI 智能输入解析 (Smart Input Parser)



**痛点解决**：消除填写 20+ 个参数表单的恐惧感。

**实现逻辑**：

1. **定义 Pydantic Schema**：首先定义标准的配置结构。

   Python

   ```
   class UserFinancialProfile(BaseModel):
       initial_capital: float = Field(..., description="初始总资金")
       monthly_living_cost: float
       assets_allocation: Dict[str, float] = Field(..., description="资产分配比例，如 {'GOLD': 0.5, 'CASH': 0.5}")
       risk_tolerance: Literal['conservative', 'balanced', 'aggressive']
   ```

2. **LLM 提取**：后端接收用户文本，使用 `Instructor` 库强制 LLM 输出上述 JSON 格式。

   Python

   ```
   # services/ai_agent.py
   import instructor
   from openai import OpenAI
   
   client = instructor.patch(OpenAI())
   
   def parse_natural_language_input(text: str) -> UserFinancialProfile:
       return client.chat.completions.create(
           model="gpt-4o-mini", # 或 deepseek-chat
           response_model=UserFinancialProfile,
           messages=[
               {"role": "system", "content": "你是一个专业的金融参数提取助手。从用户的口语描述中提取财务配置参数。"},
               {"role": "user", "content": text}
           ]
       )
   ```

3. **前端交互**：用户在输入框输入文本 -> 发送后端 -> 后端返回 JSON -> 前端自动填充到 Naive UI 的表单组件中供用户确认。



### 模块二：金融数学引擎 (Math Engine)



**核心算法**：带跳跃扩散的几何布朗运动 (GBM with Jump Diffusion) 与 现金流折现。

1. **数据获取**：

   - 使用 `Akshare` 获取国内 ETF 数据（如华安黄金 518880，国泰纳指 513100）。
   - **缓存策略**：SQLite 中建立 `market_history` 表，每次计算前检查本地数据是否为最新，非最新则增量更新。

2. **蒙特卡洛模拟核心 (Simulation Loop)**：

   - **时间步长**：按日 (Daily) 迭代，但需处理非交易日（周末/节假日）的资产不变逻辑。

   - **学期/假期掩码**：根据 2025-2026 校历，生成一个 `is_vacation` 布尔数组。

     - *寒假*: 1月中旬 - 2月中旬 (约 4-5 周)
     - *暑假*: 7月 - 8月 (约 8 周)

   - **定投逻辑**：

     Python

     ```
     # 伪代码逻辑
     if is_trading_day and nasdaq_value < target_cap:
         transfer_amount = min(daily_sip, gold_balance)
         gold_balance -= transfer_amount
         nasdaq_balance += transfer_amount
     ```



### 模块三：生成式情景压力测试 (Generative Scenario)



**创新点**：将新闻事件转化为数学参数。

**实现路径**：

1. 用户输入：“如果发生类似 2008 年的金融危机，我的钱能撑多久？”
2. **AI 参数映射**： LLM 接收指令，输出 `ScenarioParams`：
   - `nasdaq_drift`: -0.30 (年化收益率 -30%)
   - `nasdaq_volatility`: 0.45 (波动率激增)
   - `gold_correlation`: 0.60 (危机时刻资产相关性上升)
3. **重运行模拟**：后端使用这组新参数运行 5000 次模拟。
4. **结果对比**：前端在原有的“基准曲线”旁边，绘制一条红色的“压力测试曲线”，直观展示资产枯竭速度的加快。



### 模块四：AI 投资顾问报告 (AI Advisor)



**技术实现：流式响应 (Server-Sent Events)**

1. **数据准备**：将蒙特卡洛模拟的统计结果（中位数、10%分位数、破产月份）序列化为简短文本。

2. **Prompt 设计**：

   > "你是一位犀利但负责任的理财导师。基于以下模拟数据：毕业时资金中位数 2w，破产概率 12%。用户是大一学生。请用幽默警示的口吻点评，并给出 3 条具体建议。"

3. **SSE 接口开发 (FastAPI)**：

   Python

   ```
   from sse_starlette.sse import EventSourceResponse
   
   @app.get("/api/ai/analysis/stream")
   async def stream_analysis(simulation_id: str):
       stats = get_simulation_stats(simulation_id)
       async def event_generator():
           stream = client.chat.completions.create(
               model="deepseek-chat",
               messages=[...],
               stream=True
           )
           for chunk in stream:
               yield chunk.choices.delta.content
       return EventSourceResponse(event_generator())
   ```

4. **前端渲染**：使用 `fetch` 或 `EventSource` 接收流，利用 `markdown-it` 实时渲染 HTML，实现类似 ChatGPT 的逐字生成体验。

------



## 4. 数据库设计 (SQLite + JSON)



保持轻量级，无需部署庞大的 MySQL。



### 4.1 SQLite Schema (`market_data.db`)



用于存储清洗后的金融时间序列，支持 Pandas 高速读取。

SQL

```
CREATE TABLE etf_daily (
    date TEXT,          -- YYYY-MM-DD
    symbol TEXT,        -- 代码, e.g. '518880'
    close REAL,         -- 复权收盘价
    daily_return REAL,  -- 日收益率
    PRIMARY KEY (date, symbol)
);
-- 索引优化查询速度
CREATE INDEX idx_symbol_date ON etf_daily(symbol, date);
```



### 4.2 JSON Config (`user_profiles/`)



每个用户的配置存为一个 JSON 文件，便于导出和备份。

JSON

```
{
  "profile_name": "我的大学理财计划",
  "timeline": {
    "start": "2025-09-01",
    "end": "2029-06-30",
    "vacation_mode": "low_spend" // 假期低消费模式
  },
  "assets": {
    "initial": {"gold": 86000, "nasdaq": 16500, "cash": 37600},
    "sip_strategy": {
      "source": "gold",
      "target": "nasdaq",
      "amount": 150,
      "cap": 60000
    }
  },
  "ai_scenarios": [
    {"name": "2008危机复刻", "drift_adj": -0.3}
  ]
}
```

------



## 5. 开发阶段规划 (Roadmap)





### 阶段 1: 核心数据与数学层 (Week 1-2)



- **目标**: Python 脚本能跑通模拟，画出静态图。
- **任务**:
  - 搭建 FastAPI 项目骨架。
  - 编写 `Akshare` 数据获取脚本，填充 SQLite。
  - 实现 `MonteCarloEngine` 类，完成含定投逻辑的路径生成算法。



### 阶段 2: 基础前后端对接 (Week 3-4)



- **目标**: 网页能通过表单控制模拟参数，并展示 ECharts 图表。
- **任务**:
  - 初始化 Vue3 + Naive UI 项目。
  - 实现 `POST /simulate` 接口，返回 JSON 格式的路径数据。
  - 前端集成 ECharts，绘制“资产河流图”与“生活费水位线”。



### 阶段 3: AI 智能增强 (Week 5-6) **(重点)**



- **目标**: 让系统“听得懂人话，说得出建议”。
- **任务**:
  - 集成 OpenAI/DeepSeek SDK。
  - 开发 **"智能配置助手"**：实现文本转 JSON 的 Pydantic 提取逻辑。
  - 开发 **"AI 投顾"**：实现 SSE 流式接口，前端增加打字机效果组件。



### 阶段 4: 实时化与优化 (Week 7)



- **目标**: 引入实时行情与 WebSocket。
- **任务**:
  - 后端增加 `APScheduler` 定时任务，每 5 分钟抓取一次最新 ETF 价格。
  - 前端增加 WebSocket 连接，实时跳动显示当前资产总值。
  - 增加“假期模式”开关，精细化控制寒暑假的消费逻辑。

------



## 6. 关键代码片段 (Snippets)





### 6.1 前端 SSE 流式接收 AI 分析 (Vue 3)



JavaScript

```
// components/AIAnalysisCard.vue
<script setup>
import { ref } from 'vue'
import { fetchEventSource } from '@microsoft/fetch-event-source'
import MarkdownIt from 'markdown-it'

const md = new MarkdownIt()
const analysisContent = ref('')
const isAnalyzing = ref(false)

const startAnalysis = async (simulationResult) => {
    isAnalyzing.value = true
    analysisContent.value = ''
    
    await fetchEventSource('/api/ai/analysis/stream', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ stats: simulationResult.stats }),
        onmessage(msg) {
            // 累加 AI 返回的字符，实现流式显示
            analysisContent.value += msg.data
        },
        onclose() {
            isAnalyzing.value = false
        }
    })
}
</script>

<template>
    <n-card title="🤖 AI 风险研报">
        <div v-if="analysisContent" v-html="md.render(analysisContent)" class="markdown-body"></div>
        <n-skeleton v-else-if="isAnalyzing" text :repeat="3" />
    </n-card>
</template>
```



### 6.2 后端 AI 场景参数映射 (Python/Instructor)



Python

```
# services/scenario_generator.py
from pydantic import BaseModel, Field

class MarketScenario(BaseModel):
    description: str = Field(..., description="场景描述")
    nasdaq_annual_return: float = Field(..., description="纳斯达克预期年化收益率 (e.g. -0.20 for -20%)")
    nasdaq_volatility: float = Field(..., description="纳斯达克年化波动率")
    gold_safe_haven_effect: bool = Field(..., description="黄金是否发挥避险属性(上涨)")

def generate_stress_test_params(user_prompt: str):
    """
    将用户口语 "如果发生像2000年那样的科技股泡沫破裂" 
    转换为具体的数学模拟参数
    """
    # 调用 LLM 进行参数转换...
    pass
```

------



## 7. 总结



**ScholarQuant AI** 项目通过引入生成式 AI，彻底改变了传统量化工具“难上手、难解释”的弊端。

- **技术层面**：涵盖了 FastAPI 异步处理、SSE 流式传输、金融时间序列数据库设计等高阶全栈技能。
- **业务层面**：完美融合了 **GBM 随机过程**（底层的数学真理）与 **LLM**（上层的交互与解释），为大学生提供了一个既严谨又温情的财富管理助手。

这是一个非常适合作为毕业设计或求职作品集的项目，它展示了你对**金融工程**、**全栈开发**以及**前沿 AI 应用**的综合驾驭能力。