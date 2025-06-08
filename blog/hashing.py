from passlib.context import CryptContext
class Hash():
    pwd_cxt = CryptContext(schemes=['bcrypt'], deprecated="auto")
    def hash(self, password: str) -> str:
        return self.pwd_cxt.hash(password)
    
    def verify(self, plain_password: str, hashed_password: str) -> bool:
        return self.pwd_cxt.verify(plain_password, hashed_password)