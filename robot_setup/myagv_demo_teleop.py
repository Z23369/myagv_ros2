#!/usr/bin/env python3
import sys
import time
import tty
import termios
import select
import rclpy
from geometry_msgs.msg import Twist

CONTROLS = {
    "w": (0.10, 0.0, 0.0),
    "s": (-0.10, 0.0, 0.0),
    "a": (0.0, 0.0, 0.35),
    "d": (0.0, 0.0, -0.35),
    "q": (0.0, 0.08, 0.0),
    "e": (0.0, -0.08, 0.0),
}

def main():
    if not sys.stdin.isatty():
        raise SystemExit("Run this in an interactive terminal.")
    rclpy.init()
    node = rclpy.create_node("myagv_demo_controller")
    pub = node.create_publisher(Twist, "/cmd_vel", 10)
    fd = sys.stdin.fileno()
    original = termios.tcgetattr(fd)

    def publish(speeds):
        msg = Twist()
        msg.linear.x, msg.linear.y, msg.angular.z = speeds
        pub.publish(msg)

    def stop():
        for _ in range(6):
            publish((0.0, 0.0, 0.0))
            time.sleep(0.05)

    try:
        tty.setcbreak(fd)
        print("myAGV demo: W/S forward/back | A/D turn | Q/E strafe")
        print("Hold a key to extend movement; X/SPACE stops; X/SPACE stop; Z exit", flush=True)
        while rclpy.ok():
            key = sys.stdin.read(1).lower()
            if key == "z":
                break
            if key in ("x", " "):
                stop()
                continue
            if key not in CONTROLS:
                continue
            until = time.monotonic() + 0.9
            exit_requested = False
            while time.monotonic() < until:
                publish(CONTROLS[key])
                if select.select([sys.stdin], [], [], 0)[0]:
                    next_key = sys.stdin.read(1).lower()
                    if next_key == key:
                        until = time.monotonic() + 0.4
                    elif next_key in ("x", " ", "z"):
                        exit_requested = next_key == "z"
                        break
                time.sleep(0.08)
            stop()
            if exit_requested:
                break
    except KeyboardInterrupt:
        pass
    finally:
        try:
            stop()
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, original)
            node.destroy_node()
            rclpy.shutdown()

if __name__ == "__main__":
    main()
