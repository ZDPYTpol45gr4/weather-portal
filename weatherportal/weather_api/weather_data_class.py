from dataclasses import dataclass


@dataclass
class WeatherInfo:
    data: list

    @classmethod
    def get_dict_for_daily(cls, data: dict, days_name):
        days_temp = [val['temp'] for val in data['daily']]
        desc = [val['weather'][0]['main'] for val in data['daily']]
        icons = [val['weather'][0]['icon'] for val in data['daily']]
        # print(days_temp)
        # for day in days_temp:
        #     for key, val in day.keys():
        #         day[key] = int(val)

        for num, val in enumerate(days_temp):
            val['day_name'] = days_name[num]
            val['icon'] = f"http://openweathermap.org/img/wn/{icons[num]}@2x.png"
            val['desc'] = desc[num]

        return cls(
            data=days_temp
        )
