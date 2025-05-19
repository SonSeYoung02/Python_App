import os # loading_app 사용
import time # loading_app 사용(로딩 표현)
from src.utils.note_manager import NoteManager

class NoteUI:
    def __init__(self,note_manager: NoteManager):
        self.note_manager = note_manager

    """UserInterface"""
    def ui(self):

        while True:
            self.loading_effect()
            self.show_menu()

            choice = input(">> ")

            if choice == "1":
                self.handle_add_note()
            elif choice == "2":
                self.handle_edit_note()
            elif choice == "3":
                self.handle_delete_note()
            elif choice == "0":
                print("👋 프로그램을 종료합니다.")
                break
            else:
                print("[❌오류] 올바르지 않은 선택입니다.")

    def loading_effect(self):
        """기록 로딩 이펙트"""
        os.system('cls' if os.name == 'nt' else 'clear')  # 화면 클리어 (윈도우/유닉스)
    
        loading_bar = ["[■□□□□□□□□□]", "[■■□□□□□□□□]", "[■■■□□□□□□□]", "[■■■■□□□□□□]", 
                    "[■■■■■□□□□□]", "[■■■■■■□□□□]", "[■■■■■■■□□□]", "[■■■■■■■■□□]", 
                    "[■■■■■■■■■□]", "[■■■■■■■■■■]"]
        
        """앱 실행 및 초기 동기화"""
        print("┌────────────────────────────────────┐")
        print("|           📝 NOTE SYNC             |")
        print("|      나의 메모를 불러오고 있어요   |")
        print("└────────────────────────────────────┘\n")

        for step in loading_bar:
            print(f"\r🔄 메모 불러오는 중... {step}", end="")
            time.sleep(0.1)

        print("\n✅ 동기화 완료!\n")

        notes = self.note_manager.note_repository.fetch_note()
        self.list_notes(notes)

    def list_notes(self, notes):
        """메모 목록 화면 출력"""
        if not notes: # 노트가 없는 경우
            print("┌────────────────────────────────────┐")
            print("|📭 저장된 메모가 아직 없어요.       |")
            print("|📝 지금 첫 번째 메모를 추가해보세요!|")
            print("└────────────────────────────────────┘")
        else: # 노트가 있는 경우
            note_list = []
            for nid, note in notes.items():
                if isinstance(note, dict):
                    note_copy = note.copy()
                    note_copy['id'] = nid
                    note_list.append(note_copy)

            numbered_notes = self.note_manager.note_number_refactoring(note_list)
            
            print("[📒 메모 목록]")
            for note in numbered_notes:
                print("="*100)
                print(f"{note['display_no']})") 
                print(f"📌 제목: {note['title']}")
                print(f"📅 일정: {note['schedule_date']}")
                print(f"📝 내용: {note['content']}")
                print(f"🖼️ 이미지: {note['image_path']}")
                print("="*100 + "\n")
            return
        
    def show_menu(self):
        """메뉴 인터페이스"""
        print("[📋 메뉴]")
        print("1. 새 메모 추가")
        print("2. 메모 수정")
        print("3. 메모 삭제")
        print("0. 종료")

    def handle_add_note(self):
         # 제목과 내용은 비교적 자유 → UI에서 직접 입력
        title = self.note_manager.prompt_title(required=True)
        schedule_date = self.note_manager.prompt_schedule_date(required=True)
        content = self.note_manager.prompt_content(required=True)
        image_path = self.note_manager.prompt_image_path()

        try:
            self.note_manager.add_note(title, schedule_date, content, image_path)
        except Exception as e:
            print(f"[❌오류] {e}")
    
    def handle_edit_note(self):
        input_note = input("✏️ 수정할 메모: ").strip()
        try:
            input_id = self.note_manager.validate_note_id(input_note)
        except Exception as e:
            print(f"[❌오류] {e}")
            return
            
        self.preview_note(input_id) # 수정할 메모 미리보기

        if self.confirm_action("[🔘확인] 수정하시겠습니까 (y/n): "):

            # 필드별 개별 반복 입력0
            title = self.note_manager.prompt_title(required=False)
            schedule_date = self.note_manager.prompt_schedule_date(required=False)
            content = self.note_manager.prompt_content(required=False)
            image_path = self.note_manager.prompt_image_path()

            try:
                self.note_manager.edit_note(input_id, title, schedule_date, content, image_path)
                print(f"[✅ 성공] 메모({input_id}) 📌수정 완료")
            except KeyError as e:
                print(f"[❌ 오류] Error: {e}")
        else:
            print("[🔘확인] 수정이 취소되었습니다.")


    def handle_delete_note(self):
        input_note = input("🗑️ 삭제할 메모: ").strip()
        try:
            input_id = self.note_manager.validate_note_id(input_note)
        except Exception as e:
            print(f"[❌ 오류] {e}")
            return

        self.preview_note(input_id) # 삭제할 메모 미리보기

        if self.confirm_action("[🔘확인] 삭제하시겠습니까? (y/n): "):
            try:
                self.note_manager.delete_note(input_note)
            except Exception as e:
                print(f"[❌오류] {e}")
        else:
            print("[🔘확인] 삭제가 취소되었습니다.")
    

    def confirm_action(self,prompt)->bool: #True False 값 반환
        """'y'일 때만 True, 그 외에는 재입력 요청"""
        while True:
            choice = input(prompt).strip().lower()
            if choice == "y":
                return True
            elif choice == "n":
                return False
            else:
                print("[❌오류] 'y' 또는 'n만 입력해주세요.")

    def preview_note(self, note_id):
        notes = self.note_manager.note_repository.fetch_note()
        note = notes.get(note_id)
        if not note:
            print("[❌오류] 해당 ID의 메모를 찾을 수 없습니다.")
            return
        """노트 UI"""
        print("="*100)
        print(f"{note_id})")
        print(f"📌 제목: {note['title']}")
        print(f"📅 일정: {note['schedule_date']}")
        print(f"📝 내용: {note['content']}")
        print(f"🖼️ 이미지: {note['image_path']}")
        print("="*100 + "\n")
    