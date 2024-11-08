from datetime import datetime
from app import db
import uuid

def generate_uuid():
    return str(uuid.uuid4())

class ChristmasLetter(db.Model):
    """크리스마스 편지 모델"""
    id = db.Column(db.Integer, primary_key=True)
    uuid = db.Column(db.String(36), unique=True, default=generate_uuid)  # URL용 고유 식별자
    
    # 편지 작성자 정보
    sender_name = db.Column(db.String(100), nullable=False)
    sender_email = db.Column(db.String(120))  # 선택적
    
    # 편지 내용
    message = db.Column(db.Text, nullable=False)
    image_path = db.Column(db.String(255))  # 이미지 파일 경로
    
    # 메타 데이터
    is_public = db.Column(db.Boolean, default=True)  # 공개/비공개 설정
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    ip_address = db.Column(db.String(45))  # IPv6도 고려
    
    # 감정 표현 (이모지 또는 스티커)
    emotion = db.Column(db.String(50))  # 'happy', 'love', 'thankful' 등
    
    # 관리용 필드
    is_appropriate = db.Column(db.Boolean, default=True)  # 부적절한 콘텐츠 필터링
    
    def __repr__(self):
        return f'<ChristmasLetter {self.sender_name}>'