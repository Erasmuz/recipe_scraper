from database import engine, Base, Recipe


if __name__ == "__main__":
    Base.metadata.create_all(engine)

