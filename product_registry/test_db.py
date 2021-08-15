def create_db():
    from sqlalchemy import create_engine
    engine = create_engine("postgresql+psycopg2://postgres:uttasarga@localhost:5433/target_api")
    con = engine.connect()
    print(engine.table_names())

create_db()