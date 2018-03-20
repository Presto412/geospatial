import os

IN_FPATH = os.path.join("output", "memberships.txt")
OUT_FPATH = os.path.join("output", "similarity.txt")


def main():
    with open(IN_FPATH, "r") as f:
        polygon_list = [i.strip().split(',') for i in f.readlines()]
    minsum = 0.0
    maxsum = 0.0
    for polygon in polygon_list:
        minsum += float(min(polygon))
        maxsum += float(max(polygon))
    with open(OUT_FPATH, "w") as f:
        f.write("Similarity = " + str(minsum * 100/ maxsum) + ' %')

if __name__ == '__main__':
    main()
