
    // weather_advisor_test.cpp
    #include "gtest/gtest.h"
    #include "weather_advisor.h"

    TEST(WeatherAdvisorTest, BadWeather) {
        WeatherAdvisor advisor(-5, 95, 900);
        EXPECT_EQ(advisor.shouldGoOutside(), "It's not recommended to go outside due to bad weather conditions.");
    }

    TEST(WeatherAdvisorTest, UncomfortableWeather) {
        WeatherAdvisor advisor(25, 85, 1010);
        EXPECT_EQ(advisor.shouldGoOutside(), "You can go outside, but it might be uncomfortable.");
    }

    TEST(WeatherAdvisorTest, GoodWeather) {
        WeatherAdvisor advisor(20, 60, 1020);
        EXPECT_EQ(advisor.shouldGoOutside(), "It's a great day to go outside!");
    }

    TEST(WeatherAdvisorTest, ExtremeTemperature) {
        WeatherAdvisor advisor(-20, 50, 1015);
        EXPECT_EQ(advisor.shouldGoOutside(), "It's not recommended to go outside due to bad weather conditions.");
    }

    TEST(WeatherAdvisorTest, ExtremeHumidity) {
        WeatherAdvisor advisor(20, 95, 1015);
        EXPECT_EQ(advisor.shouldGoOutside(), "It's not recommended to go outside due to bad weather conditions.");
    }

    TEST(WeatherAdvisorTest, ExtremeBarometer) {
        WeatherAdvisor advisor(20, 60, 900);
        EXPECT_EQ(advisor.shouldGoOutside(), "It's not recommended to go outside due to bad weather conditions.");
    }