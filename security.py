# security.py
from passlib.context import CryptContext
from jose import jwt
from datetime import datetime, timedelta
from fastapi import HTTPException

# CONFIG
SECRET_KEY = "SUPER_SECRET_KEY_CHANGE_ME"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

# Use pbkdf2_sha256 to avoid bcrypt native issues
pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")

def hash_password(password: str) -> str:#convierto la contraseña a un texto plano antes de guardarla en mi bd
    return pwd_context.hash(password)

def verify_password(password: str, hashed: str) -> bool:#comparo la contraseña en texto plano con mi hash almacenado 
    return pwd_context.verify(password, hashed)
#en este caso hash convierte mi contraseña en un texto plano ejemplo hash(1234) va guarda en texto plano algo como $pbkdf2-sha256$29000$2j1mZb...$1/2kW1w3s...

#aca abajo generamos un token y cuando se hacen un login exitoso se genera un jwt (json web tokens) que va contener correo y contraseña para mi login
def create_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def verify_token(token: str) -> dict:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except Exception as e:
        raise HTTPException(status_code=401, detail="Token inválido")
