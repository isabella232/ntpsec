#include "config.h"
#include "ntp_stdlib.h"
#include "ntp_fp.h"

#include "unity.h"
#include "unity_fixture.h"

TEST_GROUP(dolfptoa);

TEST_SETUP(dolfptoa) {}

TEST_TEAR_DOWN(dolfptoa) {}


TEST(dolfptoa, DoLfpToA) {
	l_fp in;

	in = lfpinit(0, 0);
	TEST_ASSERT_EQUAL_STRING("0.0", dolfptoa(in, false, 0, false));
	TEST_ASSERT_EQUAL_STRING("0.0", dolfptoa(in, true, 0, false));
	TEST_ASSERT_EQUAL_STRING("0.0", dolfptoa(in, false, 0, true));
	TEST_ASSERT_EQUAL_STRING("0.0", dolfptoa(in, true, 0, true));

	TEST_ASSERT_EQUAL(1, 2);
}

//TEST(dolfptoa, MfpToA) {
//}

//TEST(dolfptoa, MfpToMs) {
//}

TEST_GROUP_RUNNER(dolfptoa) {
	RUN_TEST_CASE(dolfptoa, DoLfpToA);
	//RUN_TEST_CASE(dolfptoa, MfpToA);
	//RUN_TEST_CASE(dolfptoa, MfpToMs);
}
