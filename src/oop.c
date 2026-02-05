#include "rebound.h"

DLLEXPORT void reb_set_heartbeat(struct reb_simulation* r, void (*hb)(struct reb_simulation*)) {
    r->heartbeat = hb;
}