from .exceptions import ValidationWeatherError


class Validator:
    @classmethod
    def validate_location(cls, data):
        if not data:
            raise ValueError('No data from location api')

        for city in data:
            if not city['lat']:
                raise ValidationWeatherError('There is no lat coords')
            if not city['lon']:
                raise ValidationWeatherError('There is no lon coords')

    @classmethod
    def validate_weather(cls, data):
        if not data:
            raise ValueError('No data from weather api')

        keys = (
            'lat',
            'lon',
            'daily',
        )
        for key in keys:
            if key not in data.keys():
                raise ValidationWeatherError('Data not found from api response')

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
                    raise ValidationWeatherError('Data not found from api response')

            for key_2 in keys_weather_info:
                if key_2 not in day['weather'][0]:
                    raise ValidationWeatherError('Data not found from api response')
