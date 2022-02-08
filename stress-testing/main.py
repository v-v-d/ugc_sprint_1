from model import Data


def collect_data():
    data = []
    data_count = 1
    post_id = 1
    user_id = 1
    timestamp = 100
    move_id = 1
    while True:
        data.append(
            Data(id=post_id, user_id=user_id, timestamp=timestamp, move_id=move_id)
        )
        data_count += 1
        post_id += 1
        user_id += 1
        timestamp += 1
        move_id += 1
        if data_count == 10000000:
            break
    return data


if __name__ == "__main__":
    data = collect_data()

