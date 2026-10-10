# Physics model

Each ball's mass is proportional to `radius²`, treating all balls as equal-density
discs. Every update applies gravity, exponential air damping, motion, and wall
constraints. Pair collisions first separate overlapping balls in proportion to
their masses, then apply a one-dimensional impulse along the collision normal.

`COLLISION_DAMPING` is the coefficient of restitution for ball-ball impacts;
`WALL_ELASTICITY` is the equivalent value for walls. The simulation is discrete,
so very fast small balls can still tunnel through other bodies.
