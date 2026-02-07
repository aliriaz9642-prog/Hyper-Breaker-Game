def get_level_data(level):
    return {
        "bricks": 5 + level * 2,
        "ball_speed": 4 + level * 0.1,
        "powerups": max(1, 5 - level // 10)
    }
