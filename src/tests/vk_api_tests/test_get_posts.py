import allure
import pytest

from client.vk_errors import APICallError, NoItemsError
from parser.data_structures import Post

from tests.fixtures.vk_api_fixtures import vk_client


@pytest.mark.need_mock
@pytest.mark.vk
@pytest.mark.unit
@pytest.mark.asyncio
class TestGetPosts:
    basic_group_domain = 'club238077517'
    huge_posts_domain = 'schule75petrograd'
    no_valid_posts_domain = 'club238343321'

    three_posts_data = [
        Post(post_text='ЛЕГЕНДАРНЫЕ БОКА И ЖОКА НА СЦЕНЕ ПОПАПИСЯВВУВУ', 
             first_image_url='https://sun9-25.vkuserphoto.ru/s/v1/ig2/c5Cs3y8IjYXCcE7LTmtRI9Htf7vaD1vEp-9zG2f8jBCUEag22Vhf'
                             'lx0_SPi08SOqq3bM2QwDhNyq0fn-pf2PRvT2.jpg?quality=95&crop=0,0,499,708&as=32x45,48x68,72x102,108'
                             'x153,160x227,240x341,360x511,480x681,499x708&from=bu&u=EE3ltkSEi6IlvqKgbEwgFEp7-TB5NpMi-HUg-PfFfug',
             post_link='https://vk.com/club238077517?w=wall-238077517_3'),
        Post(post_text='Это я\n\nСори за детскую фотку ребята', 
             first_image_url='https://sun9-4.vkuserphoto.ru/s/v1/ig2/cAGekey43b_JRLspZy1gZDtRKQ34pvFOrxm2_FWcUb96DgMTF3S7TK_zu'
                             'C17n5DyDnMlWaAeZ5zovCTRjxsLACnt.jpg?quality=95&crop=0,0,736,736&as=32x32,48x48,72x72,108x108,160x'
                             '160,240x240,360x360,480x480,540x540,640x640,720x720,736x736&from=bu&u=C0xZvu-A8PU8LBz4Xp-Q7iZc1etZzzFXP7HwSP9Ljj0',
             post_link='https://vk.com/club238077517?w=wall-238077517_2'),
        Post(post_text='Я рот того всего ебал\n\nУ меня огромный пенис',
             first_image_url='https://sun9-48.vkuserphoto.ru/s/v1/ig2/B55jbLrmmE-osQCEuO2qwHKdBzJNLKUdPnIUd6XFYFN95ON-sqylCkoXmgU'
                             'XMIuMerl0XxwoEQvlyj-2aJo95KJS.jpg?quality=95&crop=0,0,400,400&as=32x32,48x48,72x72,108x108,160x160,2'
                             '40x240,360x360,400x400&from=bu&u=pH9AG3Flyvz0JIA_TrHPFJh7h83PtjX6c0ECwAuq4Q4',
             post_link='https://vk.com/club238077517?w=wall-238077517_1')
    ]


    test_data = [
        ('Get post with one symbol length', basic_group_domain, 1, 1, [Post('Л...', 
                                                                            'https://sun9-25.vkuserphoto.ru/s/v1/ig2/c5Cs3y8IjYXCcE7LTmtR'
                                                                                    'I9Htf7vaD1vEp-9zG2f8jBCUEag22Vhflx0_SPi08SOqq3bM2QwDhNyq0fn-'
                                                                                    'pf2PRvT2.jpg?quality=95&crop=0,0,499,708&as=32x45,48x68,72x1'
                                                                                    '02,108x153,160x227,240x341,360x511,480x681,499x708&from=bu&u'
                                                                                    '=EE3ltkSEi6IlvqKgbEwgFEp7-TB5NpMi-HUg-PfFfug', 
                                                                            'https://vk.com/club238077517?w=wall-238077517_3')]),
        ('Get post with zero symbol length', basic_group_domain, 1, 0, [Post('...', 
                                                                             'https://sun9-25.vkuserphoto.ru/s/v1/ig2/c5Cs3y8IjYXCcE7LTmtR'
                                                                                    'I9Htf7vaD1vEp-9zG2f8jBCUEag22Vhflx0_SPi08SOqq3bM2QwDhNyq0fn-'
                                                                                    'pf2PRvT2.jpg?quality=95&crop=0,0,499,708&as=32x45,48x68,72x1'
                                                                                    '02,108x153,160x227,240x341,360x511,480x681,499x708&from=bu&u'
                                                                                    '=EE3ltkSEi6IlvqKgbEwgFEp7-TB5NpMi-HUg-PfFfug', 
                                                                            'https://vk.com/club238077517?w=wall-238077517_3')]),
        ('Get one post', basic_group_domain, 1, 70, three_posts_data),
        ('Get three posts', basic_group_domain, 3, 70, three_posts_data)
    ]


    test_data_domain_problems = [
        ('Get posts from private domain', '372', 'Failed to execute method "wall.get": Some error from VK servers: This profile is private', APICallError),
        ('Get posts from banned domain', '323232323232', 'Failed to execute method "wall.get": Some error from VK servers: User was deleted or banned', APICallError),
        ('Get posts from wrong domain', '32323232323243', 'No post items for domain "32323232323243": VK returned empty posts list', NoItemsError)
    ]
    

    @pytest.mark.parametrize('title, domain, count, text_len, expected', test_data)
    async def test_get_posts(self, title, domain, count, text_len, 
                              expected, vk_client, caplog):
        allure.dynamic.title(title)
        with allure.step(f'#1. Try to execute method with domain: "{domain}"'):
            posts = await vk_client.get_posts(domain, count, text_len)
        with allure.step('#2. Check that logs is clear'):
            assert caplog.text == '', f'Some errors in logs: {caplog.text}'
        with allure.step('#3. Assert posts list with expected'):
            for i in range (len(posts)):
                assert posts[i] == expected[i], f'The post information ({posts[i]}) does not match what was expected'


    @pytest.mark.parametrize('title, domain, expected_log_msg, expected_exeption', test_data_domain_problems)
    async def test_get_posts_with_domain_problems(self, title, domain, expected_log_msg, expected_exeption, 
                                                  caplog, vk_client):
        allure.dynamic.title(title)
        with allure.step(f'#1. Try to execute method and check that method raised {str(expected_exeption)}'):
            with pytest.raises(expected_exeption):
                post = await vk_client.get_posts(domain, 1, 15)
        with allure.step('#2. Assert log message'):
            assert expected_log_msg in caplog.text, 'No error message found in logs'

    @allure.title('Get no valid post')
    async def test_get_no_valid_posts(self, vk_client, caplog):
        with allure.step('#1. #1. Try to execute method and check that method raised NoItemsError'):
            with pytest.raises(NoItemsError):
                post = await vk_client.get_posts(self.no_valid_posts_domain, 1, 15)
        with allure.step('#2. Assert log message'):
            assert f'No post items for domain "{self.no_valid_posts_domain}": Failed to retrieve valid data' in caplog.text, \
                'No error message found in logs'

    @allure.title('Get 100 posts')
    async def test_get_100_posts(self, vk_client, caplog):
        with allure.step('#1. Try to get 100 posts from VK'):
            posts = await vk_client.get_posts(self.huge_posts_domain, 100, 70)
        with allure.step('#2. Check that logs are empty'):
            assert caplog.text == '', f'Some errors in logs: {caplog.text}'
        with allure.step('#3 Check that posts count equals 98 (because we not parsing reposts)'):
            assert len(posts) == 98, 'Posts count not equal 98'