import customtkinter as ctk

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


class WelcomeApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Welcome")
        self.geometry("900x560")
        self.minsize(900, 560)

        # Основная сетка
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Левая декоративная панель
        self.left_frame = ctk.CTkFrame(self, corner_radius=0, fg_color="#111827")
        self.left_frame.grid(row=0, column=0, sticky="nsew")

        self.left_frame.grid_rowconfigure(0, weight=1)
        self.left_frame.grid_rowconfigure(1, weight=1)
        self.left_frame.grid_rowconfigure(2, weight=1)
        self.left_frame.grid_columnconfigure(0, weight=1)

        logo = ctk.CTkLabel(
            self.left_frame,
            text="✨",
            font=("Arial", 48, "bold")
        )
        logo.grid(row=0, column=0, sticky="s", pady=(40, 10))

        title = ctk.CTkLabel(
            self.left_frame,
            text="Welcome Back",
            font=("Arial", 34, "bold"),
            text_color="#F9FAFB"
        )
        title.grid(row=1, column=0, sticky="n", pady=(0, 10))

        subtitle = ctk.CTkLabel(
            self.left_frame,
            text="Создай аккаунт и начни работу\nв красивом приветственном окне",
            font=("Arial", 16),
            text_color="#9CA3AF",
            justify="center"
        )
        subtitle.grid(row=1, column=0, sticky="n", pady=(60, 0))

        footer = ctk.CTkLabel(
            self.left_frame,
            text="CustomTkinter Demo",
            font=("Arial", 13),
            text_color="#6B7280"
        )
        footer.grid(row=2, column=0, sticky="s", pady=30)

        # Правая часть с формой
        self.right_frame = ctk.CTkFrame(self, corner_radius=0, fg_color="#1F2937")
        self.right_frame.grid(row=0, column=1, sticky="nsew")

        self.form_card = ctk.CTkFrame(
            self.right_frame,
            width=420,
            height=420,
            corner_radius=24,
            fg_color="#0F172A"
        )
        self.form_card.place(relx=0.5, rely=0.5, anchor="center")

        self.form_card.grid_propagate(False)

        form_title = ctk.CTkLabel(
            self.form_card,
            text="Регистрация",
            font=("Arial", 28, "bold"),
            text_color="#F8FAFC"
        )
        form_title.pack(pady=(35, 8))

        form_subtitle = ctk.CTkLabel(
            self.form_card,
            text="Заполни поля ниже, чтобы продолжить",
            font=("Arial", 14),
            text_color="#94A3B8"
        )
        form_subtitle.pack(pady=(0, 24))

        self.name_entry = ctk.CTkEntry(
            self.form_card,
            width=300,
            height=42,
            corner_radius=14,
            placeholder_text="Имя"
        )
        self.name_entry.pack(pady=8)

        self.email_entry = ctk.CTkEntry(
            self.form_card,
            width=300,
            height=42,
            corner_radius=14,
            placeholder_text="Email"
        )
        self.email_entry.pack(pady=8)

        self.password_entry = ctk.CTkEntry(
            self.form_card,
            width=300,
            height=42,
            corner_radius=14,
            placeholder_text="Пароль",
            show="*"
        )
        self.password_entry.pack(pady=8)

        self.register_button = ctk.CTkButton(
            self.form_card,
            width=300,
            height=42,
            corner_radius=14,
            text="Создать аккаунт",
            font=("Arial", 15, "bold"),
            command=self.register
        )
        self.register_button.pack(pady=(18, 12))

        self.status_label = ctk.CTkLabel(
            self.form_card,
            text="",
            font=("Arial", 13),
            text_color="#22C55E"
        )
        self.status_label.pack(pady=(6, 0))

    def register(self):
        name = self.name_entry.get().strip()
        email = self.email_entry.get().strip()
        password = self.password_entry.get().strip()

        if not name or not email or not password:
            self.status_label.configure(
                text="Пожалуйста, заполни все поля",
                text_color="#EF4444"
            )
            return

        self.status_label.configure(
            text=f"Добро пожаловать, {name} ✨",
            text_color="#22C55E"
        )


if __name__ == "__main__":
    app = WelcomeApp()
    app.mainloop()