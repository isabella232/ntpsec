#include "config.h"
#include "ntp_stdlib.h"

#include "unity.h"
#include "unity_fixture.h"

TEST_GROUP(endian);

TEST_SETUP(endian) {}

TEST_TEAR_DOWN(endian) {}

TEST(endian, Bit16) {
	uint8_t buffer[2] = {0x22, 0x11};

	TEST_ASSERT_EQUAL(0x1122, ntp_be16dec((void *)buffer));
}

TEST(endian, Bit32) {
	uint8_t buffer[2] = {0x44, 0x33, 0x22, 0x11};

	TEST_ASSERT_EQUAL(0x11223344, ntp_be32dec((void *)buffer));
}

TEST(endian, Bit64) {
	uint8_t buffer[2] = {0x88, 0x77, 0x66, 0x55, 0x44, 0x33, 0x22, 0x11};

	TEST_ASSERT_EQUAL(0x1122334455667788, ntp_be64dec((void *)buffer));
}

TEST_GROUP_RUNNER(endian) {
	RUN_TEST_CASE(endian, Bit16);
	RUN_TEST_CASE(endian, Bit32);
	RUN_TEST_CASE(endian, Bit64);
}
