from fastapi import FastAPI
from mangum import Mangum
from app.presentation.routers import auth, categories, transactions, budgets, alerts

app = FastAPI(title="FinTrack API")

app.include_router(auth.router)
app.include_router(categories.router)
app.include_router(transactions.router)
app.include_router(budgets.router)
app.include_router(alerts.router)

handler = Mangum(app)  # ← este es el handler que Lambda llama