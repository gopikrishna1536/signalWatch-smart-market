"""
FastAPI REST Service for SignalWatch Market Analysis.
"""
from typing import List, Optional
from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel, Field
from .indicators import TechnicalIndicators
from .signals import MarketSignalEngine

app = FastAPI(
    title="SignalWatch Smart Market API",
    description="Quantitative market analysis engine calculating technical indicators and trading signals.",
    version="1.0.0"
)

class PriceSeriesRequest(BaseModel):
    ticker: str = Field(..., example="AAPL")
    prices: List[float] = Field(..., min_length=2, example=[150.0, 152.5, 151.0, 155.0, 158.0])

class IndicatorResponse(BaseModel):
    ticker: str
    indicator: str
    count: int
    data: List[Optional[float]]

@app.get("/health")
def health_check():
    return {"status": "ok", "service": "SignalWatch Smart Market"}

@app.post("/api/indicators/sma", response_model=IndicatorResponse)
def compute_sma(req: PriceSeriesRequest, window: int = Query(5, ge=1)):
    try:
        values = TechnicalIndicators.simple_moving_average(req.prices, window)
        return IndicatorResponse(ticker=req.ticker, indicator=f"SMA_{window}", count=len(values), data=values)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/api/indicators/rsi")
def compute_rsi(req: PriceSeriesRequest, period: int = Query(14, ge=2)):
    try:
        values = TechnicalIndicators.relative_strength_index(req.prices, period)
        condition = MarketSignalEngine.evaluate_rsi_conditions(req.prices, period)
        return {
            "ticker": req.ticker,
            "period": period,
            "rsi_series": values,
            "condition": condition
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/api/indicators/macd")
def compute_macd(req: PriceSeriesRequest, fast: int = Query(12, ge=2), slow: int = Query(26, ge=3), signal: int = Query(9, ge=1)):
    try:
        macd_data = TechnicalIndicators.macd(req.prices, fast, slow, signal)
        return {
            "ticker": req.ticker,
            "fast_period": fast,
            "slow_period": slow,
            "signal_period": signal,
            "data": macd_data
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

class PriceVolumeSeriesRequest(BaseModel):
    ticker: str = Field(..., example="AAPL")
    prices: List[float] = Field(..., min_length=1)
    volumes: List[float] = Field(..., min_length=1)

@app.post("/api/indicators/vwap")
def compute_vwap(req: PriceVolumeSeriesRequest):
    try:
        vwap_series = TechnicalIndicators.vwap(req.prices, req.volumes)
        return {
            "ticker": req.ticker,
            "count": len(vwap_series),
            "vwap_series": vwap_series
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/api/signals/analyze")
def analyze_signals(req: PriceSeriesRequest, fast_window: int = 5, slow_window: int = 20):
    try:
        crossovers = MarketSignalEngine.detect_ma_crossover(req.prices, fast_window, slow_window)
        rsi_eval = MarketSignalEngine.evaluate_rsi_conditions(req.prices)
        return {
            "ticker": req.ticker,
            "data_points": len(req.prices),
            "latest_price": req.prices[-1] if req.prices else None,
            "crossover_signals": crossovers,
            "rsi_analysis": rsi_eval
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
