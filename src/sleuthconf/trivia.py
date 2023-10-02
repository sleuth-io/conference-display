from dataclasses import dataclass

import yaml


@dataclass
class Question:
    name: str
    choices: list[str]
    answer: str


class Trivia:
    questions: list[Question] = []

    def __init__(self, data):
        self.questions.clear()
        data = data["questions"]
        for item in data:
            q = Question(
                name=item['name'],
                choices=item['choices'],
                answer=item['answer']
            )
            self.questions.append(q)
