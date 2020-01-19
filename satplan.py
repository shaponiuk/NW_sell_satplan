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
    global counter
    global name_dict

    for i in range(desiredTimestamp):
        clause_list = [-var_dict["sold"],
                       register_var_if_unregistered("weak marketing, service market, timestamp %d" % (i)),
                       register_var_if_unregistered("strong marketing, service market, timestamp %d" % (i)),
                       register_var_if_unregistered("weak traders, product market, timestamp %d" % (i)),
                       register_var_if_unregistered("strong traders, product market, timestamp %d" % (i))]

        for j in range(3):
            clause_list.append(register_var_if_unregistered(
                "strong marketing, product market, marketing area %d, market area %d, timestamp %d" % (j, j, i)))
            clause_list.append(register_var_if_unregistered(
                "strong traders, service market, trading area %d, market area %d, timestamp %d" % (j, j, i)))

        g.add_clause(clause_list)


def add_rules_for_weak_marketing_tuples(g, timestamp):
    global name_dict, var_dict, counter
    for i in range(timestamp):
        for j in range(i + 1):
            g.add_clause([-var_dict["weak marketing, service market, timestamp %d" % (i)], counter,
                          register_var_if_unregistered("weak marketing, timestamp %d" % (j))])
            g.add_clause([-var_dict["weak marketing, service market, timestamp %d" % (i)], counter,
                          register_var_if_unregistered("service market, timestamp %d" % (j))])


def add_rules_for_strong_marketing_tuples(g, timestamp):
    for i in range(timestamp):
        for j in range(i + 1):
            g.add_clause([-register_var_if_unregistered("strong marketing, service market, timestamp %d" % (i)),
                          register_var_if_unregistered("strong marketing, timestamp %d" % (j))])
            g.add_clause([-register_var_if_unregistered("strong marketing, service market, timestamp %d" % (i)),
                          register_var_if_unregistered("service market, timestamp %d" % (j))])

            for k in range(3):
                g.add_clause([-register_var_if_unregistered(
                    "strong marketing, product market, marketing area %d, market area %d, timestamp %d" % (k, k, i)),
                              register_var_if_unregistered("strong marketing, timestamp %d" % (j))])
                g.add_clause([-register_var_if_unregistered(
                    "strong marketing, product market, marketing area %d, market area %d, timestamp %d" % (k, k, i)),
                              register_var_if_unregistered("product_market, timestamp %d" % (j))])
                g.add_clause([-register_var_if_unregistered(
                    "strong marketing, product market, marketing area %d, market area %d, timestamp %d" % (k, k, i)),
                              register_var_if_unregistered("marketing area %d, timestamp %d" % (k, j))])
                g.add_clause([-register_var_if_unregistered(
                    "strong marketing, product market, marketing area %d, market area %d, timestamp %d" % (k, k, i)),
                              register_var_if_unregistered("market area %d, timestamp %d" % (k, j))])


def add_rules_for_marketing_tuples(g, timestamp):
    add_rules_for_weak_marketing_tuples(g, timestamp)
    add_rules_for_strong_marketing_tuples(g, timestamp)


def add_rules_for_weak_traders_tuples(g, timestamp):
    for i in range(timestamp):
        for j in range(i + 1):
            g.add_clause([-register_var_if_unregistered("weak traders, product market, timestamp %d" % i),
                          register_var_if_unregistered("weak traders, timestamp %d" % j)])
            g.add_clause([-register_var_if_unregistered("weak traders, product market, timestamp %d" % i),
                          register_var_if_unregistered("product market, timestamp %d" % (j))])


def add_rules_for_strong_traders_tuples(g, timestamp):
    for i in range(timestamp):
        for j in range(i + 1):
            g.add_clause([-register_var_if_unregistered("strong traders, product market, timestamp %d" % (i)),
                          register_var_if_unregistered("strong traders, timestamp %d" % (j))])
            g.add_clause([-register_var_if_unregistered("strong traders, product market, timestamp %d" % (i)),
                          register_var_if_unregistered("product market, timestamp %d" % j)])

            for k in range(3):
                g.add_clause([-register_var_if_unregistered(
                    "strong traders, service market, trading area %d, market area %d, timestamp %d" % (k, k, i)),
                               register_var_if_unregistered("strong traders, timestamp %d" % (j))])
                g.add_clause([-register_var_if_unregistered(
                    "strong traders, service market, trading area %d, market area %d, timestamp %d" % (k, k, i)),
                               register_var_if_unregistered("service_market, timestamp %d" % (j))])
                g.add_clause([-register_var_if_unregistered(
                    "strong traders, service market, trading area %d, market area %d, timestamp %d" % (k, k, i)),
                               register_var_if_unregistered("trading area %d, timestamp %d" % (k, j))])
                g.add_clause([-register_var_if_unregistered(
                    "strong traders, service market, trading area %d, market area %d, timestamp %d" % (k, k, i)),
                        register_var_if_unregistered("market area %d, timestamp %d" % (k, j))])


