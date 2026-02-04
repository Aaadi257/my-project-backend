from fastapi import FastAPI, HTTPException, Depends, Query
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from fastapi.responses import FileResponse
import os
from datetime import datetime
import tempfile
import openpyxl
from typing import List

from models import (
    Base,
    ScorecardDB,
    MetricsInput,
    ScorecardCreate,
    ScorecardResponse,
    Breakdown,
)
import logic

app = FastAPI(title="Manager Reward System")

# =========================
# Database Setup
# =========================
SQLALCHEMY_DATABASE_URL = "sqlite:///./rewards.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)

Base.metadata.create_all(bind=engine)

# =========================
# CORS (PRODUCTION SAFE)
# =========================
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "https://my-project-frontend-hazel.vercel.app",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# =========================
# Dependency
# =========================
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# =========================
# Logic
# =========================
def calculate_breakdown(m: MetricsInput) -> Breakdown:
    return Breakdown(
        google_score=logic.calculate_google_rating_score(
            m.google_rating_amritsari,
            m.google_rating_chennai,
        ),
        zomato_swiggy_score=logic.calculate_zomato_swiggy_score([
            m.zomato_rating_amritsari,
            m.swiggy_rating_amritsari,
            m.zomato_rating_chennai,
            m.swiggy_rating_chennai,
        ]),
        food_cost_score=logic.calculate_food_cost_score(
            m.food_cost_amritsari,
            m.food_cost_chennai,
        ),
        online_activity_score=logic.calculate_online_activity_score([
            m.online_activity_amritsari_zomato,
            m.online_activity_amritsari_swiggy,
            m.online_activity_chennai_zomato,
            m.online_activity_chennai_swiggy,
        ]),
        kitchen_prep_score=logic.calculate_kitchen_prep_score([
            m.kitchen_prep_amritsari_zomato,
            m.kitchen_prep_amritsari_swiggy,
            m.kitchen_prep_chennai_zomato,
            m.kitchen_prep_chennai_swiggy,
        ]),
        bad_delay_score=logic.calculate_bad_delay_score(
            [
                m.bad_order_amritsari_zomato,
                m.bad_order_amritsari_swiggy,
                m.bad_order_chennai_zomato,
                m.bad_order_chennai_swiggy,
            ],
            [
                m.delay_order_amritsari_zomato,
                m.delay_order_amritsari_swiggy,
                m.delay_order_chennai_zomato,
                m.delay_order_chennai_swiggy,
            ],
        ),
        outlet_audit_score=logic.calculate_outlet_audit_score(
            m.mistakes_amritsari,
            m.mistakes_chennai,
        ),
        add_on_sale_score=logic.calculate_add_on_sale_score(
            m.total_sale_amritsari,
            m.add_on_sale_amritsari,
            m.total_sale_chennai,
            m.add_on_sale_chennai,
        ),
    )

# =========================
# Routes
# =========================
@app.post("/calculate", response_model=ScorecardResponse)
def calculate_only(data: ScorecardCreate):
    bd = calculate_breakdown(data.metrics)
    total = sum(bd.model_dump().values())

    return ScorecardResponse(
        manager_name=data.manager_name,
        mall_name=data.mall_name,
        month=data.month,
        created_at=datetime.utcnow(),
        total_score=total,
        breakdown=bd,
        metrics=data.metrics,
    )

@app.post("/scorecards", response_model=ScorecardResponse)
def create_scorecard(
    data: ScorecardCreate,
    db: Session = Depends(get_db),
):
    bd = calculate_breakdown(data.metrics)
    total = sum(bd.model_dump().values())

    db_item = ScorecardDB(
        month=data.month,
        manager_name=data.manager_name,
        mall_name=data.mall_name,
        total_score=total,
        raw_metrics=data.metrics.model_dump(),
        breakdown=bd.model_dump(),
    )

    db.add(db_item)
    db.commit()
    db.refresh(db_item)

    return ScorecardResponse(
        id=db_item.id,
        manager_name=db_item.manager_name,
        mall_name=db_item.mall_name,
        month=db_item.month,
        created_at=db_item.created_at,
        total_score=db_item.total_score,
        breakdown=Breakdown(**db_item.breakdown),
        metrics=MetricsInput(**db_item.raw_metrics),
    )

@app.get("/scorecards", response_model=List[ScorecardResponse])
def get_scorecards(
    month: str = Query(None),
    year: str = Query(None),
    db: Session = Depends(get_db),
):
    query = db.query(ScorecardDB)

    if month and year:
        query = query.filter(ScorecardDB.month == f"{month} {year}")
    elif month:
        query = query.filter(ScorecardDB.month.startswith(month))
    elif year:
        query = query.filter(ScorecardDB.month.endswith(year))

    items = query.all()

    return [
        ScorecardResponse(
            id=i.id,
            manager_name=i.manager_name,
            mall_name=i.mall_name,
            month=i.month,
            created_at=i.created_at,
            total_score=i.total_score,
            breakdown=Breakdown(**i.breakdown),
            metrics=MetricsInput(**i.raw_metrics),
        )
        for i in items
    ]

@app.delete("/scorecards/{id}")
def delete_scorecard(id: int, db: Session = Depends(get_db)):
    item = db.query(ScorecardDB).filter(ScorecardDB.id == id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Not found")

    db.delete(item)
    db.commit()
    return {"ok": True}

@app.get("/export/{id}")
def export_excel(id: int, db: Session = Depends(get_db)):
    item = db.query(ScorecardDB).filter(ScorecardDB.id == id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Not found")

    metrics = MetricsInput(**item.raw_metrics)
    bd = Breakdown(**item.breakdown)

    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Scorecard"

    ws.append(["Metric", "Value", "Points"])
    ws.append(["Manager", item.manager_name, ""])
    ws.append(["Mall", item.mall_name, ""])
    ws.append(["Month", item.month, ""])
    ws.append(["Total Score", item.total_score, ""])
    ws.append(["", "", ""])

    ws.append(["Google Rating", f"A: {metrics.google_rating_amritsari}, C: {metrics.google_rating_chennai}", bd.google_score])
    ws.append(["Zomato/Swiggy", "(Avg of 4 ratings)", bd.zomato_swiggy_score])
    ws.append(["Food Cost", f"A: {metrics.food_cost_amritsari}%, C: {metrics.food_cost_chennai}%", bd.food_cost_score])
    ws.append(["Online Activity", "(Avg of 4%)", bd.online_activity_score])
    ws.append(["Kitchen Prep", "(Avg of 4 times)", bd.kitchen_prep_score])
    ws.append(["Bad & Delay", "(Combined Score)", bd.bad_delay_score])
    ws.append(["Outlet Audit", f"A: {metrics.mistakes_amritsari}, C: {metrics.mistakes_chennai}", bd.outlet_audit_score])
    ws.append(["Add On Sale", f"A: {metrics.add_on_sale_amritsari}/{metrics.total_sale_amritsari}, C: {metrics.add_on_sale_chennai}/{metrics.total_sale_chennai}", bd.add_on_sale_score])

    handle, path = tempfile.mkstemp(suffix=".xlsx")
    os.close(handle)
    wb.save(path)

    return FileResponse(
        path,
        filename=f"Scorecard_{item.manager_name}_{item.month}.xlsx",
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    )