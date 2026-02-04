from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, JSON, DateTime
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

# SQLAlchemy Database Model
class ScorecardDB(Base):
    __tablename__ = "scorecards"
    
    id = Column(Integer, primary_key=True, index=True)
    month = Column(String, index=True)
    manager_name = Column(String)
    mall_name = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    total_score = Column(Float)
    
    # Store complex data as JSON
    raw_metrics = Column(JSON)
    breakdown = Column(JSON)

# Pydantic Models for API
class MetricsInput(BaseModel):
    # Google Ratings
    google_rating_amritsari: float
    google_rating_chennai: float
    
    # Zomato + Swiggy Ratings (4 ratings)
    zomato_rating_amritsari: float
    swiggy_rating_amritsari: float
    zomato_rating_chennai: float
    swiggy_rating_chennai: float
    
    # Food Cost %
    food_cost_amritsari: float
    food_cost_chennai: float
    
    # Online Activity % (4 measurements)
    online_activity_amritsari_zomato: float
    online_activity_amritsari_swiggy: float
    online_activity_chennai_zomato: float
    online_activity_chennai_swiggy: float
    
    # Kitchen Prep Time (4 measurements)
    kitchen_prep_amritsari_zomato: float
    kitchen_prep_amritsari_swiggy: float
    kitchen_prep_chennai_zomato: float
    kitchen_prep_chennai_swiggy: float
    
    # Bad & Delay Order % (4 measurements each)
    bad_order_amritsari_zomato: float
    bad_order_amritsari_swiggy: float
    bad_order_chennai_zomato: float
    bad_order_chennai_swiggy: float
    
    delay_order_amritsari_zomato: float
    delay_order_amritsari_swiggy: float
    delay_order_chennai_zomato: float
    delay_order_chennai_swiggy: float
    
    # Outlet Audit
    mistakes_amritsari: int
    mistakes_chennai: int
    
    # Add on Sale
    total_sale_amritsari: float
    add_on_sale_amritsari: float
    total_sale_chennai: float
    add_on_sale_chennai: float

class ScorecardCreate(BaseModel):
    manager_name: str
    mall_name: str
    month: str
    metrics: MetricsInput

class Breakdown(BaseModel):
    google_score: int
    zomato_swiggy_score: int
    food_cost_score: int
    online_activity_score: int
    kitchen_prep_score: int
    bad_delay_score: int
    outlet_audit_score: float
    add_on_sale_score: float

class ScorecardResponse(BaseModel):
    id: Optional[int] = None
    manager_name: str
    mall_name: str
    month: str
    created_at: datetime
    total_score: float
    breakdown: Breakdown
    metrics: MetricsInput

    class Config:
        from_attributes = True

