import os


def get_phrases():
    path = "./txt_files"
    files = os.listdir(path=path)

    result = []

    for file in files:
        try:
            with open(path + "/" + file, "r") as file:
                data = list(map(lambda string: string.strip().lower() if string.strip() != "" else None, file.readlines()))
                result.append(data)

        finally:
            file.close()

    return result


res = get_phrases()
print(res)
