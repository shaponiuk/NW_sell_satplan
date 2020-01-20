from pysat.solvers import Glucose3

# 3 dziedziny

counter = 1
name_dict = {}
var_dict = {}


def check_var_exists(var_name):
    global var_dict
    if var_name in var_dict:
        return True
    else:
        return False


def register_var_if_unregistered(name):
    global counter, var_dict, name_dict
    if check_var_exists(name):
        return var_dict[name]
    else:
        var_dict[name] = counter
        name_dict[counter] = name
        counter += 1
        return counter - 1


def add_sold_clause(g):
    g.add_clause([register_var_if_unregistered("sold")])


def add_rules_for_sold(g, desiredTimestamp):
    global var_dict

    if desiredTimestamp == 1:
        g.add_clause([-register_var_if_unregistered("sold")])

    clause_list = [-var_dict["sold"]]

    for i in range(desiredTimestamp):
        if i == 0:
            continue

        clause_list.append(register_var_if_unregistered("weak marketing, service market, timestamp %d" % (i)))
        clause_list.append(register_var_if_unregistered("strong marketing, service market, timestamp %d" % (i)))
        clause_list.append(register_var_if_unregistered("weak traders, product market, timestamp %d" % (i)))
        clause_list.append(register_var_if_unregistered("strong traders, product market, timestamp %d" % (i)))

        for j in range(3):
            clause_list.append(register_var_if_unregistered(
                "strong marketing, product market, marketing area %d, market area %d, timestamp %d" % (j, j, i)))
            clause_list.append(register_var_if_unregistered(
                "strong traders, service market, trading area %d, market area %d, timestamp %d" % (j, j, i)))

    g.add_clause(clause_list)


def add_rules_for_weak_marketing_tuples(g, timestamp):
    global name_dict, var_dict, counter

    g.add_clause([-register_var_if_unregistered("weak marketing, service market, timestamp 1")])

    for i in range(timestamp):
        if i == 0:
            continue

        for j in range(i + 1):
            if j == 0:
                continue
            g.add_clause([-var_dict["weak marketing, service market, timestamp %d" % (i)], counter,
                          register_var_if_unregistered("weak marketing, timestamp %d" % (j))])
            g.add_clause([-var_dict["weak marketing, service market, timestamp %d" % (i)], counter,
                          register_var_if_unregistered("service market, timestamp %d" % (j))])


def add_rules_for_strong_marketing_tuples(g, timestamp):
    g.add_clause([-register_var_if_unregistered("strong marketing, service market, timestamp 1")])

    for k in range(3):
        g.add_clause([-register_var_if_unregistered(
            "strong marketing, product market, marketing area %d, market area %d, timestamp 1" % (k, k))])

    for i in range(timestamp):
        if i == 0:
            continue

        clause_list_1 = [-register_var_if_unregistered("strong marketing, service market, timestamp %d" % i)]
        clause_list_2 = [-register_var_if_unregistered("strong marketing, service market, timestamp %d" % i)]

        clause_list_3 = [[],[],[]]
        clause_list_4 = [[],[],[]]
        clause_list_5 = [[],[],[]]
        clause_list_6 = [[],[],[]]
        for k in range(3):
            clause_list_3[k].append(-register_var_if_unregistered(
                    "strong marketing, product market, marketing area %d, market area %d, timestamp %d" % (k, k, i)))
            clause_list_4[k].append(-register_var_if_unregistered(
                    "strong marketing, product market, marketing area %d, market area %d, timestamp %d" % (k, k, i)))
            clause_list_5[k].append(-register_var_if_unregistered(
                    "strong marketing, product market, marketing area %d, market area %d, timestamp %d" % (k, k, i)))
            clause_list_6[k].append(-register_var_if_unregistered(
                    "strong marketing, product market, marketing area %d, market area %d, timestamp %d" % (k, k, i)))

        for j in range(i + 1):
            if j == 0:
                continue

            clause_list_1.append(register_var_if_unregistered("strong marketing, timestamp %d" % j))
            clause_list_2.append(register_var_if_unregistered("service market, timestamp %d" % j))

            for k in range(3):
                clause_list_3[k].append(register_var_if_unregistered("strong marketing, timestamp %d" % (j)))
                clause_list_4[k].append(register_var_if_unregistered("product market, timestamp %d" % (j)))
                clause_list_5[k].append(register_var_if_unregistered("marketing area %d, timestamp %d" % (k, j)))
                clause_list_6[k].append(register_var_if_unregistered("market area %d, timestamp %d" % (k, j)))

        g.add_clause(clause_list_1)
        g.add_clause(clause_list_2)

        for k in range(3):
            g.add_clause(clause_list_3[k])
            g.add_clause(clause_list_4[k])
            g.add_clause(clause_list_5[k])
            g.add_clause(clause_list_6[k])


