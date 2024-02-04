import pytest
import requests
from unittest.mock import Mock

# このロードで、__init__.pyに記載されているか？の検証も兼ねている。
from open_meteo_weather_sample_jpcity import get, list_locations



# モジュールレベルの定数として定義
EXPECTED_COORDINATES_DICT: dict = {
    "tokyo" : {
        "latitude" : "35.6785",
        "longitude": "139.6823",
    },
    "nagoya" : {
        "latitude" : "35.1814",
        "longitude": "136.9063",
    },
    "osaka" : {
        "latitude" : "34.6937",
        "longitude": "135.5021",
    },
}


# locationとして期待する配列を定義
EXPECTED_LOCATIONS_LIST = ["tokyo", "nagoya", "osaka"]

# locationとexpected_resultのペアをリストで定義
stub_response_in_locations = [
    ("tokyo", {
        "time"          : "dummy_time",
        "temperature_2m": "dummy_temperature"
    }),
    ("nagoya", {
        "time"          : "dummy_time",
        "temperature_2m": "dummy_temperature"
    }),
    ("osaka", {
        "time"          : "dummy_time",
        "temperature_2m": "dummy_temperature"
    })
]


def test_list_locations():
    expected_result = EXPECTED_LOCATIONS_LIST

    result = list_locations()
    assert result == expected_result, f"Expected {expected_result}, but got {result}"



# パラメータ化を利用してテストケースを定義
@pytest.mark.parametrize("location, stub_responce", stub_response_in_locations)
def test_get(location, stub_responce):
    """
    This is the title of the test case.
    """
    
    # モックオブジェクトを作成
    mock_response = Mock()
    mock_response.json.return_value = {"hourly": stub_responce}

    # requests.getをモックに置き換え
    requests.get = Mock(return_value=mock_response)

    # 関数をテスト
    result = get(location)
    assert result["location"] == location
    assert result["time"]           == stub_responce["time"]
    assert result["temperature_2m"] == stub_responce["temperature_2m"]

    # APIが正しいURLで呼び出されたことを確認
    selected_location = EXPECTED_COORDINATES_DICT[location]
    latitude = selected_location["latitude"]
    longitude= selected_location["longitude"]
    timezone = "Asia%2FTokyo"
    url = f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&timezone={timezone}&hourly=temperature_2m"
    requests.get.assert_called_once_with(
        url,
        headers={'user-agent' : 'curl'}
    )
