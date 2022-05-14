from dataclasses import dataclass


@dataclass
class WeatherInfo:
    weather_data: list

    @classmethod
    def get_weather_list_from_dict(cls, data: dict, days_name):
        out_data = []

        for day in range(len(days_name)):
            print(day)
            out_data.append(WeatherInfoOneDay.get_day_from_dict(data['daily'][day], days_name[day]))

        return cls(
            weather_data=out_data
        )


@dataclass
class WeatherInfoOneDay:
    temp: int
    temp_min: int
    temp_max: int
    desc: str
    icon: str
    day_name: str

    @classmethod
    def get_day_from_dict(cls, data: dict, day_name: str):
        tmp = int(data['temp']['day'])
        temp_min = int(data['temp']['min'])
        temp_max = int(data['temp']['max'])
        desc = data['weather'][0]['main']
        icon = f"http://openweathermap.org/img/wn/{data['weather'][0]['icon']}@2x.png"

        return cls(
            temp=tmp,
            temp_max=temp_max,
            temp_min=temp_min,
            desc=desc,
            icon=icon,
            day_name=day_name
        )
