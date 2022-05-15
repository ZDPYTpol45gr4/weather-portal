from pprint import pprint


class Validator:
    @classmethod
    def validate_location(cls, data):
        if not data:
            raise ValueError('No data')

        for city in data:
            if not city['lat']:
                raise KeyError('There is no lat coords')
            if not city['lon']:
                raise KeyError('There is no lon coords')

    @classmethod
    def validate_weather(cls, data):
        if not data:
            raise ValueError('No data')

        keys = (
            'lat',
            'lon',
            'daily',
        )
        for key in keys:
            if key not in data.keys():
                raise KeyError('Data not found from api response')

        keys_temp = (
            'day',
            'min',
            'max',
        )
        keys_weather_info = (
            'icon',
            'main',
        )
        for day in data['daily']:
            for key in keys_temp:
                if key not in day['temp']:
                    raise KeyError('Data not found from api response')

            for key_2 in keys_weather_info:
                if key_2 not in day['weather'][0]:
                    raise KeyError('Data not found from api response')

