/**
 * A basic simulation setup for Doma system
 * 
 * We first create a REBOUND simulation, then we add  two particles and integrate the system for 10000 time units.
 */
#include "rebound.h"
#include <stdio.h>
#include <stdlib.h>

int main(int argc, char* argv[]) {
    // Initialize
    struct reb_simulation* r = reb_create_simulation();

    // Setup
    reb_add_fmt(r, "m", 1.);                // Central object
    reb_add_fmt(r, "m a e", 1e-3, 1., 0.1); // Jupiter mass planet
    reb_add_fmt(r, "a e", 1.4, 0.1);        // Massless test particle 

    // Simulate
    reb_integrate(r,100.);

    // Print results
    for (int i=0; i<r->N; i++){
        struct reb_particle p = r->particles[i];
        printf("%f %f %f\n", p.x, p.y, p.z);
    }
    struct reb_particle primary = r->particles[0];
    for (int i=1; i<r->N; i++){
        struct reb_particle p = r->particles[i];
        struct reb_orbit o = reb_tools_particle_to_orbit(r->G, p, primary);
        printf("%f %f %f\n", o.a, o.e, o.f);
    }

    // Release
    reb_free_simulation(r);
}

