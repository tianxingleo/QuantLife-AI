<script setup>
import { ref, onMounted, watch } from 'vue';
import {
  NLayout,
  NLayoutHeader,
  NLayoutContent,
  NCard,
  NSelect,
  NSlider,
  NSpin,
  NGrid,
  NGridItem,
  NStatistic,
  NAlert,
  NSpace,
  NH1,
  NH3,
  NText,
  NIcon,
  useMessage,
} from 'naive-ui';
import * as echarts from 'echarts';
import { runSimulation, getHistoryRange } from './api';

// 消息提示
const message = useMessage();

// 状态管理
const scenario = ref('avg');
const historyStartYear = ref(2015);
const historyStartMonth = ref(1);
const loading = ref(false);
const simulationData = ref(null);
const historyRange = ref(null);

// 图表实例
let assetChart = null;
let allowanceChart = null;

// 场景选项
const scenarioOptions = [
  { label: '🐂 牛市 (历史高位)', value: 'bull' },
  { label: '🐻 熊市 (历史低位)', value: 'bear' },
  { label: '⚖️ 均线 (平稳增长)', value: 'avg' },
  { label: '📅 历史回测平移', value: 'history' },
];

// 月份选项
const monthOptions = Array.from({ length: 12 }, (_, i) => ({
  label: `${i + 1}月`,
  value: i + 1,
}));

// 初始化图表
const initCharts = () => {
  // 资产图表
  const assetChartDom = document.getElementById('assetChart');
  if (assetChartDom) {
    assetChart = echarts.init(assetChartDom);
  }

  // 生活费图表
  const allowanceChartDom = document.getElementById('allowanceChart');
  if (allowanceChartDom) {
    allowanceChart = echarts.init(allowanceChartDom);
  }

  // 响应式调整
  window.addEventListener('resize', () => {
    assetChart?.resize();
    allowanceChart?.resize();
  });
};

// 更新图表
const updateCharts = (data) => {
  const dates = data.monthly_data.map((d) => d.date);
  const gold = data.monthly_data.map((d) => d.gold);
  const nasdaq = data.monthly_data.map((d) => d.nasdaq);
  const safe = data.monthly_data.map((d) => d.safe);
  const cash = data.monthly_data.map((d) => d.cash);
  const living = data.monthly_data.map((d) => d.theoretical_living);

  // 标记寒暑假月份
  const vacationMarks = [];
  data.monthly_data.forEach((d, idx) => {
    if (d.is_vacation) {
      vacationMarks.push([
        { xAxis: idx, yAxis: 0 },
        { xAxis: idx + 1, yAxis: 'max' },
      ]);
    }
  });

  // 资产堆叠图
  assetChart?.setOption({
    title: {
      text: '💰 总资产趋势',
      left: 'center',
      textStyle: {
        fontSize: 18,
        fontWeight: 'bold',
        color: '#1f2937',
      },
    },
    tooltip: {
      trigger: 'axis',
      axisPointer: { type: 'shadow' },
      formatter: (params) => {
        const total = params.reduce((sum, p) => sum + p.value, 0);
        let result = `${params[0].name}<br/>`;
        result += `<strong>总资产: ¥${total.toLocaleString()}</strong><br/>`;
        params.forEach((p) => {
          result += `${p.marker} ${p.seriesName}: ¥${p.value.toLocaleString()}<br/>`;
        });
        return result;
      },
    },
    legend: {
      data: ['现金', '稳健', '黄金', '纳指'],
      bottom: 10,
    },
    grid: {
      left: '3%',
      right: '4%',
      bottom: '15%',
      top: '15%',
      containLabel: true,
    },
    xAxis: {
      type: 'category',
      data: dates,
      axisLabel: {
        rotate: 45,
        fontSize: 10,
      },
    },
    yAxis: {
      type: 'value',
      axisLabel: {
        formatter: (value) => `¥${(value / 1000).toFixed(0)}k`,
      },
    },
    series: [
      {
        name: '现金',
        type: 'bar',
        stack: 'total',
        data: cash,
        itemStyle: { color: '#9ca3af' },
      },
      {
        name: '稳健',
        type: 'bar',
        stack: 'total',
        data: safe,
        itemStyle: { color: '#60a5fa' },
      },
      {
        name: '黄金',
        type: 'bar',
        stack: 'total',
        data: gold,
        itemStyle: { color: '#fbbf24' },
      },
      {
        name: '纳指',
        type: 'bar',
        stack: 'total',
        data: nasdaq,
        itemStyle: { color: '#a855f7' },
      },
    ],
  });

  // 生活费趋势图
  allowanceChart?.setOption({
    title: {
      text: '🍜 理论月均生活费',
      left: 'center',
      textStyle: {
        fontSize: 18,
        fontWeight: 'bold',
        color: '#1f2937',
      },
    },
    tooltip: {
      trigger: 'axis',
      formatter: (params) => {
        const p = params[0];
        const monthData = data.monthly_data[p.dataIndex];
        return `${p.name}<br/>${p.marker} 理论生活费: ¥${p.value.toLocaleString()}<br/>${
          monthData.is_vacation ? '🏖️ <strong>寒暑假(不扣费)</strong>' : ''
        }`;
      },
    },
    grid: {
      left: '3%',
      right: '4%',
      bottom: '15%',
      top: '15%',
      containLabel: true,
    },
    xAxis: {
      type: 'category',
      data: dates,
      axisLabel: {
        rotate: 45,
        fontSize: 10,
      },
    },
    yAxis: {
      type: 'value',
      min: 0,
      axisLabel: {
        formatter: (value) => `¥${value.toLocaleString()}`,
      },
    },
    visualMap: {
      show: false,
      pieces: [
        { gt: 0, lte: 2000, color: '#ef4444' },
        { gt: 2000, color: '#22c55e' },
      ],
    },
    series: [
      {
        name: '理论月生活费',
        type: 'line',
        smooth: true,
        data: living,
        lineStyle: { width: 3 },
        markLine: {
          data: [{ yAxis: 2000, name: '基准线' }],
          lineStyle: { color: '#333', type: 'dashed', width: 2 },
          label: { formatter: '基准 ¥2000' },
        },
        markArea: {
          silent: true,
          itemStyle: {
            color: 'rgba(147, 197, 253, 0.2)',
          },
          data: data.monthly_data
            .map((d, idx) =>
              d.is_vacation
                ? [
                    { xAxis: dates[idx] },
                    { xAxis: dates[Math.min(idx + 1, dates.length - 1)] },
                  ]
                : null
            )
            .filter((d) => d !== null),
        },
      },
    ],
  });
};

