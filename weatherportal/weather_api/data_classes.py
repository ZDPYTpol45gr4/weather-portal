from dataclasses import dataclass
import datetime


@dataclass
class WeatherInfo:
    weather_data: list

    @classmethod
    def get_weather_list_from_dict(cls, data: dict, days_name):
        out_data = []

        for day in range(len(days_name)):
            out_data.append(WeatherInfoOneDay.get_day_from_dict(data['daily'][day], days_name[day]))

        return cls(
            weather_data=out_data
        )


@dataclass
class WeatherInfoOneDay:
    temp_avg: int
    temp_min: int
    temp_max: int
    description: str
    icon: str
    days_names: list[datetime]

    # TODO Make data ready to parse, dont parse it here
    @classmethod
    def get_day_from_dict(cls, data: dict, days_names: list[datetime]) -> "WeatherInfoOneDay":
        tmp_avg = int(data['temp']['day'])
        temp_min = int(data['temp']['min'])
        temp_max = int(data['temp']['max'])
        desc = data['weather'][0]['main']
        icon = f"http://openweathermap.org/img/wn/{data['weather'][0]['icon']}@2x.png"

        return cls(
            temp_avg=tmp_avg,
            temp_max=temp_max,
            temp_min=temp_min,
            description=desc,
            icon=icon,
            days_names=days_names
        )
