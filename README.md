# QuantLife AI - 大学生毕业资产与生活费数学建模系统

## 📖 项目简介

QuantLife AI 是一个专业的财务模拟系统,用于帮助大学生预测从现在到毕业期间的资产变化和每月可支配生活费。系统基于真实的金融数据,通过数学建模模拟不同市场环境(牛市/熊市/均线/历史回测)下的资产表现。

## ✨ 核心功能

- 🎯 **多场景模拟**: 支持牛市、熊市、均线和历史回测四种模拟模式
- 📊 **可视化图表**: 使用 ECharts 展示资产趋势和生活费变化
- 💰 **智能定投**: 自动模拟黄金到纳斯达克的定投策略
- 🏦 **稳健投资管理**: 按年度自动提取稳健投资并转入高收益资产
- 📅 **假期识别**: 准确识别寒暑假,不扣除生活费
- 🔄 **实时数据**: 使用 yfinance 获取真实的历史金融数据

## 🛠️ 技术栈

### 后端
- **FastAPI** - 现代化的 Python Web 框架
- **Pandas** - 数据处理和分析
- **yfinance** - 获取金融市场数据
- **Pydantic** - 数据验证和序列化

### 前端
- **Vue 3** - 渐进式 JavaScript 框架
- **Vite** - 下一代前端构建工具
- **Naive UI** - 优雅的 Vue 3 组件库
- **ECharts** - 强大的数据可视化库
- **Axios** - HTTP 客户端

## 📁 项目结构

```
project-root/
├── backend/                # FastAPI 后端
│   ├── app/
│   │   ├── main.py        # FastAPI 主应用
│   │   ├── models/        # Pydantic 数据模型
│   │   ├── services/      # 业务逻辑(模拟引擎)
│   │   └── data/          # 数据获取与处理
│   ├── requirements.txt   # Python 依赖
│   └── data_cache/        # 历史数据缓存
├── frontend/              # Vue 3 前端
│   ├── src/
│   │   ├── App.vue        # 主组件
│   │   ├── api/           # API 封装
│   │   └── main.js        # 应用入口
│   └── package.json       # Node 依赖
└── README.md
```

## 🚀 快速开始

### 环境要求

- Python 3.8+
- Node.js 16+
- npm 或 yarn

### 后端设置

1. 进入后端目录并安装依赖:
```bash
cd backend
pip install -r requirements.txt
```

2. 启动后端服务:
```bash
# 方式1: 直接运行
python -m app.main

# 方式2: 使用 uvicorn
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

后端将在 `http://localhost:8000` 启动。

### 前端设置

1. 进入前端目录并安装依赖:
```bash
cd frontend
npm install
```

2. 启动开发服务器:
```bash
npm run dev
```

前端将在 `http://localhost:5173` 启动。

## 📊 业务逻辑说明

### 初始资产配置
- **黄金 ETF**: 86,000 元
- **纳斯达克 ETF**: 16,500 元(已投入成本)
- **稳健投资**: 37,600 元(年化 3%)
- **活期现金**: 2,300 元

### 资金流转规则

#### 1. 定投逻辑
- 每月从黄金 ETF 转出 3,150 元(150元/天 × 21个交易日)
- 投入纳斯达克 ETF,直到总成本达到 60,000 元

#### 2. 稳健投资提取
- 2026年9月: 提取 1/3
- 2027年9月: 提取剩余的 1/2
- 2028年9月: 提取全部剩余
- 提取后全部投入纳斯达克 ETF

#### 3. 生活费扣除
- 每月扣除 2,000 元(仅限上学月份)
- **定投期间**: 优先从黄金 ETF 扣除
- **定投完成后**: 按黄金与纳斯达克的市值比例混合扣除

#### 4. 假期规则
- 1月、2月、8月为寒暑假
- 假期期间资产继续增值,但不扣除生活费
- 计算理论生活费时,假期不计入分母

### 模拟场景

- **牛市**: 使用历史收益率的 75% 分位数
- **熊市**: 使用历史收益率的 25% 分位数
- **均线**: 使用历史收益率的平均值
- **历史回测**: 选择历史某个时间点,将之后的涨跌幅映射到未来

## 🎨 界面特性

- 🌈 **现代化设计**: 采用渐变背景和毛玻璃效果
- 📱 **响应式布局**: 适配各种屏幕尺寸
- 🎯 **交互式图表**: 
  - 资产堆叠柱状图,直观展示各资产占比
  - 生活费趋势线,标注基准线和假期区域
- 💡 **智能提示**: 实时计算并展示关键指标

## 📈 使用示例

1. **选择模拟场景**: 在下拉菜单中选择牛市、熊市、均线或历史回测
2. **调整参数**: 如果选择历史回测,可以通过滑块选择起始年份和月份
3. **查看结果**: 系统自动计算并更新图表,展示:
   - 每月总资产变化
   - 理论月均生活费趋势
   - 各资产(黄金、纳指、稳健、现金)的分布

## 🔧 配置说明

### API 基础地址
在 `frontend/src/api/index.js` 中修改:
```javascript
const API_BASE_URL = 'http://localhost:8000';
```

### 数据源
默认使用 yfinance 获取数据:
- 黄金: GLD (SPDR Gold Shares)
- 纳斯达克: QQQ (Nasdaq-100 ETF)

可在 `backend/app/data/data_loader.py` 中修改为其他股票代码。

## 🧪 测试

### 后端测试
```bash
cd backend
python -m app.data.data_loader  # 测试数据获取
python -m app.services.simulation  # 测试模拟引擎
```

### 关键验证点
- 2026/2027/2028年9月稳健投资是否正确提取
- 纳斯达克定投达到60000元后是否停止
- 生活费扣除逻辑是否按定投状态正确切换
- 假期月份是否正确排除在分母外

## 📝 开发路线图

- [x] 后端数据获取模块
- [x] 核心模拟引擎
- [x] FastAPI 接口
- [x] Vue 3 前端框架
- [x] ECharts 图表集成
- [x] 交互式控制面板
- [ ] 数据导出功能(CSV/Excel)
- [ ] 自定义参数配置
- [ ] 移动端适配优化
- [ ] 多语言支持

## 🤝 贡献指南

欢迎提交 Issue 和 Pull Request!

1. Fork 本仓库
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启 Pull Request

## 📄 许可证

本项目采用 MIT 许可证。

## 👨‍💻 作者

QuantLife AI Team

## 🙏 致谢

- [FastAPI](https://fastapi.tiangolo.com/) - 现代化的 Python Web 框架
- [Vue.js](https://vuejs.org/) - 渐进式 JavaScript 框架
- [Naive UI](https://www.naiveui.com/) - 优雅的 Vue 3 组件库
- [ECharts](https://echarts.apache.org/) - 强大的数据可视化库
- [yfinance](https://github.com/ranaroussi/yfinance) - 金融数据获取库

---

**注意**: 本系统仅用于学习和研究目的,模拟结果不构成投资建议。实际投资决策请咨询专业理财顾问。
