import os # add_note에서 사용(path 파일 경로 설정)
import re # _check_image_path에서 사용
from datetime import datetime # add_note에서 사용(날짜 형식 지정)
from src.repository import NoteRepository

class NoteManager:
    def __init__(self, note_repository: NoteRepository):
        self.note_repository = note_repository
   
    """노트 추가"""
    def add_note(self, title, schedule_date, content, image_path):
        nid = self.note_repository.save_note(title, schedule_date, content, image_path)
        print(f"[✅ 성공] 메모({nid}) 💾저장 완료")

    """노트 수정"""
    def edit_note(self, note_id, title, schedule_date, content, image_path):
        self.validate_note_id(note_id)
        self.note_repository.update_note(note_id,title, schedule_date, content, image_path)
        
    """노트 삭제"""
    def delete_note(self, note_id):
        """메모 삭제"""
        try:
            self.note_repository.delete_note(note_id)
            print(f"[✅성공] 메모({note_id}) 🗑️삭제 완료")
        except KeyError as e:
            print(f"[❌오류] Error: {e}")

    def validate_note_id(self, input_note: str) -> int:
        """입력된 note_id 문자열을 검증하고, 정수로 반환합니다."""
        if not input_note:
            raise ValueError("ID를 입력해주세요.")
        try:
            note_id = int(input_note)
        except ValueError:
            raise ValueError("숫자형태가 아닙니다.")
        if not self.note_repository.note_exists(note_id):
            raise LookupError("해당 ID는 존재하지 않습니다.")
        return note_id
    
    def note_number_refactoring(self, notes: list) -> list:
        numbered = []
        for idx, note in enumerate(notes, start=1):
            note_with_number = note.copy()
            note_with_number['display_no'] = idx
            numbered.append(note_with_number)
        return numbered
    
    # 필드별 입력 + 유효성 반복
    def prompt_title(self, required):
        while True:
            title = input("✏️ 제목 (새 메모는 입력, 없으면 Enter): ").strip() or None
            try:
                self._check_title(title, required=required)
                return title
            except ValueError as e:
                print(f"[❌오류] {e}")

    def prompt_schedule_date(self, required):
        while True:
            date = input("📅 일정 (새 메모는 입력, 형식 YYYY-MM-DD, 없으면 Enter): ").strip() or None
            try:
                self._check_schedule(date, required=required)
                return date
            except ValueError as e:
                print(f"[❌오류] {e}")

    def prompt_content(self, required):
        while True:
            content = input("📝 내용 (새 메모는 입력, 없으면 Enter): ").strip() or None
            try:
                self._check_content(content, required=required)
                return content
            except ValueError as e:
                print(f"[❌오류] {e}")

    def prompt_image_path(self):
        while True:
            path = input("🖼️ 이미지 경로 ([절대경로], 없으면 Enter): ").strip() or None
            try:
                self._check_image_path(path)
                return path
            except ValueError as e:
                print(f"[❌오류] {e}")

    def _check_title(self, title, required):
        if required and not title: # required * 제목이 없을때 =>참이면 실행
            raise ValueError("제목은 필수입니다.")
        if title and len(title) >= 255: # 제목이 있을때 * 문자길이가 255이상일때 => 참이면 실행
            raise ValueError("제목은 255자를 넘을 수 없습니다.")
        
    def _check_schedule(self, schedule_date, required):
        if required and not schedule_date: # required * 스케줄이 없을때 => 참이면 실행
                raise ValueError("일정을 입력해주세요.")
        if schedule_date: # 스케줄이 있을때때
            try:
                datetime.strptime(schedule_date, "%Y-%m-%d")
            except ValueError:
                raise ValueError("일정 형식은 YYYY-MM-DD이어야 합니다.")
            
    def _check_content(self, content, required):
        if required and not content: # required * 내용이 없을때 => 참이면 실행
            raise ValueError("내용을 입력해주세요.")
        if content and len(content) >= 21000: # 내용이 있을때 * 문자 길이가 21000이상일때 => 실행
            raise ValueError("내용은 21,000자를 넘길 수 없습니다.")
            
    def _check_image_path(self, image_path):
        if image_path:
            # 한글만 포함된 경우 경고
            if re.fullmatch(r"[가-힣\s]+", image_path):
                raise ValueError("경로 대신 일반 문자가 입력되었습니다. 이미지 경로를 올바르게 입력하세요.")
            # 절대경로 검사: 경로가 절대경로인지 확인
            if not os.path.isabs(image_path):
                raise ValueError("이미지 경로는 절대경로로 입력해 주세요.")
            # 실제 파일 존재 여부 확인
            if not os.path.isfile(image_path):
                raise ValueError(f"이미지 파일이 존재하지 않습니다: {image_path}")