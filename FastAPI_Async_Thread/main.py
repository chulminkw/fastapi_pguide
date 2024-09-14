from fastapi import FastAPI
import asyncio
import time

app = FastAPI()

# long-running I/O-bound 작업 시뮬레이션
async def long_running_task():
    # 특정 초동안 수행 시뮬레이션
    await asyncio.sleep(20)        
    return {"status": "long_running task completed"}
    
@app.get("/task")
async def run_task():
    result = await long_running_task()
    return result

# @app.get("/task")
# async def run_task():
#     time.sleep(20)
#     return {"status": "long_running task completed"}

@app.get("/quick")
async def quick_response():
    return {"status": "quick response"}