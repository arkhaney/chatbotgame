import tkinter as tk
from tkinter import simpledialog
from PIL import Image, ImageTk
import os

# ==== 전체 앱 클래스 구조로 시작 ====
class ChatApp:
    def __init__(self, root):
        self.root = root
        self.root.title("AI 챗 인터페이스")
        self.root.geometry("1000x600")
        self.root.minsize(800, 500)

        self.BG_COLOR = "#f7f7f7"
        self.SIDEBAR_COLOR = "#e0e0e0"
        self.CHAT_BG = "#ffffff"
        self.PROFILE_IMG_SIZE = (120, 120)

        self.memo_file = "memo.txt"
        self.current_contact = None
        self.current_img = None

        self.difficulty = None
        self.CHAT_PARTNERS = []
        self.profiles = {}

        self.frames = {}

        self.setup_start_screen()

                # ==== 전화번호 매핑 ==== 
        # key: 전화번호(str), 
        # value: dict(name: str, img_path: str, description: str)
        self.phone_book = {
            "01011112222": {
                "name": "용의자 A",
                "img_path": "images/suspect_a.png",
                "description": "사건 A의 주요 용의자입니다."
            },
            "01033334444": {
                "name": "증인 B",
                "img_path": "images/witness_b.png",
                "description": "사건 현장을 목격한 증인입니다."
            },
            # ... 필요한 만큼 추가 ...
        }

    def clear_frames(self):
        for frame in self.frames.values():
            frame.destroy()
        self.frames = {}

    # ==== 시작 화면 ====
    def setup_start_screen(self):
        self.clear_frames()
        start_frame = tk.Frame(self.root, bg=self.BG_COLOR)
        start_frame.pack(expand=True, fill="both")
        self.frames["start"] = start_frame

        tk.Label(start_frame, text="AI 챗 인터페이스", font=("Arial", 24), bg=self.BG_COLOR).pack(pady=40)
        tk.Button(start_frame, text="시작", font=("Arial", 16), command=self.setup_difficulty_screen).pack()

    # ==== 난이도 선택 화면 ====
    def setup_difficulty_screen(self):
        self.clear_frames()
        diff_frame = tk.Frame(self.root, bg=self.BG_COLOR)
        diff_frame.pack(expand=True, fill="both")
        self.frames["difficulty"] = diff_frame

        tk.Label(diff_frame, text="난이도를 선택하세요", font=("Arial", 20), bg=self.BG_COLOR).pack(pady=30)

        for level in ["쉬움", "중간", "어려움"]:
            btn = tk.Button(diff_frame, text=level, font=("Arial", 14),
                            width=15, command=lambda l=level: self.start_main_interface(l))
            btn.pack(pady=10)

    # ==== 난이도에 따라 챗봇 구성 ====
    def configure_partners(self, difficulty):
        if difficulty == "쉬움":
            self.CHAT_PARTNERS = ["초보봇", "친절봇"]
            self.profiles = {
                "초보봇": {
                    "img_path": "images/beginner.png",
                    "description": "초보자를 위한 간단한 챗봇입니다."
                },
                "친절봇": {
                    "img_path": "images/friendly.png",
                    "description": "항상 친절하게 대답해주는 봇이에요."
                }
            }
        elif difficulty == "중간":
            self.CHAT_PARTNERS = ["챗봇 A", "챗봇 B"]
            self.profiles = {
                "챗봇 A": {
                    "img_path": "images/chatbot_a.png",
                    "description": "챗봇 A는 친절하고 똑똑한 AI입니다."
                },
                "챗봇 B": {
                    "img_path": "images/chatbot_b.png",
                    "description": "챗봇 B는 유머러스하고 재치 있는 AI입니다."
                }
            }
        elif difficulty == "어려움":
            self.CHAT_PARTNERS = ["논리봇", "고수봇", "냉정봇"]
            self.profiles = {
                "논리봇": {
                    "img_path": "images/logical.png",
                    "description": "논리적으로 철저히 따지는 AI입니다."
                },
                "고수봇": {
                    "img_path": "images/master.png",
                    "description": "고급 지식을 보유한 AI입니다."
                },
                "냉정봇": {
                    "img_path": "images/cold.png",
                    "description": "감정에 흔들리지 않고 냉정한 대화를 합니다."
                }
            }

        # 채팅 기록 및 메모 초기화
        for name in self.CHAT_PARTNERS:
            file = f"chat_{name}.txt"
            if os.path.exists(file):
                os.remove(file)
        if os.path.exists(self.memo_file):
            os.remove(self.memo_file)

        # 기본 선택
        self.current_contact = self.CHAT_PARTNERS[0]

    # ==== 메인 인터페이스 시작 ====
    def start_main_interface(self, difficulty):
        self.difficulty = difficulty
        self.configure_partners(difficulty)
        self.clear_frames()
        self.setup_main_interface()  # 이건 2부에서 계속...
    def setup_main_interface(self):
        self.root.configure(bg=self.BG_COLOR)

        # ===== 프레임 설정 =====
        self.main_frame = tk.Frame(self.root, bg=self.SIDEBAR_COLOR)
        self.main_frame.pack(expand=True, fill="both")
        self.frames["main"] = self.main_frame

        # ===== 메인 프레임 구성 =====
        self.main_frame.grid_rowconfigure(0, weight=1)
        self.main_frame.grid_columnconfigure(0, weight=0)  # 종류 선택
        self.main_frame.grid_columnconfigure(1, weight=1)  # 대화상대
        self.main_frame.grid_columnconfigure(2, weight=3)  # 채팅창 (조금 줄임)
        self.main_frame.grid_columnconfigure(3, weight=2)  # 사건파일 패널 (새로 추가)
        self.main_frame.grid_columnconfigure(4, weight=2)  # 프로필 패널

        # ===== 결론 버튼 =====
        conclusion_sidebar = tk.Frame(self.main_frame, bg=self.SIDEBAR_COLOR, width=150)
        conclusion_sidebar.grid(row=0, column=0, sticky="nsew")
        conclusion_sidebar.grid_propagate(False)

        tk.Label(conclusion_sidebar, text="결론 제출", bg=self.SIDEBAR_COLOR, font=("Arial", 14)).pack(pady=(20,10))
        btn = tk.Button(
            conclusion_sidebar,
            text="결론 작성",
            font=("Arial", 12),
            width=12,
            command=self.open_conclusion
        )
        btn.pack(pady=10)


        # ===== 대화상대 리스트 =====
        sidebar_left = tk.Frame(self.main_frame, bg=self.SIDEBAR_COLOR)
        sidebar_left.grid(row=0, column=1, sticky="nsew")
        tk.Label(sidebar_left, text="대화상대", bg=self.SIDEBAR_COLOR, font=("Arial", 14)).pack(pady=10)

        self.contact_list = tk.Listbox(sidebar_left)
        for name in self.CHAT_PARTNERS:
            self.contact_list.insert(tk.END, name)
        self.contact_list.pack(expand=True, fill="both", padx=10, pady=10)
        self.contact_list.bind("<<ListboxSelect>>", self.update_profile)

        tk.Button(sidebar_left, text="대화상대 추가", command=self.add_new_contact).pack(fill="x", padx=10, pady=5)

        # ===== 채팅창 (Canvas + Frame) =====
        chat_frame = tk.Frame(self.main_frame, bg=self.CHAT_BG , bd=1, relief="sunken")
        chat_frame.grid(row=0, column=2, sticky="nsew", padx=5, pady=5)

        self.chat_canvas = tk.Canvas(chat_frame, bg=self.CHAT_BG, highlightthickness=0)
        scrollbar = tk.Scrollbar(chat_frame, command=self.chat_canvas.yview)
        self.chat_canvas.configure(yscrollcommand=scrollbar.set)

        self.chat_inner_frame = tk.Frame(self.chat_canvas, bg=self.CHAT_BG)
        self.chat_inner_frame.grid_columnconfigure(0, weight=1)

        self.chat_inner_id = self.chat_canvas.create_window((0, 0), window=self.chat_inner_frame, anchor="nw")
        self.chat_canvas.bind("<Configure>", lambda e: self.chat_canvas.itemconfig(self.chat_inner_id, width=e.width))

        self.chat_inner_frame.bind(
            "<Configure>",
            lambda e: self.chat_canvas.configure(scrollregion=self.chat_canvas.bbox("all"))
        )

        self.chat_canvas.grid(row=0, column=0, columnspan=2, sticky="nsew")
        scrollbar.grid(row=0, column=2, sticky="ns")

        chat_frame.grid_rowconfigure(0, weight=10)
        chat_frame.grid_rowconfigure(1, weight=1)
        chat_frame.grid_columnconfigure(0, weight=1)

        self.chat_entry = tk.Entry(chat_frame, font=("Arial", 12))
        self.chat_entry.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)
        send_button = tk.Button(chat_frame, text="전송", font=("Arial", 12), command=self.send_message)
        send_button.grid(row=1, column=1, sticky="nsew", padx=5, pady=5)
        self.chat_entry.bind("<Return>", self.send_message)

        # ===== 사건파일 패널 (column=3) =====
        file_panel = tk.Frame(self.main_frame, bg=self.SIDEBAR_COLOR, bd=0, relief="flat")
        file_panel.grid(row=0, column=3, sticky="nsew", padx=(0,5), pady=5)

        # 탭 버튼들 (크롬탭 느낌)
        tab_frame = tk.Frame(file_panel, bg=self.SIDEBAR_COLOR)
        tab_frame.pack(side="top", fill="x")

        self.case_tabs = []
        self.selected_tab_index = tk.IntVar(value=0)

        def switch_tab(index):
            self.selected_tab_index.set(index)
            for i, btn in enumerate(self.case_tabs):
                if i == index:
                    btn.config(bg="#ffffff", relief="flat")
                else:
                    btn.config(bg="#cccccc", relief="flat")
            for i, frame in enumerate(self.case_contents):
                frame.pack_forget()
                if i == index:
                    frame.pack(fill="both", expand=True)

        tab_names = ["사건 A", "사건 B", "사건 C"]
        self.case_contents = []

        for idx, name in enumerate(tab_names):
            btn = tk.Button(tab_frame, text=name, bd=0, font=("Arial", 10), padx=10,
                            command=lambda i=idx: switch_tab(i),
                            bg="#ffffff" if idx == 0 else "#cccccc")
            btn.pack(side="left", padx=(0, 1), ipadx=4, ipady=2)
            self.case_tabs.append(btn)

        # 사건 내용 영역
        for i in range(3):
            content = tk.Frame(file_panel, bg="#ffffff", bd=0, relief="solid")
            tk.Label(content, text=f"{tab_names[i]}의 내용", bg="#ffffff",
                    font=("Arial", 11), wraplength=200, justify="left").pack(padx=10, pady=10)
            self.case_contents.append(content)

        # 첫 번째 탭 내용 표시
        self.case_contents[0].pack(fill="both", expand=True)

        # ===== 우측 프로필 패널 =====
        sidebar_right = tk.Frame(self.main_frame, bg=self.SIDEBAR_COLOR)
        sidebar_right.grid(row=0, column=4, sticky="nsew")

        profile_frame = tk.Frame(sidebar_right, bg=self.SIDEBAR_COLOR)
        profile_frame.pack(fill="x", padx=10, pady=10)

        self.profile_img_label = tk.Label(profile_frame, bg=self.SIDEBAR_COLOR)
        self.profile_img_label.pack(pady=(0, 5))

        self.profile_label = tk.Label(profile_frame, text="", bg=self.SIDEBAR_COLOR, font=("Arial", 12))
        self.profile_label.pack(anchor="w")

        self.profile_info = tk.Text(profile_frame, height=5, width=25, wrap="word",
                                    bg=self.SIDEBAR_COLOR, font=("Arial", 10), relief="flat")
        self.profile_info.config(state="disabled")
        self.profile_info.pack(anchor="w")

        btn_frame = tk.Frame(sidebar_right, bg=self.SIDEBAR_COLOR)
        btn_frame.pack(side="bottom", fill="x", padx=10, pady=10)

        tk.Button(btn_frame, text="메모장", command=self.open_memo).pack(fill="x", pady=2)
        tk.Button(btn_frame, text="나가기", command=self.root.quit).pack(fill="x", pady=2)

        self.update_profile_by_name(self.current_contact)

    # ==== 말풍선 추가 ====
    def add_message(self, text, is_user=True):
        wrapper = tk.Frame(self.chat_inner_frame, bg=self.CHAT_BG)
        wrapper.grid(sticky="ew", padx=10, pady=2)
        wrapper.grid_columnconfigure(0, weight=1)

        msg_frame = tk.Frame(wrapper, bg=self.CHAT_BG)

        msg = tk.Label(
            msg_frame,
            text=text,
            bg="#d9edf7" if is_user else "#eeeeee",
            font=("Arial", 11),
            wraplength=300,
            justify="left",
            bd=0,
            relief="flat",
            padx=8,
            pady=6
        )

        tail = tk.Label(
            msg_frame,
            text="▶" if is_user else "◀",
            bg=self.CHAT_BG,
            fg="#d9edf7" if is_user else "#eeeeee",
            font=("Arial", 10)
        )

        msg_frame.grid_columnconfigure(0, weight=1)
        msg_frame.grid_columnconfigure(1, weight=0)
        if is_user:
            msg.grid(row=0, column=0, sticky="e")
            tail.grid(row=0, column=1, sticky="e", padx=(2,0))
            msg_frame.grid(row=0, column=1, sticky="e")
        else:
            tail.grid(row=0, column=0, sticky="w", padx=(0,2))
            msg.grid(row=0, column=1, sticky="w")
            msg_frame.grid(row=0, column=0, sticky="w")

        self.chat_canvas.yview_moveto(1.0)

    def send_message(self, event=None):
        message = self.chat_entry.get().strip()
        if not message:
            return
        self.chat_entry.delete(0, tk.END)
        self.add_message(f"나: {message}", is_user=True)
        with open(f"chat_{self.current_contact}.txt", "a", encoding="utf-8") as f:
            f.write(f"나: {message}\n")

    def update_profile(self, event):
        selection = self.contact_list.curselection()
        if not selection:
            return
        name = self.contact_list.get(selection[0])
        self.update_profile_by_name(name)

    def update_profile_by_name(self, name):
        self.current_contact = name
        info = self.profiles[name]
        self.profile_label.config(text=f"프로필: {name}")
        self.profile_info.config(state="normal")
        self.profile_info.delete("1.0", tk.END)
        self.profile_info.insert(tk.END, info["description"])
        self.profile_info.config(state="disabled")

        try:
            img = Image.open(info["img_path"])
            img = img.resize(self.PROFILE_IMG_SIZE, Image.Resampling.LANCZOS)
            self.current_img = ImageTk.PhotoImage(img)
            self.profile_img_label.config(image=self.current_img)
            self.profile_img_label.image = self.current_img
        except:
            pass

        for widget in self.chat_inner_frame.winfo_children():
            widget.destroy()
        file_path = f"chat_{name}.txt"
        if os.path.exists(file_path):
            with open(file_path, "r", encoding="utf-8") as f:
                for line in f:
                    self.add_message(line.strip(), is_user=True)

    def add_new_contact(self):
        # 전화번호 입력 받기
        phone = simpledialog.askstring("대화상대 추가", "전화번호(숫자만)를 입력하세요:")
        if not phone or not phone.isdigit():
            return  # 취소 또는 숫자가 아닌 입력 무시

        # 미리 설정된 번호인지 체크
        if phone in self.phone_book:
            info = self.phone_book[phone]
            new_name = info["name"]
            # 프로필 딕셔너리에 미리 저장
            self.profiles[new_name] = {
                "img_path": info["img_path"],
                "description": info["description"]
            }
        else:
            # 등록된 번호가 아니면 그냥 번호 자체를 이름으로 사용
            new_name = phone
            self.profiles[new_name] = {
                "img_path": "images/default.png",
                "description": f"{new_name} (사전 정보 없음)"
            }

        # 리스트와 내부 데이터 구조에 반영
        if new_name not in self.CHAT_PARTNERS:
            self.CHAT_PARTNERS.append(new_name)
            self.contact_list.insert(tk.END, new_name)
            # 대화 기록용 파일 미리 생성
            open(f"chat_{new_name}.txt", "w", encoding="utf-8").close()

    def open_conclusion(self):
        # Toplevel 창 띄우기
        win = tk.Toplevel(self.root)
        win.title("결론 제출")
        win.geometry("400x300")
        win.configure(bg=self.BG_COLOR)

        # 서류 느낌 내기: 테두리 없애고 살짝 그림자나 padding 활용
        container = tk.Frame(win, bg="white", bd=1, relief="solid")
        container.pack(expand=True, fill="both", padx=20, pady=20)

        tk.Label(container, text="용의자 이름:", bg="white", font=("Arial", 12)).pack(anchor="w", pady=(10,0), padx=10)
        suspect_entry = tk.Entry(container, font=("Arial", 12))
        suspect_entry.pack(fill="x", padx=10, pady=(0,10))

        tk.Label(container, text="이유:", bg="white", font=("Arial", 12)).pack(anchor="w", padx=10)
        reason_txt = tk.Text(container, height=6, wrap="word", font=("Arial", 11), bd=1, relief="solid")
        reason_txt.pack(expand=True, fill="both", padx=10, pady=(0,10))

        def submit():
            suspect = suspect_entry.get().strip()
            reason = reason_txt.get("1.0", "end").strip()
            # TODO: 나중에 결과 처리 로직
            print(f"제출된 결론 → 용의자: {suspect}, 이유: {reason}")
            win.destroy()

        submit_btn = tk.Button(container, text="제출", font=("Arial", 12), command=submit)
        submit_btn.pack(pady=(0,10))

    def open_memo(self):
        memo_window = tk.Toplevel(self.root)
        memo_window.title("메모장")
        memo_window.geometry("400x300")
        text_area = tk.Text(memo_window, wrap="word", font=("Arial", 12))
        text_area.pack(expand=True, fill="both", padx=10, pady=(10, 0))

        if os.path.exists(self.memo_file):
            with open(self.memo_file, "r", encoding="utf-8") as f:
                text_area.insert(tk.END, f.read())

        def save_and_close():
            with open(self.memo_file, "w", encoding="utf-8") as f:
                f.write(text_area.get("1.0", tk.END))
            memo_window.destroy()

        memo_window.protocol("WM_DELETE_WINDOW", save_and_close)

# ==== 실행 ====
if __name__ == "__main__":
    root = tk.Tk()
    app = ChatApp(root)
    root.mainloop()