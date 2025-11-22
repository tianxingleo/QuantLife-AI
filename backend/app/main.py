"""
FastAPI 主应用
提供模拟API接口
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from .models.schemas import (
    SimulationRequest, 
    SimulationResult, 
    HistoryRangeResponse,
    SimulationScenario
)
from .services.simulation import SimulationEngine
from .data.data_loader import DataLoader
import pandas as pd

app = FastAPI(
    title="QuantLife AI - 资产模拟系统",
    description="大学生毕业资产与生活费数学建模系统",
    version="1.0.0"
)

# CORS配置
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 生产环境应该限制具体域名
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 初始化引擎(应用启动时)
engine = None
data_loader = None


@app.on_event("startup")
async def startup_event():
    """应用启动时初始化"""
    global engine, data_loader
    print("🚀 正在启动 QuantLife AI 后端服务...")
    
    data_loader = DataLoader()
    
    # 检查是否有缓存数据,没有则获取
    try:
        data_loader.load_cached_data()
        print("✅ 历史数据已加载")
    except:
        print("⚠️  正在首次获取历史数据,请稍候...")
        data_loader.fetch_and_process_data()
    
    engine = SimulationEngine()
    print("✅ 模拟引擎已就绪")


@app.get("/")
async def root():
    """根路径"""
    return {
        "message": "QuantLife AI - 资产模拟系统",
        "version": "1.0.0",
        "docs": "/docs"
    }


@app.post("/api/simulation/run", response_model=SimulationResult)
async def run_simulation(request: SimulationRequest):
    """
    运行模拟
    
    Args:
        request: 模拟请求参数
        
    Returns:
        模拟结果
    """
    if engine is None:
        raise HTTPException(status_code=503, detail="引擎未就绪")
    
    try:
        # 运行模拟
        monthly_data = engine.run_simulation(
            scenario=request.scenario,
            history_start_year=request.history_start_year,
            history_start_month=request.history_start_month
        )
        
        # 构造结果
        result = SimulationResult(
            monthly_data=monthly_data,
            final_assets=monthly_data[-1].total_assets if monthly_data else 0,
            initial_assets=monthly_data[0].total_assets if monthly_data else 0,
            scenario=request.scenario.value
        )
        
        return result
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"模拟失败: {str(e)}")


@app.get("/api/meta/history-range", response_model=HistoryRangeResponse)
async def get_history_range():
    """
    获取历史数据的时间范围
    用于前端滑块限制
    
    Returns:
        历史数据范围
    """
    if data_loader is None:
        raise HTTPException(status_code=503, detail="数据加载器未就绪")
    
    try:
        df = data_loader.load_cached_data()
        
        min_date = df['Date'].min()
        max_date = df['Date'].max()
        
        return HistoryRangeResponse(
            min_year=min_date.year,
            max_year=max_date.year,
            min_month=min_date.month,
            max_month=max_date.month
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取数据范围失败: {str(e)}")


@app.get("/api/statistics")
async def get_statistics():
    """获取统计信息"""
    if data_loader is None:
        raise HTTPException(status_code=503, detail="数据加载器未就绪")
    
    try:
        stats = data_loader.get_statistics()
        return stats
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取统计信息失败: {str(e)}")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
