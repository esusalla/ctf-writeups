import itertools
import multiprocessing
import sys

target = "ElxFr9)F"
a = 1103515245
c = 12345
i32_limit = 256**4//2


def get_possible_seeds():
    mask = 0x7fff
    limit = 0xffff + 1

    seed = ord("E") - 0x21
    seeds = []

    while seed < mask:
        seeds.append(range(seed << 16, (seed << 16) + limit))
        seeds.append(range(-(-seed & mask) << 16, (-(-seed & mask) << 16) - limit))
        seed += 0x5e
    
    return itertools.chain(*seeds)


def generate_password(seed):
    pwd = []
    for _ in range(8):
        pwd.append(chr((((seed >> 16) & 0x7fff) % 0x5e) + 0x21))
        seed = ((seed * a) % i32_limit) + c

    return "".join(pwd)


def check_seed(seed):
    pwd = generate_password(seed)
    if pwd == target:
        print(seed)
        sys.exit()


if __name__ == "__main__":
    seeds = get_possible_seeds()

    with multiprocessing.Pool(16) as pool:
        pool.map(check_seed, seeds)
        pool.join()
        pool.close()
