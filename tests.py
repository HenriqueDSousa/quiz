import pytest
from model import Question


def test_create_choice_with_invalid_text():
    question = Question(title='q1')
    with pytest.raises(Exception) as e:
        question.add_choice('', False)
        assert str(e.value) == 'Text cannot be empty'
    with pytest.raises(Exception) as e:
        question.add_choice('a'*101, False)
        assert str(e.value) == 'ext cannot be longer than 100 characters'

def test_create_question():
    question = Question(title='q1')
    assert question.id != None

def test_create_multiple_questions():
    question1 = Question(title='q1')
    question2 = Question(title='q2')
    assert question1.id != question2.id

def test_create_question_with_invalid_title():
    with pytest.raises(Exception):
        Question(title='')
    with pytest.raises(Exception):
        Question(title='a'*201)
    with pytest.raises(Exception):
        Question(title='a'*500)

def test_create_question_with_valid_points():
    question = Question(title='q1', points=1)
    assert question.points == 1
    question = Question(title='q1', points=100)
    assert question.points == 100

def test_create_question_with_invalid_points():
    with pytest.raises(Exception) as e:
        Question(title='q1', points=0)
        assert str(e.value) == 'Points must be between 1 and 100'


def test_create_choice():
    question = Question(title='q1')
    
    question.add_choice('a', False)

    choice = question.choices[0]
    assert len(question.choices) == 1
    assert choice.text == 'a'
    assert not choice.is_correct

def test_remove_choice():
    question = Question(title='q1')
    choice = question.add_choice('a', False)

    question.remove_choice_by_id(choice.id)
    assert question.choices == []

def test_remove_choice_with_invalid_id():
    question = Question(title='q1')
    choice = question.add_choice('a', False)

    with pytest.raises(Exception) as e:
        question.remove_choice_by_id('invalid-id')
        assert str(e.value) == 'Invalid choice ID'

def test_remove_all_choices():
    question = Question(title='q1')
    choice1 = question.add_choice('a', False)
    choice2 = question.add_choice('b', True)

    question.remove_all_choices()
    assert question.choices == []



def test_correct_selected_choices():
    question = Question(title='q1', max_selections=2)
    choice1 = question.add_choice('a', False)
    choice2 = question.add_choice('b', True)
    choice3 = question.add_choice('c', True)

    selected_ids = [choice2.id, choice3.id]
    assert question.correct_selected_choices(selected_ids)

def test_correct_selected_choices_with_invalid_choice():

    question = Question(title='q1', max_selections=2)
    choice1 = question.add_choice('a', False)
    choice2 = question.add_choice('b', True)

    selected_ids = [choice1.id,'invalid-id']
    with pytest.raises(Exception) as e:
        question.correct_selected_choices(selected_ids)
        assert str(e.value) == 'Invalid choice ID'

def test_invalid_len_selected_choices():
    question = Question(title='q1', max_selections=1)
    choice1 = question.add_choice('a', False)
    choice2 = question.add_choice('b', True)
    choice3 = question.add_choice('c', True)

    selected_ids = [choice2.id, choice3.id]
    with pytest.raises(Exception) as e:
        question.correct_selected_choices(selected_ids)
        assert str(e.value) == 'Cannot select more than 1 choices'

def test_set_correct_choices():

    question = Question(title='q1')
    choice1 = question.add_choice('a', False)
    choice2 = question.add_choice('b', True)
    choice3 = question.add_choice('c', True)

    question.set_correct_choices([choice2.id, choice3.id])
    assert choice1.is_correct == False
    assert choice2.is_correct
    assert choice3.is_correct


def test_raises_if_invalid_set_correct_choices():

    question = Question(title='q1')

    with pytest.raises(Exception) as e:
        question.set_correct_choices(['invalid-id'])

@pytest.fixture
def question_with_choices():

    q = Question(title="q1", max_selections=2)
    c1 = q.add_choice("a", False)
    c2 = q.add_choice("b", True)
    c3 = q.add_choice("c", True)
    return q, c1, c2, c3


@pytest.fixture
def empty_question():
    return Question(title="Questão vazia")

def test_find_correct_choice_ids(question_with_choices):
    q, c1, c2, c3 = question_with_choices

    correct_ids = q._find_correct_choice_ids()

    assert c2.id in correct_ids
    assert c3.id in correct_ids
    assert c1.id not in correct_ids
    assert len(correct_ids) == 2

def test_remove_all_choices_with_fixture(question_with_choices):
    q, c1, c2, c3 = question_with_choices

    assert len(q.choices) == 3

    q.remove_all_choices()

    assert q.choices == []
    assert q._list_choice_ids() == []
