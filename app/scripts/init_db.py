from app.core.database import Base, engine
from app.models import *  # noqa


def main() -> None:
    Base.metadata.create_all(bind=engine)
    print("Database tables created.")


if __name__ == "__main__":
    main()
