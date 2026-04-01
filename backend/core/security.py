"""
Security and Authentication Module.

This module handles user authentication, password hashing,
JWT token management, and authorization.
"""

import hashlib
import hmac
from datetime import datetime, timedelta
from typing import Optional, Dict, Any
from jose import JWTError, jwt
from passlib.context import CryptContext

from backend.core.config import settings


# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class AuthService:
    """
    Authentication service for user management and token generation.
    
    This service handles:
    - Password hashing and verification
    - JWT token generation and validation
    - User authentication
    """
    
    def __init__(self):
        """Initialize authentication service."""
        self.secret_key = settings.security.secret_key
        self.algorithm = settings.security.algorithm
        self.access_token_expire_minutes = settings.security.access_token_expire_minutes
        self.refresh_token_expire_days = settings.security.refresh_token_expire_days
    
    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """
        Verify a password against its hash.
        
        Args:
            plain_password: Plain text password
            hashed_password: Hashed password to verify against
            
        Returns:
            bool: True if password matches
        """
        return pwd_context.verify(plain_password, hashed_password)
    
    def get_password_hash(self, password: str) -> str:
        """
        Hash a password.
        
        Args:
            password: Plain text password to hash
            
        Returns:
            str: Hashed password
        """
        return pwd_context.hash(password)
    
    def create_access_token(
        self,
        data: Dict[str, Any],
        expires_delta: Optional[timedelta] = None
    ) -> str:
        """
        Create a JWT access token.
        
        Args:
            data: Data to encode in the token
            expires_delta: Optional custom expiration time
            
        Returns:
            str: Encoded JWT token
        """
        to_encode = data.copy()
        
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=self.access_token_expire_minutes)
        
        to_encode.update({"exp": expire, "type": "access"})
        
        encoded_jwt = jwt.encode(to_encode, self.secret_key, algorithm=self.algorithm)
        return encoded_jwt
    
    def create_refresh_token(
        self,
        data: Dict[str, Any],
        expires_delta: Optional[timedelta] = None
    ) -> str:
        """
        Create a JWT refresh token.
        
        Args:
            data: Data to encode in the token
            expires_delta: Optional custom expiration time
            
        Returns:
            str: Encoded JWT refresh token
        """
        to_encode = data.copy()
        
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(days=self.refresh_token_expire_days)
        
        to_encode.update({"exp": expire, "type": "refresh"})
        
        encoded_jwt = jwt.encode(to_encode, self.secret_key, algorithm=self.algorithm)
        return encoded_jwt
    
    def create_tokens(self, user_id: int, username: str) -> Dict[str, str]:
        """
        Create both access and refresh tokens.
        
        Args:
            user_id: User's ID
            username: User's username
            
        Returns:
            Dict containing access_token and refresh_token
        """
        token_data = {"sub": str(user_id), "username": username}
        
        access_token = self.create_access_token(token_data)
        refresh_token = self.create_refresh_token(token_data)
        
        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer"
        }
    
    def verify_token(self, token: str, token_type: str = "access") -> Optional[Dict[str, Any]]:
        """
        Verify and decode a JWT token.
        
        Args:
            token: JWT token to verify
            token_type: Type of token (access or refresh)
            
        Returns:
            Optional[Dict]: Decoded token payload if valid, None otherwise
        """
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            
            if payload.get("type") != token_type:
                return None
            
            return payload
        except JWTError:
            return None
    
    def get_user_id_from_token(self, token: str) -> Optional[int]:
        """
        Extract user ID from a token.
        
        Args:
            token: JWT token
            
        Returns:
            Optional[int]: User ID if token is valid
        """
        payload = self.verify_token(token)
        if payload:
            user_id = payload.get("sub")
            if user_id:
                return int(user_id)
        return None


# Global auth service instance
auth_service = AuthService()


def create_access_token(data: Dict[str, Any], expires_delta: Optional[timedelta] = None) -> str:
    """Create access token (convenience function)."""
    return auth_service.create_access_token(data, expires_delta)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify password (convenience function)."""
    return auth_service.verify_password(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """Hash password (convenience function)."""
    return auth_service.get_password_hash(password)


def create_tokens(user_id: int, username: str) -> Dict[str, str]:
    """Create tokens (convenience function)."""
    return auth_service.create_tokens(user_id, username)
