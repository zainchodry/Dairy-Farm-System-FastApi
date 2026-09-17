from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.models.accounts import User, RoleEnum
from app.utils.auth import verify_token
from app.database import get_db
# This tells FastAPI where the client can send username/password to get a token
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/accounts/login")

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> User:
    """Decodes the JWT access token and returns the current authenticated User object."""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    payload = verify_token(token, is_refresh=False)
    if payload is None:
        raise credentials_exception
        
    username: str = payload.get("sub")
    if username is None:
        raise credentials_exception
        
    user = db.query(User).filter(User.username == username).first()
    if user is None:
        raise credentials_exception
        
    return user

def require_role(allowed_roles: list[RoleEnum]):
    """
    Dependency factory for Role-Based Access Control (RBAC).
    Usage: Depends(require_role([RoleEnum.ADMIN, RoleEnum.MANAGER]))
    """
    def role_checker(current_user: User = Depends(get_current_user)):
        if current_user.role not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, 
                detail=f"Access denied. Requires one of the following roles: {[role.value for role in allowed_roles]}"
            )
        return current_user
    return role_checker