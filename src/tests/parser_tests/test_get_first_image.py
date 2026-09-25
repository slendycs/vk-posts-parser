import allure
import pytest

from parser.parser import get_first_image

from tests.test_data import (one_post_response,
                             post_without_image,
                             post_two_image,
                             post_photo_video,
                             post_two_video)


@pytest.mark.parser
@pytest.mark.unit
class TestGetFirstImage:
    test_data = [
        (
            'One image in JSON', 
            one_post_response, 
            'https://sun9-25.vkuserphoto.ru/s/v1/ig2/c5Cs3y8IjYXCcE7LTmtRI9Htf7vaD1vEp-9zG2f8jBCUEag22Vhflx0_SPi08SOqq3bM2QwDhNyq0fn-pf2PRvT2.jpg?quality=95&crop=0,0,499,708&as=32x45,48x68,72x102,108x153,160x227,240x341,360x511,480x681,499x708&from=bu&u=EE3ltkSEi6IlvqKgbEwgFEp7-TB5NpMi-HUg-PfFfug'
        ),
        (
            'No image in JSON',
            post_without_image,
            ''
        ),
        (
            'Two image in JSON',
            post_two_image,
            'https://sun9-36.vkuserphoto.ru/s/v1/ig2/q8HyyRVPROhUoz4Z15lYiFkhc-709GUuBpqnO9O-7ERO3y1rTuljHBuupXa2DB0HHNLQEnosTW5ZeudxloA3AwsB.jpg?quality=95&crop=0,0,1200,674&as=32x18,48x27,72x40,108x61,160x90,240x135,360x202,480x270,540x303,640x359,720x404,1080x607,1200x674&from=bu&u=h7dkKfhFZOzwugzsjNhj8ECYO7lFN9i-LANoxT1hRjk'
        ),
        (
            'Photo and video in JSON',
            post_photo_video,
            'https://sun9-3.userapi.com/s/v1/ig2/GlzLegPYbxfIqHDwVd7sDYGznwAPlKEJCcb204_qge2iemmfoYbrDQJiVMEkFXVeHrK4yC41f996SU2p-BAn3V4H.jpg?quality=95&crop=0,0,216,205&as=32x30,48x46,72x68,108x102,160x152,216x205&from=bu&u=5hHdTAuf0t4biIVbuya-Xgsi6O09ryKo6FnJn5eY1o8'
        ),
        (
            'Two video in JSON',
            post_two_video,
            ''
        )
    ]


    @pytest.mark.parametrize('title, raw_json, expected_url', test_data)
    def test_get_first_image(self, title, raw_json, expected_url):
        allure.dynamic.title(title)
        with allure.step('#1. Prepare JSON'):
            json_response = raw_json['response']['items']
            item = json_response[0]
            attachments = item['attachments']
        with allure.step('#2. Try to get first image URL'):
            url = get_first_image(attachments)
        with allure.step('#3. Assert url with expected'):
            assert url == expected_url, f'The link ({url}) does not match the expected one'
