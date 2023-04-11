from dataclasses import dataclass

import yaml


@dataclass
class Question:
    name: str
    answer: str


class Trivia:
    questions: list[Question] = []

    def __init__(self, path):
        self._path = path
        self._reload()

    def _reload(self):
        with open(self._path, "r") as stream:
            try:
                data = yaml.safe_load(stream)
            except yaml.YAMLError as exc:
                print(exc)

        self.questions.clear()
        data = data["questions"]
        for item in data:
            q = Question(
                name=item["name"],
                answer=item["answer"]
            )
            self.questions.append(q)
