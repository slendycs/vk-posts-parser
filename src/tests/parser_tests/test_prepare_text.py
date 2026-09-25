import allure
import pytest

from parser.parser import prepare_post_text


@pytest.mark.parser
@pytest.mark.unit
class TestPreparePostText:
    test_data = [
        ('Empty text', '', ''),
        ('Only Emoji text', '😒😒😒😒😒😪😪😪😪😪🥵🥵🥵🥵🥵', ''),
        ('Emoji and text', '😒😒😒Папочка🥵🥵🥵', 'Папочка'),
        ('Short censored word', '[#blur|хуй|&$!]', 'хуй'),
        ('Long censored word', '[#blur|еблан|&$!#%]', 'еблан'),
        ('Censored Article', '[#blur|Хуй|&$!] [#blur|хуй|&$!] да да?', 'Хуй хуй да да?'),
        ('Only whitespace', '   \n\t  ', '   \n\t  '),
        ('Malformed blur tag (no match)', '[#blur|broken_tag]', '[#blur|broken_t...'),
        ('Text exactly at limit', 'Ровно15символов', 'Ровно15символов'),
        ('Text longer than limit (default truncation)', 'Этот текст явно длиннее пятнадцати символов', 'Этот текст явно...'),
        ('Punctuation and newlines preserved', 'Привет, мир!\nКак дела?', 'Привет, мир!\nКа...'),
        ('Combined censored text and emojis', '🥵🥵🥵🥵[#blur|Хуй|&$!] [#blur|хуй|&$!] да да?🥵🥵🥵🥵', 'Хуй хуй да да?')
    ]

    @pytest.mark.parametrize("title, raw_text, expected_text", test_data)
    def test_prepare_text(self, title, raw_text, expected_text):
        allure.dynamic.title(title)
        with allure.step('#1. Prepare text'):
            prepared_text = prepare_post_text(raw_text)
        with allure.step('#2. Assert text with expected'):
            assert prepared_text == expected_text, f'The text ({prepared_text}) does not match what was expected'