def add_rules_for_marketing_tuples(g, timestamp):
    add_rules_for_weak_marketing_tuples(g, timestamp)
    add_rules_for_strong_marketing_tuples(g, timestamp)


def add_rules_for_weak_traders_tuples(g, timestamp):
    g.add_clause([-register_var_if_unregistered("weak traders, product market, timestamp 1")])

    for i in range(timestamp):
        if i == 0:
            continue

        for j in range(i + 1):
            if j == 0:
                continue

            g.add_clause([-register_var_if_unregistered("weak traders, product market, timestamp %d" % i),
                          register_var_if_unregistered("weak traders, timestamp %d" % j)])
            g.add_clause([-register_var_if_unregistered("weak traders, product market, timestamp %d" % i),
                          register_var_if_unregistered("product market, timestamp %d" % (j))])


def add_rules_for_strong_traders_tuples(g, timestamp):
    g.add_clause([-register_var_if_unregistered("strong traders, product market, timestamp 1")])

    for k in range(3):
        g.add_clause([-register_var_if_unregistered(
            "strong traders, service market, trading area %d, market area %d, timestamp 1" % (k, k))])

    for i in range(timestamp):
        if i == 0:
            continue

        clause_list_1 = [-register_var_if_unregistered("strong traders, product market, timestamp %d" % i)]
        clause_list_2 = [-register_var_if_unregistered("strong traders, product market, timestamp %d" % i)]

        clause_list_3 = [[], [], []]
        clause_list_4 = [[], [], []]
        clause_list_5 = [[], [], []]
        clause_list_6 = [[], [], []]
        for k in range(3):
            clause_list_3[k].append(-register_var_if_unregistered(
                "strong traders, service market, trading area %d, market area %d, timestamp %d" % (k, k, i)))
            clause_list_4[k].append(-register_var_if_unregistered(
                "strong traders, service market, trading area %d, market area %d, timestamp %d" % (k, k, i)))
            clause_list_5[k].append(-register_var_if_unregistered(
                "strong traders, service market, trading area %d, market area %d, timestamp %d" % (k, k, i)))
            clause_list_6[k].append(-register_var_if_unregistered(
                "strong traders, service market, trading area %d, market area %d, timestamp %d" % (k, k, i)))

        for j in range(i + 1):
            if j == 0:
                continue

            clause_list_1.append(register_var_if_unregistered("strong traders, timestamp %d" % j))
            clause_list_2.append(register_var_if_unregistered("product market, timestamp %d" % j))

            for k in range(3):
                clause_list_3[k].append(register_var_if_unregistered("strong traders, timestamp %d" % (j)))
                clause_list_4[k].append(register_var_if_unregistered("service market, timestamp %d" % (j)))
                clause_list_5[k].append(register_var_if_unregistered("trading area %d, timestamp %d" % (k, j)))
                clause_list_6[k].append(register_var_if_unregistered("market area %d, timestamp %d" % (k, j)))

        g.add_clause(clause_list_1)
        g.add_clause(clause_list_2)

        for k in range(3):
            g.add_clause(clause_list_3[k])
            g.add_clause(clause_list_4[k])
            g.add_clause(clause_list_5[k])
            g.add_clause(clause_list_6[k])


def add_rules_for_traders_tuples(g, timestamp):
    add_rules_for_weak_traders_tuples(g, timestamp)
    add_rules_for_strong_traders_tuples(g, timestamp)


