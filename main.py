import json
from pathlib import Path

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
        self.best_score = None
        self.state_path = Path(__file__).resolve().with_name("state.json")
        self.can_save = True

    def load_state(self):
        try:
            with self.state_path.open(encoding="utf-8") as file:
                data = json.load(file)

            records = data["quizzes"]
            best_score = data["best_score"]

            if not isinstance(records, list):
                raise ValueError("퀴즈 목록 형식이 올바르지 않습니다.")

            if best_score is not None and (
                type(best_score) is not int or best_score < 0
            ):
                raise ValueError("최고 기록 형식이 올바르지 않습니다.")

            quizzes = []
            for record in records:
                question = record["question"]
                choices = record["choices"]
                answer = record["answer"]

                if not isinstance(question, str) or not question.strip():
                    raise ValueError("문제가 비어 있습니다.")

                if (
                    not isinstance(choices, list)
                    or len(choices) != 4
                    or any(
                        not isinstance(choice, str) or not choice.strip()
                        for choice in choices
                    )
                ):
                    raise ValueError("선택지 형식이 올바르지 않습니다.")

                if type(answer) is not int or not 1 <= answer <= 4:
                    raise ValueError("정답 번호는 1~4여야 합니다.")

                quizzes.append(Quiz(question, choices, answer))

        except FileNotFoundError:
            return
        except (ValueError, TypeError, KeyError):
            print("저장 파일이 손상되어 기본 퀴즈로 시작합니다.")
            return
        except OSError as error:
            self.can_save = False
            print(f"저장 파일을 읽을 수 없습니다. 이번 실행의 저장이 꺼집니다. ({error})")
            return

        self.quizzes = quizzes
        self.best_score = best_score
        print(f"저장된 퀴즈 {len(self.quizzes)}개를 불러왔습니다.")

    def save_state(self):
        if not self.can_save:
            return False

        data = {
            "quizzes": [
                {
                    "question": quiz.question,
                    "choices": quiz.choices,
                    "answer": quiz.answer,
                }
                for quiz in self.quizzes
            ],
            "best_score": self.best_score,
        }

        temp_path = self.state_path.with_suffix(".json.tmp")
        try:
            with temp_path.open("w", encoding="utf-8") as file:
                json.dump(data, file, ensure_ascii=False, indent=2)
                file.write("\n")
            temp_path.replace(self.state_path)
        except OSError as error:
            print(f"데이터를 저장하지 못했습니다. ({error})")
            return False

        return True

    def show_menu(self):
        print("\n=== Python 기초 상식 퀴즈 ===")
        print("1. 퀴즈 풀기")
        print("2. 퀴즈 추가")
        print("3. 퀴즈 목록")
        print("4. 점수 확인")
        print("5. 종료")

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

        if self.best_score is None or correct_count > self.best_score:
            self.best_score = correct_count
            print("새로운 최고 기록입니다!")
            self.save_state()

    def add_quiz(self):
        question = read_text("문제: ")
        choices = []

        for number in range(1, 5):
            choices.append(read_text(f"선택지 {number}: "))

        answer = read_number("정답 번호 (1~4): ", 1, 4)
        self.quizzes.append(Quiz(question, choices, answer))

        if self.save_state():
            print(f"퀴즈가 추가되었습니다. 현재 총 {len(self.quizzes)}문제입니다.")
        else:
            print("이번 실행의 목록에 퀴즈를 추가했습니다. 파일 저장에 실패했습니다.")

    def list_quizzes(self):
        if not self.quizzes:
            print("등록된 퀴즈가 없습니다.")
            return

        print(f"\n등록된 퀴즈 (총 {len(self.quizzes)}개)")
        for number, quiz in enumerate(self.quizzes, start=1):
            print(f"[{number}] {quiz.question}")

    def show_best_score(self):
        if self.best_score is None:
            print("아직 완료한 퀴즈가 없습니다.")
            return

        print(f"최고 기록: {self.best_score}문제 정답")

    def run(self):
        try:
            self.load_state()

            while True:
                self.show_menu()
                choice = read_number("선택: ", 1, 5)

                if choice == 1:
                    self.play()
                elif choice == 2:
                    self.add_quiz()
                elif choice == 3:
                    self.list_quizzes()
                elif choice == 4:
                    self.show_best_score()
                elif choice == 5:
                    print("게임을 종료합니다.")
                    break
        except (KeyboardInterrupt, EOFError):
            print("\n입력이 중단되어 게임을 종료합니다.")
        finally:
            self.save_state()


if __name__ == "__main__":
    QuizGame().run()