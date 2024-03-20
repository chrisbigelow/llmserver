
cc_library(
    name = "weather_advisor",
    srcs = ["weather_advisor.cc"],
    hdrs = ["weather_advisor.h"],
)


cc_test(
    name = "weather_advisor_test",
    size = "small",
    srcs = ["weather_advisor_test_generated.cc"],
    deps = [
        ":weather_advisor",
        "@com_google_googletest//:gtest_main",
    ],
)