def add_rules_for_marketing_and_traders_tuples(g, timestamp):
    add_rules_for_marketing_tuples(g, timestamp)
    add_rules_for_traders_tuples(g, timestamp)


def add_rules_for_weak_marketing(g, timestamp):
    g.add_clause([-register_var_if_unregistered("weak marketing, timestamp 1")])

    for i in range(timestamp):
        if i == 0:
            continue

        clause_list = [-register_var_if_unregistered("weak marketing, timestamp %d" % i)]

        for j in range(i):
            if j == 0:
                continue

            clause_list.append(register_var_if_unregistered("analysed, able to do weak marketing, timestamp %d" % j))

        g.add_clause(clause_list)


def add_rules_for_strong_marketing(g, timestamp):
    g.add_clause([-register_var_if_unregistered("strong marketing, timestamp 1")])

    if timestamp == 1:
        g.add_clause([-register_var_if_unregistered("strong marketing, timestamp 1")])

    for i in range(timestamp):
        if i == 0:
            continue

        clause_list = [-register_var_if_unregistered("strong marketing, timestamp %d" % (i))]

        for j in range(i):
            if j == 0:
                continue

            clause_list.append(register_var_if_unregistered("analysed, able to do strong marketing, timestamp %d" % j))

        g.add_clause(clause_list)


def add_rules_for_marketing_area(g, timestamp):
    g.add_clause([-register_var_if_unregistered("marketing area, timestamp 1")])

    for i in range(timestamp):
        if i == 0:
            continue

        clause_list = [-register_var_if_unregistered("marketing area, timestamp %d" % i)]

        for j in range(i):
            if j == 0:
                continue

            clause_list.append(register_var_if_unregistered("chosen service area, timestamp %d" % j))
            clause_list.append(register_var_if_unregistered("chosen product area, timestamp %d" % j))

        g.add_clause(clause_list)


def add_rules_for_marketing(g, timestamp):
    add_rules_for_weak_marketing(g, timestamp)
    add_rules_for_strong_marketing(g, timestamp)
    add_rules_for_marketing_area(g, timestamp)


def add_rules_for_weak_traders(g, timestamp):
    g.add_clause([-register_var_if_unregistered("weak traders, timestamp 1")])

    for i in range(timestamp):
        if i == 0:
            continue

        clause_list = [-register_var_if_unregistered("weak traders, timestamp %d" % (i))]

        for j in range(i):
            if j == 0:
                continue

            clause_list.append(register_var_if_unregistered("analysed, able to do weak traders, timestamp %d" % j))

        g.add_clause(clause_list)


def add_rules_for_strong_traders(g, timestamp):
    g.add_clause([-register_var_if_unregistered("strong traders, timestamp 1")])

    for i in range(timestamp):
        if i == 0:
            continue

        clause_list = [-register_var_if_unregistered("strong traders, timestamp %d" % (i))]

        for j in range(i):
            if j == 0:
                continue

            clause_list.append(register_var_if_unregistered("analysed, able to do strong traders, timestamp %d" % j))

        g.add_clause(clause_list)


def add_rules_for_trading_area(g, timestamp):
    for i in range(timestamp):
        if i == 0:
            continue

        clause_list = [-register_var_if_unregistered("marketing area, timestamp %d" % i)]

        for j in range(i):
            if j == 0:
                continue

            clause_list.append(register_var_if_unregistered("chosen service area, timestamp %d" % j))
            clause_list.append(register_var_if_unregistered("chosen product area, timestamp %d" % j))

        g.add_clause(clause_list)


def add_rules_for_traders(g, timestamp):
    add_rules_for_weak_traders(g, timestamp)
    add_rules_for_strong_traders(g, timestamp)
    add_rules_for_trading_area(g, timestamp)


def add_rules_for_marketing_and_traders(g, timestamp):
    add_rules_for_marketing(g, timestamp)
    add_rules_for_traders(g, timestamp)


