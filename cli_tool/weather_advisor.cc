// weather_advisor.cpp
#include <iostream>
#include <string>

class WeatherAdvisor {
public:
    WeatherAdvisor(float temperature, float humidity, float barometer)
        : temperature_(temperature), humidity_(humidity), barometer_(barometer) {}

    std::string shouldGoOutside() {
        if (isBadWeather()) {
            return "It's not recommended to go outside due to bad weather conditions.";
        }
        if (isUncomfortable()) {
            return "You can go outside, but it might be uncomfortable.";
        }
        return "It's a great day to go outside!";
    }

private:
    float temperature_;
    float humidity_;
    float barometer_;

    bool isBadWeather() {
        // Example condition for bad weather
        return temperature_ < 0 || temperature_ > 35 || humidity_ > 90 || barometer_ < 1000;
    }

    bool isUncomfortable() {
        // Example condition for uncomfortable weather
        return temperature_ < 10 || temperature_ > 30 || humidity_ > 80;
    }
};

int main() {
    float temperature, humidity, barometer;
    std::cout << "Enter temperature (in Celsius), humidity (in %), and barometer (in hPa): ";
    std::cin >> temperature >> humidity >> barometer;

    WeatherAdvisor advisor(temperature, humidity, barometer);
    std::cout << advisor.shouldGoOutside() << std::endl;

    return 0;
}
