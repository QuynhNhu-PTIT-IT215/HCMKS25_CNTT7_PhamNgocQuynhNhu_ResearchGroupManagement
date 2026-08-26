from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session

from app.core.config import settings
from app.db.database import get_db
from app.models.user import User

#encode: đóng thông tin lại thành một cái token để gửi lên cho người dùng
#decode: mở token ra để xem thông tin bên trong và ktra nó có hợp lệ không

#OAuth2PasswordBearer(): hàm này nó giống như người đứng ở cửa, có nhiệm vụ lấy
# "thẻ ra vào" của ng dùng đưa cho hệ thống kiểm tra
oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/auth/login"
)

# oauth2_scheme: có nhiệm vụ lấy JWT token từ header
# -> lấy cái mã đăng nhập mà người dùng gửi lên, rồi đưa nó vào biến token
def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    try:
        payload = jwt.decode(token,settings.SECRET_KEY,algorithms=[settings.ALGORITHM])

        user_id = payload.get("sub")

        if user_id is None:
            raise HTTPException(
                status_code=401,
                detail="Token không hợp lệ"
            )

        try:
            user_id = int(user_id)
        except (ValueError, TypeError):
            raise HTTPException(
                status_code=401,
                detail="Token không hợp lệ"
            )

    except JWTError:
        raise HTTPException(
            status_code=401,
            detail="Token không hợp lệ hoặc đã hết hạn"
        )

    user = db.query(User).filter(User.id == user_id).first()

    if user is None:
        raise HTTPException(
            status_code=401,
            detail="Người dùng không tồn tại"
        )

    if not user.is_active:
        raise HTTPException(
            status_code=403,
            detail="Tài khoản đã bị khóa"
        )

    return user