// 执行模拟
const executeSimulation = async () => {
  loading.value = true;

  try {
    const params = {
      scenario: scenario.value,
    };

    if (scenario.value === 'history') {
      params.history_start_year = historyStartYear.value;
      params.history_start_month = historyStartMonth.value;
    }

    const result = await runSimulation(params);
    simulationData.value = result;

    // 更新图表
    updateCharts(result);

    message.success('模拟完成');
  } catch (error) {
    message.error('模拟失败: ' + error.message);
    console.error(error);
  } finally {
    loading.value = false;
  }
};

// 获取历史数据范围
const fetchHistoryRange = async () => {
  try {
    const range = await getHistoryRange();
    historyRange.value = range;
    historyStartYear.value = range.min_year;
  } catch (error) {
    console.error('获取历史数据范围失败:', error);
  }
};

// 监听场景变化
watch(scenario, () => {
  executeSimulation();
});

watch([historyStartYear, historyStartMonth], () => {
  if (scenario.value === 'history') {
    executeSimulation();
  }
});

// 组件挂载
onMounted(async () => {
  initCharts();
  await fetchHistoryRange();
  await executeSimulation();
});
</script>

<template>
  <NLayout style="min-height: 100vh; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%)">
    <NLayoutHeader
      style="
        padding: 20px 40px;
        background: rgba(255, 255, 255, 0.95);
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
        backdrop-filter: blur(10px);
      "
    >
      <NH1 style="margin: 0; background: linear-gradient(90deg, #667eea, #764ba2); -webkit-background-clip: text; -webkit-text-fill-color: transparent">
        🎓 QuantLife AI - 资产模拟系统
      </NH1>
      <NText depth="3">模拟 2025.12 至 2029.06 期间的财务状况</NText>
    </NLayoutHeader>

    <NLayoutContent style="padding: 40px">
      <div style="max-width: 1400px; margin: 0 auto">
        <!-- 控制面板 -->
        <NCard
          :bordered="false"
          style="
            margin-bottom: 30px;
            background: rgba(255, 255, 255, 0.95);
            backdrop-filter: blur(10px);
            border-radius: 16px;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
          "
        >
          <NGrid :cols="24" :x-gap="24">
            <!-- 场景选择 -->
            <NGridItem :span="8">
              <div style="margin-bottom: 8px; font-weight: 600">市场情境</div>
              <NSelect v-model:value="scenario" :options="scenarioOptions" size="large" />
            </NGridItem>

            <!-- 历史回测年份 -->
            <NGridItem :span="8" v-if="scenario === 'history' && historyRange">
              <div style="margin-bottom: 8px; font-weight: 600">历史起始年份</div>
              <NSlider
                v-model:value="historyStartYear"
                :min="historyRange.min_year"
                :max="historyRange.max_year"
                :step="1"
                :marks="{ [historyRange.min_year]: String(historyRange.min_year), [historyRange.max_year]: String(historyRange.max_year) }"
              />
            </NGridItem>

            <!-- 历史回测月份 -->
            <NGridItem :span="8" v-if="scenario === 'history'">
              <div style="margin-bottom: 8px; font-weight: 600">起始月份</div>
              <NSelect v-model:value="historyStartMonth" :options="monthOptions" size="large" />
            </NGridItem>

            <!-- 统计卡片 -->
            <NGridItem :span="scenario === 'history' ? 24 : 16">
              <NSpace justify="space-around" style="margin-top: 20px">
                <NStatistic label="初始总资产" tabular-nums>
                  <template #prefix>¥</template>
                  {{ simulationData ? simulationData.initial_assets.toLocaleString() : '142,400' }}
                </NStatistic>
                <NStatistic label="毕业时预计总资产" tabular-nums>
                  <template #prefix>¥</template>
                  <span :style="{ color: simulationData && simulationData.final_assets > 100000 ? '#22c55e' : '#ef4444' }">
                    {{ simulationData ? simulationData.final_assets.toLocaleString() : '0' }}
                  </span>
                </NStatistic>
                <NStatistic label="初始月生活费" tabular-nums>
                  <template #prefix>¥</template>
                  {{ simulationData && simulationData.monthly_data.length > 0 ? simulationData.monthly_data[0].theoretical_living.toLocaleString() : '0' }}
                </NStatistic>
              </NSpace>
            </NGridItem>
          </NGrid>
        </NCard>

        <!-- 图表区域 -->
        <NSpin :show="loading" size="large">
          <NGrid :cols="2" :x-gap="30" :y-gap="30" responsive="screen">
            <!-- 资产图表 -->
            <NGridItem>
              <NCard
                :bordered="false"
                style="
                  background: rgba(255, 255, 255, 0.95);
                  backdrop-filter: blur(10px);
                  border-radius: 16px;
                  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
                "
              >
                <div id="assetChart" style="height: 400px"></div>
              </NCard>
            </NGridItem>

            <!-- 生活费图表 -->
            <NGridItem>
              <NCard
                :bordered="false"
                style="
                  background: rgba(255, 255, 255, 0.95);
                  backdrop-filter: blur(10px);
                  border-radius: 16px;
                  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
                "
              >
                <div id="allowanceChart" style="height: 400px"></div>
              </NCard>
            </NGridItem>
          </NGrid>
        </NSpin>

        <!-- 逻辑说明 -->
        <NAlert
          type="info"
          title="当前逻辑检查"
          style="
            margin-top: 30px;
            background: rgba(59, 130, 246, 0.1);
            backdrop-filter: blur(10px);
            border-radius: 16px;
            border: 1px solid rgba(59, 130, 246, 0.3);
          "
        >
          <ul style="margin: 10px 0; padding-left: 20px">
            <li>当前时间: 2025.11.22 (大一)，模拟从 2025.12 开始</li>
            <li>寒暑假 (1,2,8月): 资产增值但不扣费，也不计入生活费分母</li>
            <li>稳健提款: 2026/27/28年9月分别取出1/3, 1/2, 全部，直接买入纳指</li>
            <li>定投: 每月3150元(150×21交易日)直到纳指成本达6万。来源优先扣黄金</li>
            <li>消费: 每月2000元。定投期扣黄金，定投结束后按金/纳比例混合扣除</li>
          </ul>
        </NAlert>
      </div>
    </NLayoutContent>
  </NLayout>
</template>

<style>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
}

#app {
  width: 100%;
  min-height: 100vh;
}
</style>
