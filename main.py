from default_quizzes import create_default_quizzes
from quiz import Quiz

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

def read_text(prompt):
    while True:
        value = input(prompt).strip()
        if value:
            return value

        print("빈 내용은 입력할 수 없습니다.")


class QuizGame:
    def __init__(self):
        self.quizzes = create_default_quizzes()

    def play(self):
        if not self.quizzes:
            print("등록된 퀴즈가 없습니다.")
            return

        correct_count = 0

        for number, quiz in enumerate(self.quizzes, start=1):
            print(f"\n[문제 {number}]")
            quiz.display()
            selected = read_number("정답 번호 (1~4): ", 1, 4)

            if quiz.is_correct(selected):
                correct_count += 1
                print("정답입니다!")
            else:
                correct_choice = quiz.choices[quiz.answer - 1]
                print(f"오답입니다. 정답은 {quiz.answer}번 {correct_choice}입니다.")

        print(f"\n{len(self.quizzes)}문제 중 {correct_count}문제 정답입니다.")
    def show_menu(self):
        print("\n=== Python 기초 상식 퀴즈 ===")
        print("1. 퀴즈 풀기")
        print("2. 퀴즈 추가")
        print("3. 퀴즈 목록")
        print("4. 점수 확인")
        print("5. 종료")

    def add_quiz(self):
        question = read_text("문제: ")
        choices = []

        for number in range(1, 5):
            choices.append(read_text(f"선택지 {number}: "))

        answer = read_number("정답 번호 (1~4): ", 1, 4)
        self.quizzes.append(Quiz(question, choices, answer))
        print(f"퀴즈가 추가되었습니다. 현재 총 {len(self.quizzes)}문제입니다.")

    def list_quizzes(self):
        if not self.quizzes:
            print("등록된 퀴즈가 없습니다.")
            return

        print(f"\n등록된 퀴즈 (총 {len(self.quizzes)}개)")
        for number, quiz in enumerate(self.quizzes, start=1):
            print(f"[{number}] {quiz.question}")    
    def run(self):
        try:
            while True:
                self.show_menu()
                choice = read_number("선택: ", 1, 5)

                if choice == 5:
                    print("게임을 종료합니다.")
                    break

                if choice == 1:
                    self.play()
                elif choice == 2:
                    self.add_quiz()
                elif choice == 3:
                    self.list_quizzes()
                else:
                    print("이 기능은 다음 단계에서 구현합니다.")
        except (KeyboardInterrupt, EOFError):
            print("\n입력이 중단되어 게임을 종료합니다.") 


if __name__ == "__main__":
    QuizGame().run()            