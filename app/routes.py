import os
from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app
from werkzeug.utils import secure_filename
from app.models import ChristmasLetter, db
from datetime import datetime

main_bp = Blueprint('main', __name__)

# 허용된 파일 확장자 설정
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    """파일 확장자 검사 함수"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@main_bp.route('/')
def index():
    letters = ChristmasLetter.query.filter_by(is_public=True)\
        .order_by(ChristmasLetter.created_at.desc())\
        .all()
    return render_template('index.html', letters=letters)

@main_bp.route('/write', methods=['GET', 'POST'])
def write_letter():
    if request.method == 'POST':
        # 폼 데이터 받기
        sender_name = request.form.get('sender_name')
        message = request.form.get('message')
        emotion = request.form.get('emotion', 'happy')
        
        # 이미지 처리
        image_path = None
        if 'image' in request.files:
            file = request.files['image']
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                # 파일명 중복 방지를 위해 타임스탬프 추가
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                new_filename = f"{timestamp}_{filename}"
                
                # uploads 디렉토리가 없으면 생성
                uploads_dir = os.path.join(current_app.root_path, 'static', 'uploads')
                os.makedirs(uploads_dir, exist_ok=True)
                
                # 파일 저장
                file_path = os.path.join(uploads_dir, new_filename)
                file.save(file_path)
                image_path = f"uploads/{new_filename}"
        
        # 새 편지 생성
        letter = ChristmasLetter(
            sender_name=sender_name,
            message=message,
            emotion=emotion,
            image_path=image_path,
            ip_address=request.remote_addr
        )
        
        try:
            db.session.add(letter)
            db.session.commit()
            flash('편지가 성공적으로 전달되었습니다!', 'success')
            return redirect(url_for('main.index'))
        except Exception as e:
            db.session.rollback()
            flash('편지 전송 중 오류가 발생했습니다. 다시 시도해주세요.', 'error')
            print(f"Error: {str(e)}")  # 로깅을 위해 추가
    
    return render_template('write.html')