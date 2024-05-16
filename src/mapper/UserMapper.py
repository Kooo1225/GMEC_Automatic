from sqlalchemy.orm import Session
from src.vo.UserVO import UserVO

class UserMapper:
    def insert(self, vo: UserVO, db: Session):
        new_record = vo
        db.add(new_record)
        db.commit()

    def read_all(self, db: Session):
        return db.query(UserVO).all()

    def read_id(self, id: str, db: Session):
        return db.query(UserVO).filter(UserVO.id == id).first()

    def update(self, vo: UserVO, db: Session):
        record = db.query(UserVO).filter(UserVO.id == vo.id).first()
        record.replaced_date = vo.replaced_date
        record.folder_id = vo.folder_id
        db.commit()

    def delete(self, user_id: int, db: Session):
        record = db.query(UserVO).filter(UserVO.user_id == user_id).first()
        db.delete(record)
        db.commit()
