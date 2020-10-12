/*
 * Statistics counters - first the good, then the bad
 * These get reset every hour if sysstats is enabled.
 */
#include "ntp_types.h"

extern uptime_t	use_stattime;		/* time since usestats reset */

struct statistics_counters {
	uptime_t	sys_stattime;		/* time since sysstats reset */
	uint64_t	sys_received;		/* packets received */
	uint64_t	sys_processed;		/* packets for this host */
	uint64_t	sys_restricted;		/* restricted packets */
	uint64_t	sys_newversion;		/* current version  */
	uint64_t	sys_oldversion;		/* old version */
	uint64_t	sys_badlength;		/* bad length or format */
	uint64_t	sys_badauth;		/* bad authentication */
	uint64_t	sys_declined;		/* declined */
	uint64_t	sys_limitrejected;	/* rate exceeded */
	uint64_t	sys_kodsent;		/* KoD sent */
};
extern volatile struct statistics_counters stat_proto_hourago, stat_proto_total;

#define stat_sys_form(member)\
extern uint64_t stat_##member(void);\
extern uint64_t stat_total_##member(void)

stat_sys_form(received);
stat_sys_form(processed);
stat_sys_form(restricted);
stat_sys_form(newversion);
stat_sys_form(oldversion);
stat_sys_form(badlength);
stat_sys_form(badauth);
stat_sys_form(declined);
stat_sys_form(limitrejected);
stat_sys_form(kodsent);

#undef stat_sys_form

extern uptime_t stat_total_stattime(void);
extern uptime_t stat_stattime(void);

extern void increment_restricted(void);
extern uptime_t stat_use_stattime(void);
extern void set_use_stattime(uptime_t stattime);