def add_rules_for_traders_tuples(g, timestamp):
    add_rules_for_weak_traders_tuples(g, timestamp)
    add_rules_for_strong_traders_tuples(g, timestamp)


def add_rules_for_marketing_and_traders_tuples(g, timestamp):
    add_rules_for_marketing_tuples(g, timestamp)
    add_rules_for_traders_tuples(g, timestamp)


def add_rules_for_weak_marketing(g, timestamp):
    for i in range(timestamp):
        for j in range(i):
            g.add_clause([-register_var_if_unregistered("weak marketing, timestamp %d" % (i)),
                          register_var_if_unregistered("analysed, able to do weak marketing, timestamp %d" % j)])


def add_rules_for_strong_marketing(g, timestamp):
    for i in range(timestamp):
        for j in range(i):
            g.add_clause([-register_var_if_unregistered("strong marketing, timestamp %d" % (i)),
                          register_var_if_unregistered("analysed, able to do strong marketing, timestamp %d" % j)])


def add_rules_for_marketing_area(g, timestamp):
    for i in range(timestamp):
        for j in range(i):
            g.add_clause([-register_var_if_unregistered("marketing area, timestamp %d" % i),
                          register_var_if_unregistered("chosen service area, timestamp %d" % j),
                          register_var_if_unregistered("chosen product area, timestamp %d" % j)])


def add_rules_for_marketing(g, timestamp):
    add_rules_for_weak_marketing(g, timestamp)
    add_rules_for_strong_marketing(g, timestamp)
    add_rules_for_marketing_area(g, timestamp)


def add_rules_for_weak_traders(g, timestamp):
    for i in range(timestamp):
        for j in range(i):
            g.add_clause([-register_var_if_unregistered("weak traders, timestamp %d" % (i)),
                          register_var_if_unregistered("analysed, able to do weak traders, timestamp %d" % j)])


def add_rules_for_strong_traders(g, timestamp):
    for i in range(timestamp):
        for j in range(i):
            g.add_clause([-register_var_if_unregistered("strong traders, timestamp %d" % (i)),
                          register_var_if_unregistered("analysed, able to do strong traders, timestamp %d" % j)])


def add_rules_for_trading_area(g, timestamp):
    for i in range(timestamp):
        for j in range(i):
            g.add_clause([-register_var_if_unregistered("marketing area, timestamp %d" % i),
                          register_var_if_unregistered("chosen service area, timestamp %d" % j),
                          register_var_if_unregistered("chosen product area, timestamp %d" % j)])


def add_rules_for_traders(g, timestamp):
    add_rules_for_weak_traders(g, timestamp)
    add_rules_for_strong_traders(g, timestamp)
    add_rules_for_trading_area(g, timestamp)


def add_rules_for_marketing_and_traders(g, timestamp):
    add_rules_for_marketing(g, timestamp)
    add_rules_for_traders(g, timestamp)


# def add_rules_for_self_marketing_traders_capability_analysis(g, timestamp):
#     add_rules_for_self_marketing_capability_analysis(g, timestamp)
#     add_rules_for_self_traders_capability_analysis(g, timestap)


for i in range(2):
    name_dict = {}
    var_dict = {}
    counter = 1
    g = Glucose3()

    add_sold_clause(g)
    add_rules_for_sold(g, i + 1)
    add_rules_for_marketing_and_traders_tuples(g, i + 1)
    add_rules_for_marketing_and_traders(g, i + 1)
    # add_rules_for_self_marketing_traders_capability_analysis(g, i + 1)

    s = g.solve()
    m = g.get_model()

    print("steps: %d, solved with model:" % (i + 1), s, m)

    if not s:
        continue
    for var in m:
        if var > 0:
            print(name_dict[var])
