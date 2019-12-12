#include <stdbool.h>

void ntpc_setprogname(char*);
char *ntpc_prettydate(char*);
double ntpc_lfptofloat(char*);
int ntpc_set_tod(int, int);
bool ntpc_adj_systime(double);
bool ntpc_step_systime(double);
