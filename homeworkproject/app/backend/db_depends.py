from app.backend.db  import sessionlocal

async def get_db():
    db = sessionlocal()
    try:
        yield db
    finally:
        db.close()