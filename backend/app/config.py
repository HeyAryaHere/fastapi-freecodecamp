"""
    ! READ BEFORE TO UNDERSTAND ANNOTATIONS 
    Download extenstion better comments https://marketplace.visualstudio.com/items?itemName=aaron-bond.better-comments to make it more visible on visual studio code
    Annotations are written as below:
        # Is used to understand single line comment example Import
        ! Is used to grab your attention to an important line
        ? Provides a list of functions 
        * * Is used to elobrate over a function 
"""

"""
    Import necessary libraries: Imports AsyncSession, 
    create_async_engine from SQLAlchemy for asynchronous database operations, sessionmaker for creating session objects, and SQLModel for defining database models.
    Database connection string: Sets up a PostgreSQL database connection string in DB_CONFIG.
"""
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlmodel import SQLModel

# Sets up a PostgreSQL database connection string in DB_CONFIG.
DB_CONFIG = f"postgresql+asyncpg://postgres:postgres@localhost:5432/test"

# Password for postgres PGAdmin 
SECRET_KEY = "postgres"

"""
    ! HS256 is not a PostgreSQL algorithm. It's a hashing algorithm used in cryptography for creating digital signatures.

    Breakdown of HS256:
        * * H: Stands for Hash-based.
        * * S: Stands for Signature.
        * * 256: Refers to the hash function used, SHA-256, which produces a 256-bit hash value. 
"""
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

"""
    This class encapsulates database session management.
        ? Initialization: Creates empty session and engine attributes.
        ? __getattr__: Forwards attribute access to the underlying session object.
        ? init:
            ? Creates an asynchronous database engine using create_async_engine.
            ? Creates a sessionmaker instance for creating database sessions.
        ? create_all: Creates all database tables defined in SQLModel.metadata.
"""
class AsyncDatabaseSession:

    def __init__(self) -> None:
        self.session = None
        self.engine = None

    def __getattr__(self,name):
        return getattr(self.session,name)

    def init(self):
        self.engine = create_async_engine(DB_CONFIG,future=True, echo=True)
        self.session = sessionmaker(self.engine, expire_on_commit=False, class_=AsyncSession)()

    async def create_all(self):
        async with self.engine.begin() as conn:
            await conn.run_sync(SQLModel.metadata.create_all)

# db is an instance of AsyncDatabaseSession.
db = AsyncDatabaseSession()

"""
    commit_rollback is an asynchronous function:
        ? Attempts to commit the database session.
        ? If an exception occurs, rolls back the session and re-raises the exception.
"""
async def commit_rollback():
    try:
        await db.commit()
    except Exception:
        await db.rollback()
        raise