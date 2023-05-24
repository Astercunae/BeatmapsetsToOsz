import time
import os
import shutil


def measure_time(func):
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        result = end - start
        print(result)
        return result

    return wrapper


def compress_to_osz(songs_path, output_folder):
    beatmapsets = os.listdir(songs_path)

    for beatmap in beatmapsets:
        osz_file = os.path.join(output_folder, beatmap + '.osz')
        if os.path.exists(osz_file):
            continue

        archive_path = os.path.join(output_folder, beatmap)
        shutil.make_archive(archive_path, 'zip', os.path.join(songs_path, beatmap)).replace(".zip", ".osz")
        os.rename(archive_path + ".zip", osz_file)
