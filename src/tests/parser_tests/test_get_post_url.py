import allure
import pytest

from parser.parser import get_post_url


@pytest.mark.parser
@pytest.mark.unit
class TestGetPostURL:
    test_data = [
        ('Normal case: user post', '123456', '789012', 'durov', 'https://vk.com/durov?w=wall123456_789012'),
        ('Normal case: group post (negative owner_id)', '-54321', '112233', 'club54321', 'https://vk.com/club54321?w=wall-54321_112233'),
        ('Empty owner_id', '', '789', 'test_domain', 'https://vk.com/test_domain?w=wall_789'),
        ('Empty id', '123456', '', 'durov', 'https://vk.com/durov?w=wall123456_'),
        ('Empty domain', '123456', '789012', '', 'https://vk.com/?w=wall123456_789012'),
        ('All empty strings', '', '', '', 'https://vk.com/?w=wall_'),
        ('Large numeric IDs', '999999999', '888888888', 'public123', 'https://vk.com/public123?w=wall999999999_888888888'),
        ('Domain with underscore/hyphen', '111', '222', 'my_community_2024', 'https://vk.com/my_community_2024?w=wall111_222'),
        ('Domain with dots (subdomain-like)', '333', '444', 'news.vk.team', 'https://vk.com/news.vk.team?w=wall333_444'),
        ('Unicode in domain', '555', '666', 'тест_домен', 'https://vk.com/тест_домен?w=wall555_666'),
        ('Special chars in owner_id (no encoding)', '123<script>', '456', 'durov', 'https://vk.com/durov?w=wall123<script>_456'),
        ('Spaces in parameters (no encoding)', '123 456', '78 90', 'my domain', 'https://vk.com/my domain?w=wall123 456_78 90'),
        ('Zero values', '0', '0', 'id0', 'https://vk.com/id0?w=wall0_0'),
        ('Very long domain', '1', '2', 'a' * 100, f'https://vk.com/{"a" * 100}?w=wall1_2'),
    ]

    @pytest.mark.parametrize("title, owner_id, id, domain, expected", test_data)
    def test_get_post_url(self, title, owner_id, id, domain, expected):
        allure.dynamic.title(title)
        with allure.step('#1. Get post URL'):
            result = get_post_url(owner_id, id, domain)
        with allure.step('#2. Assert post URL with expected'):
            assert result == expected, f'The link ({result}) does not match the expected one'
