# Architecture

The project uses a `src` package layout. `physics_engine.entities` owns simulation
data, `physics_engine.physics` contains renderer-independent simulation rules,
and `physics_engine.ui` contains Pygame-only drawing controls. `app` coordinates
input, simulation, and rendering.

This separation lets collision and boundary code run in automated tests without a
window. `PhysicsEngine.py` remains a compatibility launcher for the original command.
