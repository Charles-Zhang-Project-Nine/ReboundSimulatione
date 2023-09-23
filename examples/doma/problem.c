/**
 * A basic simulation setup for Doma system
 * 
 * We first create a REBOUND simulation, then we add  two particles and integrate the system for 10000 time units.
 */
#include "rebound.h"
#include <stdio.h>
#include <stdlib.h>

void simulate(struct reb_simulation* simulation, double timestep)
{
    // reb_integrate(simulation, timestep);
    reb_steps(simulation, timestep);
}

void print_coordinates(struct reb_simulation* simulation, int frame, const char* names[])
{
    for (int i = 0; i < simulation->N; i++){
        struct reb_particle p = simulation->particles[i];
        // Format: Particle Frame X Y Z
        printf("%s %i %f %f %f\n", names[i], frame, p.x, p.y, p.z);
    }
}
void print_orbits(struct reb_simulation* simulation, const char* names[])
{
    struct reb_particle primary = simulation->particles[0];
    struct reb_particle* particles = simulation->particles;

    for (int i = 1; i < simulation->N; i++){
        struct reb_particle p = particles[i];
        struct reb_orbit o = reb_tools_particle_to_orbit(simulation->G, p, primary);
        // Format: Particle Semi-major axis, elevation, true anomaly
        printf("%s %f %f %f\n", names[i], o.a, o.e, o.f);
    }
}

int main(int argc, char* argv[]) {
    // Initialize
    struct reb_simulation* r = reb_create_simulation();

    // Parameters
    int iterations = 500;
    double timestep = 10.;

    // Setup
    const char* names[] = { "Doma", "Ids", "Fukxim" };
    reb_add_fmt(r, "m", 1.0);                    // Doma
    reb_add_fmt(r, "m a e", 1e-3, 1.0, 0.1);     // Ids
    reb_add_fmt(r, "m a e", 2e-3, -1.4, 1.1);    // Fukxim 

    // Meta-data
    // Format: Key: Value
    printf("# Metadata\n");
    printf("@ Objects: ");
    unsigned long objects = sizeof(names) / sizeof(const char*);
    for(unsigned long i = 0; i < objects; i++)
        printf("%s ", names[i]);
    printf("\n@ Frames: %i\n", iterations);

    // Initial position
    printf("# Initial Positions: <Name> <Frame> <X> <Y> <Z>\n");
    print_coordinates(r, 0, names);    
    // Simulate
    for (int i = 0; i < iterations; i++)
    {
        printf("# Iteration %i\n", i);
        simulate(r, timestep);
        // Print time step (XYZ)
        print_coordinates(r, i + 1, names);
    }
    printf("# End of simulation\n");

    // Save
    reb_output_binary(r, "snapshot.bin");
    // Print coordinates around primary
    printf("\n# Orbits: <Name> <Semi-major axis> <elevation> <true anomaly> \n");
    print_orbits(r, names);

    // Release
    reb_free_simulation(r);
}