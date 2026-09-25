import allure
import pytest
import requests

from parser.data_structures import Post
from parser.parser import parse_posts_from_json

from tests.test_data import (one_post_response, 
                             three_post_response, 
                             post_without_image,
                             post_without_text,
                             post_two_image,
                             post_photo_video,
                             post_two_video,
                             post_emojii_only,
                             post_emojii_with_text)


@pytest.mark.parser
@pytest.mark.unit
class TestParsePostsJson:
    # Ожидаемые списки постов
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

    one_post_without_image_data = [
        Post(post_text='МНЕ МАЛО МАЛО МАЛО ТЕБЯЯЯЯЯЯЯЯЯ ЗНАЮЮЮЮЮЮ ЯЯЯЯЯЯЯЯЯЯЯЯ САМАААААААААААА...', 
             first_image_url='',
             post_link='https://vk.com/slendycsama?w=wall600779498_52'
        )]
    
    one_post_without_text_data = [
        Post(post_text='',
            first_image_url='https://sun9-76.vkuserphoto.ru/s/v1/ig2/iD6Z_nm3JYqIKpEPZjGCQk4xpGmuFZY_Dl4kjoYb_wc2oo6'
                            'aYhVLyCQEXS3jhjnbTPA-vvu0yLzMFitNedlsuZOr.jpg?quality=95&crop=0,0,1080,625&as=32x19,48x28,72'
                            'x42,108x62,160x93,240x139,360x208,480x278,540x312,640x370,720x417,1080x625&from=bu&u=9uH-bDbH'
                            'sslueGpQMS_wXfKPEBFvKlT--fjwYhCltrA',
            post_link='https://vk.com/club238077517?w=wall-238077517_4'
        )]
    
    one_post_two_image_data = [
        Post(post_text='', 
             first_image_url='https://sun9-36.vkuserphoto.ru/s/v1/ig2/q8HyyRVPROhUoz4Z15lYiFkhc-709GUuBpqnO9O-7ERO3y1rTuljH'
                             'BuupXa2DB0HHNLQEnosTW5ZeudxloA3AwsB.jpg?quality=95&crop=0,0,1200,674&as=32x18,48x27,72x40,108x61,1'
                             '60x90,240x135,360x202,480x270,540x303,640x359,720x404,1080x607,1200x674&from=bu&u=h7dkKfhFZOzwugzsj'
                             'Nhj8ECYO7lFN9i-LANoxT1hRjk',
             post_link='https://vk.com/club238077517?w=wall-238077517_5'
        )]
    
    one_post_image_and_video_data = [
        Post(post_text='',
             first_image_url='https://sun9-3.userapi.com/s/v1/ig2/GlzLegPYbxfIqHDwVd7sDYGznwAPlKEJCcb204_qge2iemmfoYbrDQJiVMEkFXVeH'
                             'rK4yC41f996SU2p-BAn3V4H.jpg?quality=95&crop=0,0,216,205&as=32x30,48x46,72x68,108x102,160x152,216x205&'
                             'from=bu&u=5hHdTAuf0t4biIVbuya-Xgsi6O09ryKo6FnJn5eY1o8',
             post_link='https://vk.com/club238077517?w=wall-238077517_7'
        )]
    
    one_post_emojii_with_text_data = [
        Post(post_text='Хуй хуй да да?',
             first_image_url='',
             post_link='https://vk.com/club238077517?w=wall-238077517_10')
    ]


    # Наборы данных
    test_data = [
        ('Parse empty JSON', {'response': {'items': {}}}, [], 0, ''),
        ('Parse one item in JSON', one_post_response, three_posts_data, 1, 'club238077517'),
        ('Parse three items in JSON', three_post_response, three_posts_data, 3, 'club238077517'),
        ('Parse JSON with one item without image', post_without_image, one_post_without_image_data, 1, 'slendycsama'),
        ('Parse JSON with one item without text', post_without_text, one_post_without_text_data, 1, 'club238077517'),
        ('Parse JSON with one item with two image', post_two_image, one_post_two_image_data, 1, 'club238077517'),
        ('Parse JSON with one post with image and video', post_photo_video, one_post_image_and_video_data, 1, 'club238077517'),
        ('Parse JSON with one post with two video', post_two_video, [], 0, ''),
        ('Parse JSON with emojii only text', post_emojii_only, [], 0, ''),
        ('Parse JSON with emojii and text', post_emojii_with_text, one_post_emojii_with_text_data, 1, 'club238077517')
    ]


    # Тело теста
    @pytest.mark.parametrize("title, response, expected, count, domain", test_data)
    def test_parse_json(self, title, response, expected, count, domain):
        allure.dynamic.title(title)
        with allure.step('#1. Prepare JSON'):
            response = response.copy()
            response = response['response']['items']
        with allure.step('#2. Try to serialize JSON'):
            result:list[Post] = parse_posts_from_json(response, domain)
        with allure.step('#3. Assert post data'):
            with allure.step('#3.1 Assert posts count'):
                assert len(result) == count, 'The number of posts does not match' 
            for i in range(len(result)):
                with allure.step('#3.2 Assert post data with expectd'):
                    assert result[i] == expected[i], f'The post information ({result[i]}) does not match what was expected'
                with allure.step('#3.3 Check that links are valid'):
                    if result[i].first_image_url != '':
                        answer = requests.get(result[i].first_image_url)
                        assert answer.status_code == 200, 'The image link is broken'
                    if result[i].post_link != '':
                        answer = requests.get(result[i].post_link)
                        assert answer.status_code == 200, 'The post link is broken'

