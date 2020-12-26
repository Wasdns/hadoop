#!/usr/bin/python

def read_map():
    map_results = []
    with open("map.txt", "r") as f:
        for line in f:
            if not f: break
            srcip, dstip, proto, srcport, dstport = line.split()
            map_results.append([srcip, dstip, proto, srcport, dstport])
    return map_results

def main():
    map_results = read_map()
    reduce_results = {}
    for item in map_results:
        item_tpl = tuple(item)
        if item_tpl in reduce_results:
            reduce_results[item_tpl] = reduce_results[item_tpl]+1
        else:
            reduce_results[tuple(item)] = 1
    print "===== Reducer Results ====="
    for item in reduce_results:
        print "Flow ID:", item, ", Number:", reduce_results[item]
    print "===== END ====="

if __name__ == '__main__':
    main()
