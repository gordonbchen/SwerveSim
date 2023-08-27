"""A swerve drive simulator."""


from argparse import ArgumentParser

from typing import List, Callable

import matplotlib.pyplot as plt
plt.style.use("bmh")


def optimizer(raw_target_angle: int, raw_curr_angle: int) -> int:
    """A function that should optimize the steer rotation."""
    target_angle = bound_angle(raw_target_angle)
    curr_angle = bound_angle(raw_curr_angle)

    delta = target_angle - curr_angle
    if abs(delta) > 180:
        # Case: delta(target=179, curr=-179) = -2.
        delta -= 360 * sign(delta)

    if abs(delta) > 90:
        # Case: delta(target=135, curr=0) = -45.
        delta -= 180 * sign(delta)

    target_angle = raw_curr_angle + delta
    return target_angle


def sign(x: int) -> int:
    """Return the sign of x (-1 or 1)."""
    if x < 0:
        return -1
    else:
        return 1


def bound_angle(angle: int) -> int:
    """Bound an angle on (-180, 180)."""
    # Remove excess rotations.
    angle %= 360

    # Force positive.
    if angle < 0:
        angle += 360

    # Bound to (-180, 180).
    if angle > 180:
        angle -= 360

    return angle


def show_optimized_angles(
    target_angle: int,
    curr_angles: List[int],
    optimizer: Callable[[int, int], int]
) -> None:
    """Show optimizer effects."""
    fig, ax = plt.subplots(figsize=(10, 5))

    optimized_target_angles = [
        optimizer(target_angle, curr_angle)
        for curr_angle in curr_angles
    ]

    ax.plot(curr_angles, optimized_target_angles)
    ax.set(
        title=f"Target angle: {target_angle}",

        xlabel="Curr angle",
        ylabel="Optimized angle",

        xticks=get_ticks(curr_angles, step=45),
        yticks=get_ticks(optimized_target_angles, step=180)
    )

    plt.show()


def get_ticks(data: List[int], step: int) -> List[int]:
    """Return a list of ticks that cover the range of data."""
    ticks = list(range(min(data), max(data) + 1, step))
    return ticks


if __name__ == "__main__":
    # Parse args.
    parser = ArgumentParser()
    parser.add_argument("-t", "--target", type=int, default=0)

    args = parser.parse_args()

    # Show optimized angles.
    curr_angles = [i for i in range(-540, 540 + 1)]

    show_optimized_angles(
        args.target,
        curr_angles,
        optimizer
    )
