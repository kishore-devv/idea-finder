from sqlalchemy import Column, Integer, String, Float, Boolean, Text

from app.database.database import Base


class App(Base):

    __tablename__ = "apps"

    id = Column(Integer, primary_key=True, index=True)

    app_id = Column(String, unique=True, index=True, nullable=False)

    title = Column(String)

    developer = Column(String)

    description = Column(Text)

    category = Column(String, index=True)

    score = Column(Float)

    ratings = Column(Integer)

    reviews = Column(Integer)

    installs = Column(String)

    real_installs = Column(Integer)

    price = Column(Float)

    free = Column(Boolean)

    contains_ads = Column(Boolean, default=False)

    offers_iap = Column(Boolean)

    iap_price = Column(String)

    released = Column(String)

    last_updated = Column(String)

    icon = Column(String)

    url = Column(String)


class Review(Base):

    __tablename__ = "reviews"

    id = Column(Integer, primary_key=True, index=True)

    review_id = Column(String, unique=True, index=True)

    app_id = Column(String, index=True)

    user = Column(String)

    score = Column(Integer)

    text = Column(Text)

    date = Column(String)

    thumbs_up = Column(Integer)

    version = Column(String)
