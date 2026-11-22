from quiz import Quiz


def create_default_quizzes():
    return [
        Quiz("문자열을 나타내는 자료형은?", ["int", "str", "bool", "list"], 2),
        Quiz("리스트의 첫 번째 인덱스는?", ["0", "1", "2", "-1"], 1),
        Quiz("키로 값을 찾는 자료형은?", ["str", "list", "dict", "bool"], 3),
        Quiz("함수를 정의하는 키워드는?", ["class", "return", "for", "def"], 4),
        Quiz("len(['a', 'b', 'c'])의 결과는?", ["2", "3", "4", "6"], 2),
    ]