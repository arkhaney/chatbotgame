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

        # ==== 난이도별 전화번호 매핑 ====
        # key: 난이도, value: { 전화번호: {name, img_path, description} }
        self.phone_books = {
            "쉬움": {
                "01011112222": {
                    "name": "초보 용의자 A",
                    "img_path": "images/beginner_suspect.png",
                    "description": "쉬움 난이도의 주요 용의자입니다."
                },
            },
            "어려움": {
                "01033334444": {
                    "name": "고급 용의자 C",
                    "img_path": "images/hard_suspect.png",
                    "description": "어려움 난이도의 핵심 용의자입니다."
                },
            }
        }

        # 현재 쓰게 될 사전 (configure_partners에서 덮어씌워짐)
        self.phone_book = {}

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

        for level in ["쉬움","어려움"]:
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

        # 난이도별 전화번호 사전 로드
        self.phone_book = self.phone_books.get(difficulty, {})

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
        # 사건 내용 영역
        self.case_data = {
            "쉬움": {
                "사건 A": [("2000년 뉴스", "2000년에 발생한 사건의 개요입니다."),
                        ("초기 용의자", "당시 용의자는 3명이었으며, 모두 알리바이를 주장했습니다.")],
                "사건 B": [("2010년 CCTV", "사건 당일 CCTV 기록이 일부 손상되었습니다.")],
                "사건 C": [("2020년 탐문 결과", "이웃의 증언에 따르면 평소와 다른 점이 관찰되었다고 합니다.")]
            },
            "어려움": {
                "사건 A": [("2000년 수사보고서", "상세한 분석이 포함된 보고서입니다."),
                        ("현장 사진", "피해자의 위치와 주변 환경을 담은 사진.")],
                "사건 B": [("2010년 감식결과", "지문과 DNA가 일치하지 않았습니다.")],
                "사건 C": [("2020년 금융기록", "금전 거래 내역이 수상하다는 의견이 제시되었습니다.")]
            }
        }

        # 사건 내용 영역
        self.case_contents = []

        for i in range(3):
            content_frame = tk.Frame(file_panel, bg="#ffffff", bd=0, relief="solid")

            # 스크롤 가능한 Canvas + 내부 Frame
            canvas = tk.Canvas(content_frame, bg="#ffffff", highlightthickness=0)
            scrollbar = tk.Scrollbar(content_frame, command=canvas.yview)
            canvas.configure(yscrollcommand=scrollbar.set)

            inner = tk.Frame(canvas, bg="#ffffff")
            inner_id = canvas.create_window((0, 0), window=inner, anchor="nw")

            # 캔버스 크기 바뀔 때 inner 폭 조정
            canvas.bind("<Configure>", lambda e, c=canvas, i=inner_id: c.itemconfigure(i, width=e.width))
            inner.bind("<Configure>", lambda e, c=canvas: c.configure(scrollregion=c.bbox("all")))

            canvas.pack(side="left", fill="both", expand=True)
            scrollbar.pack(side="right", fill="y")

            # 정보 카드 추가
            current_tab = tab_names[i]
            current_data = self.case_data[self.difficulty][current_tab]

            for title, detail in current_data:
                # 카드 상자 프레임
                card = tk.Frame(inner, bg="#ffffff", bd=0, relief="flat")
                card.pack(fill="x", expand=True, padx=10, pady=0)  # 간격 없애기

                # 버튼 (정보 타이틀)
                btn = tk.Button(
                    card,
                    text=title,
                    font=("Arial", 13),
                    bg="#ffffff",
                    bd=0,
                    anchor="w",
                    height=3,  # 높이를 키움
                    wraplength=600,
                    command=lambda t=title, d=detail: self.open_info_popup(t, d)
                )
                btn.pack(fill="x", expand=True, padx=20, pady=(10, 10))  # 버튼 내부 여백

                # 🔽 연한 구분선 추가
                separator = tk.Frame(inner, bg="#dddddd", height=1)
                separator.pack(fill="x", padx=10)

            self.case_contents.append(content_frame)


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

        switch_tab(0)


        # ==== 팝업 함수 추가 ====
    def open_info_popup(self, title, detail):
        win = tk.Toplevel(self.root)
        win.title(title)
        win.geometry("400x300")
        win.configure(bg="white")

        tk.Label(win, text=title, bg="white", font=("Arial", 14, "bold")).pack(anchor="w", padx=15, pady=(15, 5))
        text = tk.Text(win, wrap="word", font=("Arial", 11), bg="white", relief="flat")
        text.insert(tk.END, detail)
        text.config(state="disabled")
        text.pack(expand=True, fill="both", padx=15, pady=(0, 15))

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