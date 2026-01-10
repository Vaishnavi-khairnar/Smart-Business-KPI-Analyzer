import pytest
from sqlalchemy.orm import Session

from app.core.database import SessionLocal, engine, Base
from app.schemas.user import UserCreate
from app.services.auth import AuthService
from app.utils.auth import verify_password, get_password_hash
from app.utils.error_handling import KPIError


# =====================================================
# DATABASE FIXTURE
# =====================================================
@pytest.fixture(scope="function")
def db_session():
    Base.metadata.create_all(bind=engine)
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()
        Base.metadata.drop_all(bind=engine)


# =====================================================
# AUTH SERVICE TESTS
# =====================================================
class TestAuthService:

    def test_password_hashing(self):
        password = "Test@12345"

        hashed = get_password_hash(password)
        assert hashed != password
        assert verify_password(password, hashed) is True
        assert verify_password("wrong", hashed) is False

    def test_user_creation(self, db_session: Session):
        auth_service = AuthService()

        user = UserCreate(
            username="testuser",
            email="test@example.com",
            password="Test@12345",
        )

        created_user = auth_service.create_user(db_session, user)

        assert created_user.username == "testuser"
        assert created_user.email == "test@example.com"
        assert created_user.is_active is True
        assert created_user.is_superuser is False

    def test_user_authentication_success(self, db_session: Session):
        auth_service = AuthService()

        user = UserCreate(
            username="testuser",
            email="test@example.com",
            password="Test@12345",
        )

        auth_service.create_user(db_session, user)

        authenticated = auth_service.authenticate_user(
            db_session, "testuser", "Test@12345"
        )

        assert authenticated.username == "testuser"
        assert authenticated.email == "test@example.com"

    def test_user_authentication_wrong_password(self, db_session: Session):
        auth_service = AuthService()

        user = UserCreate(
            username="testuser",
            email="test@example.com",
            password="Test@12345",
        )

        auth_service.create_user(db_session, user)

        with pytest.raises(KPIError):
            auth_service.authenticate_user(
                db_session, "testuser", "WrongPassword"
            )

    def test_user_authentication_nonexistent_user(self, db_session: Session):
        auth_service = AuthService()

        with pytest.raises(KPIError):
            auth_service.authenticate_user(
                db_session, "ghost", "whatever"
            )
