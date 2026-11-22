def read_number(prompt, minimum, maximum):
    while True:
        raw = input(prompt).strip()

        if not raw:
            print("입력이 비어 있습니다. 숫자를 입력하세요.")
            continue

        try:
            number = int(raw)
        except ValueError:
            print("숫자로 입력하세요.")
            continue

        if minimum <= number <= maximum:
            return number

        print(f"{minimum}~{maximum} 사이의 숫자를 입력하세요.")


class QuizGame:
    def show_menu(self):
        print("\n=== Python 기초 상식 퀴즈 ===")
        print("1. 퀴즈 풀기")
        print("2. 퀴즈 추가")
        print("3. 퀴즈 목록")
        print("4. 점수 확인")
        print("5. 종료")

    def run(self):
        try:
            while True:
                self.show_menu()
                choice = read_number("선택: ", 1, 5)

                if choice == 5:
                    print("게임을 종료합니다.")
                    break

                print("이 기능은 다음 단계에서 구현합니다.")
        except (KeyboardInterrupt, EOFError):
            print("\n입력이 중단되어 게임을 종료합니다.")


if __name__ == "__main__":
    QuizGame().run()