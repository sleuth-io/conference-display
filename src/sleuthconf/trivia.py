from dataclasses import dataclass

import yaml


@dataclass
class Question:
    name: str
    answer: str


class Trivia:
    questions: list[Question] = []

    def __init__(self, data):
        self.questions.clear()
        data = data["questions"]
        for item in data:
            q = Question(
                name=f"Q: {item['name']}",
                answer=f"A: {item['answer']}"
            )
            self.questions.append(q)