def add_rules_for_self_marketing_capability_analysis(g, timestamp):
    g.add_clause([-register_var_if_unregistered("analysed, able to do weak marketing, timestamp 1")])
    g.add_clause([-register_var_if_unregistered("analysed, able to do strong marketing, timestamp 1")])

    for i in range(timestamp):
        if i == 0:
            continue

        g.add_clause([-register_var_if_unregistered("analysed, able to do weak marketing, timestamp %d" % i),
                      register_var_if_unregistered("able to do weak marketing")])
        g.add_clause([-register_var_if_unregistered("analysed, able to do strong marketing, timestamp %d" % i),
                      register_var_if_unregistered("able to do strong marketing")])


def add_rules_for_self_traders_capability_analysis(g, timestamp):
    g.add_clause([-register_var_if_unregistered("analysed, able to do weak traders, timestamp 1")])
    g.add_clause([-register_var_if_unregistered("analysed, able to do strong traders, timestamp 1")])

    for i in range(timestamp):
        if i == 0:
            continue

        g.add_clause([-register_var_if_unregistered("analysed, able to do weak traders, timestamp %d" % i),
                      register_var_if_unregistered("able to do weak traders")])
        g.add_clause([-register_var_if_unregistered("analysed, able to do strong traders, timestamp %d" % i),
                      register_var_if_unregistered("able to do strong traders")])


def add_rules_for_self_marketing_traders_capability_analysis(g, timestamp):
    add_rules_for_self_marketing_capability_analysis(g, timestamp)
    add_rules_for_self_traders_capability_analysis(g, timestamp)


def add_rules_for_market_analysis(g, timestamp):
    for k in range(3):
        g.add_clause([-register_var_if_unregistered("market area %d, timestamp 1")])
    g.add_clause([-register_var_if_unregistered("service market, timestamp 1")])
    g.add_clause([-register_var_if_unregistered("product market, timestamp 1")])

    for i in range(timestamp):
        if i == 0:
            continue

        for k in range(3):
            g.add_clause([-register_var_if_unregistered("market area %d, timestamp %d" %(k, i)),
            register_var_if_unregistered("market area %d, unanalysed" % k)])

        g.add_clause([-register_var_if_unregistered("service market, timestamp %d" % i),
                      register_var_if_unregistered("service market, unanalysed")])
        g.add_clause([-register_var_if_unregistered("product market, timestamp %d" % i),
                      register_var_if_unregistered("product market, unanalysed")])


def add_rules_for_product_service_creation(g, timestamp):
    for i in range(timestamp):
        if i == 0:
            continue

        clause_list = []
        for k in range(3):
            clause_list.append("product area %d, timestamp %d" %(k, i))
            clause_list.append("service area %d, timestamp %d" %(k, i))

        clause_list = [ register_var_if_unregistered(name) for name in clause_list ]

        g.add_clause(clause_list)


tests = [[(1, "able to do weak marketing")],
         [(1, "able to do weak marketing"),
          (0, "able to do strong marketing"),
          (1, "product market, unanalysed"),
          (0, "service market, unanalysed"),
          (0, "able to do weak traders"),
          (0, "able to do strong traders")],
         [(1, "able to do strong marketing"),
          (0, "able to do weak marketing"),
          (1, "product market, unanalysed"),
          (0, "service market, unanalysed"),
          (0, "able to do weak traders"),
          (0, "able to do strong traders")]]


count = 1
for test in tests:
    for idx in range(10):

        i = idx + 1
        name_dict = {}
        var_dict = {}
        counter = 1
        g = Glucose3()

        add_sold_clause(g)
        add_rules_for_sold(g, i)
        add_rules_for_marketing_and_traders_tuples(g, i)
        add_rules_for_marketing_and_traders(g, i)
        add_rules_for_self_marketing_traders_capability_analysis(g, i)
        add_rules_for_market_analysis(g, i)
        add_rules_for_product_service_creation(g, i)

        for t in test:
            if t[0] == 1:
                g.add_clause([register_var_if_unregistered(t[1])])
            else:
                g.add_clause([-register_var_if_unregistered(t[1])])

        s = g.solve()
        m = g.get_model()


        if not s:
            if i == 10:
                print()
                print("Test case", count)
                print()
                print("failed")
            continue

        print()
        print("Test case", count)
        print()
        print("steps: %d, solved with model:" % (i), s, m)

        for var in m:
            if var > 0:
                print(name_dict[var])

        break

    count += 1
