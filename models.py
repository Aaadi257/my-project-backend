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
    
    total_score = Column(Float, index=True)
    
    # Store complex data as JSON
    raw_metrics = Column(JSON)
    breakdown = Column(JSON)

# Pydantic Models for API
class MetricsInput(BaseModel):
    # Google Ratings
    google_rating_amritsari: Optional[float] = None
    google_rating_chennai: Optional[float] = None
    google_rating_chaat_masala: Optional[float] = None
    
    # Zomato + Swiggy Ratings (6 ratings)
    zomato_rating_amritsari: Optional[float] = None
    swiggy_rating_amritsari: Optional[float] = None
    zomato_rating_chennai: Optional[float] = None
    swiggy_rating_chennai: Optional[float] = None
    zomato_rating_chaat_masala: Optional[float] = None
    swiggy_rating_chaat_masala: Optional[float] = None
    
    # Food Cost %
    food_cost_amritsari: Optional[float] = None
    food_cost_chennai: Optional[float] = None
    food_cost_chaat_masala: Optional[float] = None
    
    # Online Activity % (6 measurements)
    online_activity_amritsari_zomato: Optional[float] = None
    online_activity_amritsari_swiggy: Optional[float] = None
    online_activity_chennai_zomato: Optional[float] = None
    online_activity_chennai_swiggy: Optional[float] = None
    online_activity_chaat_masala_zomato: Optional[float] = None
    online_activity_chaat_masala_swiggy: Optional[float] = None
    
    # Kitchen Prep Time (6 measurements)
    kitchen_prep_amritsari_zomato: Optional[float] = None
    kitchen_prep_amritsari_swiggy: Optional[float] = None
    kitchen_prep_chennai_zomato: Optional[float] = None
    kitchen_prep_chennai_swiggy: Optional[float] = None
    kitchen_prep_chaat_masala_zomato: Optional[float] = None
    kitchen_prep_chaat_masala_swiggy: Optional[float] = None
    
    # Bad & Delay Order % (3 measurements each)
    bad_order_amritsari_zomato: Optional[float] = None
    bad_order_chennai_zomato: Optional[float] = None
    bad_order_chaat_masala_zomato: Optional[float] = None
    
    delay_order_amritsari_swiggy: Optional[float] = None
    delay_order_chennai_swiggy: Optional[float] = None
    delay_order_chaat_masala_swiggy: Optional[float] = None
    
    # Outlet Audit
    mistakes_amritsari: Optional[int] = None
    mistakes_chennai: Optional[int] = None
    mistakes_chaat_masala: Optional[int] = None
    
    # Negative Reviews
    negative_reviews_amritsari: Optional[int] = None
    negative_reviews_chennai: Optional[int] = None
    negative_reviews_chaat_masala: Optional[int] = None

    # Add on Sale
    total_sale_amritsari: Optional[float] = None
    add_on_sale_amritsari: Optional[float] = None
    total_sale_chennai: Optional[float] = None
    add_on_sale_chennai: Optional[float] = None
    total_sale_chaat_masala: Optional[float] = None
    add_on_sale_chaat_masala: Optional[float] = None

    # Software Inventory ("filled_correctly" = 10 pts, "filled_incorrectly"/None = 0 pts;
    # legacy "filled" still scores 10 for backward compatibility)
    inventory_form: Optional[str] = None

    # Rolling 3-month metrics (value represents selected month + previous 2 months)
    staff_alteration: Optional[int] = None
    manager_quarterly_leave: Optional[float] = None

class ScorecardCreate(BaseModel):
    manager_name: str
    mall_name: str
    month: str
    metrics: MetricsInput

class Breakdown(BaseModel):
    google_score: int
    zomato_swiggy_score: int
    food_cost_score: float
    online_activity_score: int
    kitchen_prep_score: int
    bad_delay_score: int
    outlet_audit_score: float
    negative_review_score: float = 0.0
    add_on_sale_score: float
    inventory_form_score: int = 0
    staff_alteration_score: int = 0
    manager_quarterly_leave_score: int = 0

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

