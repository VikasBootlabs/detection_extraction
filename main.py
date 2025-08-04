from fastapi import FastAPI
from routes.routes import router
from services.latency import RouteLatencyMiddleware

app=FastAPI()
app.add_middleware(RouteLatencyMiddleware)

app.include_router(router=router)