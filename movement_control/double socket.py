import asyncio

from connection import create_connection, send_command, close_connection, host, port
from movement_control.move_commands import stop_moving, normal, turn_left, left, straight_servo

connection1 = create_connection(host, port)

connection2 = create_connection(host, port)


async def turn_left_enough():
    left()
    await asyncio.sleep(5)
    stop_moving()


async def normalize():
    normal()
    straight_servo()
