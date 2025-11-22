/**
 * API 封装
 * 使用 Axios 调用后端接口
 */
import axios from 'axios';

const API_BASE_URL = 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json',
  },
});

/**
 * 运行模拟
 * @param {Object} params - 模拟参数
 * @param {string} params.scenario - 场景: 'bull', 'bear', 'avg', 'history'
 * @param {number} params.history_start_year - 历史回测起始年份(可选)
 * @param {number} params.history_start_month - 历史回测起始月份(可选)
 * @returns {Promise}
 */
export async function runSimulation(params) {
  try {
    const response = await api.post('/api/simulation/run', params);
    return response.data;
  } catch (error) {
    console.error('模拟请求失败:', error);
    throw error;
  }
}

/**
 * 获取历史数据范围
 * @returns {Promise}
 */
export async function getHistoryRange() {
  try {
    const response = await api.get('/api/meta/history-range');
    return response.data;
  } catch (error) {
    console.error('获取历史数据范围失败:', error);
    throw error;
  }
}

/**
 * 获取统计信息
 * @returns {Promise}
 */
export async function getStatistics() {
  try {
    const response = await api.get('/api/statistics');
    return response.data;
  } catch (error) {
    console.error('获取统计信息失败:', error);
    throw error;
  }
}

export default api;
