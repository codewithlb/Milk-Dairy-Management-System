from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.admin import Admin
from app.utils.security import verify_password
from app.utils.jwt_handler import create_access_token


def login_admin(
    db: Session,
    username: str,
    password: str
):
    admin = db.query(Admin).filter(
        Admin.username == username
    ).first()

    if admin is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid username or password."
        )

    if not verify_password(password, admin.password):
        raise HTTPException(
            status_code=401,
            detail="Invalid username or password."
        )

    token = create_access_token(
        {"sub": admin.username}
    )

    return {
        "access_token": token,
        "token_type": "bearer"
    }