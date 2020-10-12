#include "ntpd.h"
#include "ntp_stats.h"

uptime_t	use_stattime;		/* time since usestats reset */


uptime_t stat_stattime(void)
{
  return current_time - stat_proto_hourago.sys_stattime;
}

uptime_t stat_total_stattime(void)
{
  return current_time - stat_proto_total.sys_stattime;
}

#define stat_sys_dumps(member)\
uint64_t stat_##member(void) {\
  return stat_proto_total.sys_##member - stat_proto_hourago.sys_##member;\
}\
uint64_t stat_total_##member(void) {\
  return stat_proto_total.sys_##member;\
}

stat_sys_dumps(received)
stat_sys_dumps(processed)
stat_sys_dumps(restricted)
stat_sys_dumps(newversion)
stat_sys_dumps(oldversion)
stat_sys_dumps(badlength)
stat_sys_dumps(badauth)
stat_sys_dumps(declined)
stat_sys_dumps(limitrejected)
stat_sys_dumps(kodsent)

#undef stat_sys_dumps

void increment_restricted(void)
{
  stat_proto_total.sys_restricted++;
}

uptime_t stat_use_stattime(void)
{
  return current_time - use_stattime;
}

void set_use_stattime(uptime_t stattime) {
  use_stattime = stattime;
}
