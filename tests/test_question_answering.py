# pylint: disable=missing-function-docstring

from server.features.llm.types import Message
from server.features.query.question_answering import question_answering


def chain(messages: list[Message]) -> Message | None:

    if len(messages) > 1:
        return None

    return {'role': 'assistant', 'content': 'Hello world!'}


def test_question_answering():

    messages: list[Message] = [
        {'role': 'assistant', 'content': 'Hello world!'},
        {'role': 'user', 'content': 'Hello world!'}
    ]

    answers = question_answering(messages, chain)

    assert len(answers) == 2
    assert answers[-1]['role'] == 'assistant'
