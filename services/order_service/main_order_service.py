import os
import time
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import Column, Integer, String, Float, create_engine, exc
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from prometheus_fastapi_instrumentator import Instrumentator

# 1. Настройка конфигурации (Раздел 4.2.1 ТЗ)
# В Docker используем имя сервиса 'postgres', для локальных тестов на M4 — localhost
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:1234@postgres:5432/store")

# 2. Инициализация SQLAlchemy
# Мы не импортируем create_all, так как это метод метаданных
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# 3. Определение модели данных
class Order(Base):
    __tablename__ = "orders"
    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer)
    product_name = Column(String)
    price = Column(Float)
    user_email = Column(String)

# 4. SRE-подход: Безопасное создание таблиц с ожиданием БД (Раздел 4.2.2 ТЗ)
def init_db():
    retries = 5
    while retries > 0:
        try:
            Base.metadata.create_all(bind=engine)
            print("Successfully connected to the database and created tables.")
            break
        except exc.OperationalError as e:
            retries -= 1
            print(f"Database not ready yet. Retrying in 5s... ({retries} retries left)")
            time.sleep(5)
    if retries == 0:
        print("Could not connect to the database. Starting without DB (expect errors).")

init_db()

# 5. Инициализация FastAPI
app = FastAPI(title="Order Service")

# Настройка CORS для работы с фронтендом
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 6. Автоматизация мониторинга (Раздел 4.2.3 ТЗ)
# Экспонирует эндпоинт /metrics для Prometheus
Instrumentator().instrument(app).expose(app)

# Dependency для работы с сессиями
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# --- ЭНДПОИНТЫ ---

@app.get("/health")
def health_check():
    """Эндпоинт для Docker Healthcheck (Раздел 4.2.2 ТЗ)"""
    return {"status": "healthy"}

@app.get("/")
def root():
    return {"message": "Order Service is running"}

@app.post("/orders")
def create_order(order_data: dict, db: Session = Depends(get_db)):
    """Создание заказа и запись в Postgres"""
    try:
        new_order = Order(
            product_id=order_data.get("product_id"),
            product_name=order_data.get("product_name"),
            price=order_data.get("price"),
            user_email=order_data.get("user_email", "guest")
        )
        db.add(new_order)
        db.commit()
        db.refresh(new_order)
        return {"status": "created", "order": new_order}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

@app.get("/orders")
def get_orders(db: Session = Depends(get_db)):
    """Получение всех заказов для проверки записи"""
    return db.query(Order).all()