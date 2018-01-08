from itertools import combinations


def read_roster():
    pass


def find_rainbow_teams():
    """
    Rainbow teams are teams that contain powers across all the colors.
    :return:
    """

    cs = [{'name': 'S', 'G': 12, 'B': 11, 'Y': 1},
          {'name': 'I', 'R': 11, 'U': 10, 'Y': 1},
          {'name': 'B', 'P': 10, 'U': 9},
          {'name': 'V', 'B': 9, 'P': 8},
          {'name': 'P', 'R': 8, 'U': 7, 'P': 1},
          {'name': 'H', 'P': 7, 'R': 6},
          {'name': 'J', 'G': 6, 'R': 5}]

    i = combinations(cs, 3)
    gt_list = []
    for x in i:
        jc = {'B': 0, 'U': 0, 'R': 0, 'Y': 0, 'G': 0, 'P': 0}
        for item in x:
            for key, value in item.items():
                if key != 'name':
                    jc[key] += value
        # print(x)
        if all(value > 0 for value in jc.values()):
            # print(sum(jc.values()))
            new_c_list = [u for u in x]
            # print(new_c_list)
            # new_c_list.append({'name': 'sum', 'value': sum(jc.values())})
            gt_list.append(new_c_list)

    # print(gt_list)
    for gt in gt_list:
        jc = {'B': 0, 'U': 0, 'R': 0, 'Y': 0, 'G': 0, 'P': 0}
        for c in gt:
            for key in c.keys():
                if key != 'name' and c[key] > jc[key]:
                    jc[key] = c[key]
        gt.append(sum(jc.values()))

        # print(gt.p)
        # print([x.get('name') for x in gt])
        # print(jc)
    sorted(gt_list, key=lambda a: int(a[3]))
    for gt in gt_list:
        print(gt)
