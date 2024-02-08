// weather_advisor.h
#ifndef WEATHER_ADVISOR_H
#define WEATHER_ADVISOR_H

#include <string>

class WeatherAdvisor {
public:
    WeatherAdvisor(float temperature, float humidity, float barometer);
    std::string shouldGoOutside();

private:
    float temperature_;
    float humidity_;
    float barometer_;

    bool isBadWeather();
    bool isUncomfortable();
};

#endif // WEATHER_ADVISOR_H