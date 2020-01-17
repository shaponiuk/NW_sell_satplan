from pysat.solvers import Glucose3

# I'll use up to 100 variables per timestamp, eg. 101 indicates that this is a first variable in timestamp1

# 3 dziedziny

counter = 1
name_dict = {}
var_dict = {}

def add_sold_clause(g):
    global counter
    global name_dict
    global var_dict

    g.add_clause([counter])
    name_dict[counter] = "sold"
    var_dict["sold"] = counter

    counter += 1

def add_rules_for_sold(g, desiredTimestamp):
    global counter
    global name_dict

    for i in range(desiredTimestamp):
        clause_list = [-var_dict["sold"]]

        clause_list.append(counter)
        name = "weak marketing, service market, timestamp %d" %(i)
        name_dict[counter] = name
        var_dict[name] = counter
        counter += 1

        clause_list.append(counter)
        name = "strong marketing, service market, timestamp %d" %(i)
        name_dict[counter] = name
        var_dict[name] = counter
        counter += 1

        for j in range(3):
            clause_list.append(counter)
            name = "strong marketing, product market, marketing area %d, market area %d, timestamp %d" %(j, j, i)
            name_dict[counter] = name
            var_dict[name] = counter
            counter += 1

        clause_list.append(counter)
        name = "weak traders, product market, timestamp %d" %(i)
        name_dict[counter] = name
        var_dict[name] = counter
        counter += 1

        clause_list.append(counter)
        name = "strong traders, product market, timestamp %d" %(i)
        name_dict[counter] = name
        var_dict[name] = counter
        counter += 1

        for j in range(3):
            clause_list.append(counter)
            name = "strong traders, service market, trading area %d, market area %d, timestamp %d" %(j, j, i)
            name_dict[counter] = name
            var_dict[name] = counter
            counter += 1

        g.add_clause(clause_list)

def add_rules_for_weak_marketing_tuples(g, timestamp):
    global name_dict, var_dict, counter
    for i in range(timestamp):
        for j in range(i + 1):
            clause_list = [-var_dict["weak marketing, service market, timestamp %d" %(i)], counter]
            name = "weak marketing, timestamp %d" %(j)
            name_dict[counter] = name
            var_dict[name] = counter
            counter += 1
            g.add_clause(clause_list)

            clause_list = [-var_dict["weak marketing, service market, timestamp %d" %(i)], counter]
            name = "service market, timestamp %d" %(j)
            name_dict[counter] = name
            var_dict[name] = counter
            counter += 1
            g.add_clause(clause_list)

def add_rules_for_strong_marketing_tuples(g, timestamp):
    global name_dict, var_dict, counter
    for i in range(timestamp):
        for j in range(i + 1):
            clause_list = [-var_dict["strong marketing, service market, timestamp %d" %(i)], counter]
            name = "strong marketing, timestamp %d" %(j)
            name_dict[counter] = name
            var_dict[name] = counter
            counter += 1
            g.add_clause(clause_list)

            clause_list = [-var_dict["strong marketing, service market, timestamp %d" %(i)], counter]
            name = "service market, timestamp %d" %(j)
            name_dict[counter] = name
            var_dict[name] = counter
            counter += 1
            g.add_clause(clause_list)
            
            for k in range(3):
                clause_list = [-var_dict["strong marketing, product market, marketing area %d, market area %d, timestamp %d" %(k, k, i)], counter]
                name = "strong marketing, timestamp %d" %(j)
                name_dict[counter] = name
                var_dict[name] = counter
                counter += 1
                g.add_clause(clause_list)

                clause_list = [-var_dict["strong marketing, product market, marketing area %d, market area %d, timestamp %d" %(k, k, i)], counter]
                name = "product_market, timestamp %d" %(j)
                name_dict[counter] = name
                var_dict[name] = counter
                counter += 1
                g.add_clause(clause_list)

                clause_list = [-var_dict["strong marketing, product market, marketing area %d, market area %d, timestamp %d" %(k, k, i)], counter]
                name = "marketing area %d, timestamp %d" %(k, j)
                name_dict[counter] = name
                var_dict[name] = counter
                counter += 1
                g.add_clause(clause_list)

                clause_list = [-var_dict["strong marketing, product market, marketing area %d, market area %d, timestamp %d" %(k, k, i)], counter]
                name = "market area %d, timestamp %d" %(k, j)
                name_dict[counter] = name
                var_dict[name] = counter
                counter += 1
                g.add_clause(clause_list)
            
def add_rules_for_marketing_tuples(g, timestamp):
    add_rules_for_weak_marketing_tuples(g, timestamp)
    add_rules_for_strong_marketing_tuples(g, timestamp)

def add_rules_for_weak_traders_tuples(g, timestamp):
    global name_dict, var_dict, counter
    for i in range(timestamp):
        for j in range(i + 1):
            clause_list = [-var_dict["weak traders, product market, timestamp %d" %(i)], counter]
            name = "weak traders, timestamp %d" %(j)
            name_dict[counter] = name
            var_dict[name] = counter
            counter += 1
            g.add_clause(clause_list)

            clause_list = [-var_dict["weak traders, product market, timestamp %d" %(i)], counter]
            name = "product market, timestamp %d" %(j)
            name_dict[counter] = name
            var_dict[name] = counter
            counter += 1
            g.add_clause(clause_list)

def add_rules_for_strong_traders_tuples(g, timestamp):
    global name_dict, var_dict, counter
    for i in range(timestamp):
        for j in range(i + 1):
            clause_list = [-var_dict["strong traders, product market, timestamp %d" %(i)], counter]
            name = "strong traders, timestamp %d" %(j)
            name_dict[counter] = name
            var_dict[name] = counter
            counter += 1
            g.add_clause(clause_list)

            clause_list = [-var_dict["strong traders, product market, timestamp %d" %(i)], counter]
            name = "product market, timestamp %d" %(j)
            name_dict[counter] = name
            var_dict[name] = counter
            counter += 1
            g.add_clause(clause_list)
            
            for k in range(3):
                clause_list = [-var_dict["strong traders, service market, trading area %d, market area %d, timestamp %d" %(k, k, i)], counter]
                name = "strong traders, timestamp %d" %(j)
                name_dict[counter] = name
                var_dict[name] = counter
                counter += 1
                g.add_clause(clause_list)

                clause_list = [-var_dict["strong traders, service market, trading area %d, market area %d, timestamp %d" %(k, k, i)], counter]
                name = "service_market, timestamp %d" %(j)
                name_dict[counter] = name
                var_dict[name] = counter
                counter += 1
                g.add_clause(clause_list)

                clause_list = [-var_dict["strong traders, service market, trading area %d, market area %d, timestamp %d" %(k, k, i)], counter]
                name = "trading area %d, timestamp %d" %(k, j)
                name_dict[counter] = name
                var_dict[name] = counter
                counter += 1
                g.add_clause(clause_list)

                clause_list = [-var_dict["strong traders, service market, trading area %d, market area %d, timestamp %d" %(k, k, i)], counter]
                name = "market area %d, timestamp %d" %(k, j)
                name_dict[counter] = name
                var_dict[name] = counter
                counter += 1
                g.add_clause(clause_list)

def add_rules_for_traders_tuples(g, timestamp):
    add_rules_for_weak_traders_tuples(g, timestamp)
    add_rules_for_strong_traders_tuples(g, timestamp)

def add_rules_for_marketing_and_traders_tuples(g, timestamp):
    add_rules_for_marketing_tuples(g, timestamp)
    add_rules_for_traders_tuples(g, timestamp)

def add_rules_for_weak_marketing(g, timestamp):
    for i in range(timestamp):
        

def add_rules_for_marketing(g, timestamp):
    add_rules_for_weak_marketing(g, timestamp)
    add_rules_for_strong_marketing(g, timestamp)
    add_rules_for_marketing_area(g, timestamp)

def add_rules_for_traders(g, timestamp):

def add_rules_for_marketing_and_traders(g, timestamp):
    add_rules_for_marketing(g, timestamp)
    add_rules_for_traders(g, timestamp)

for i in range(1):
    name_dict = {}
    var_dict = {}
    counter = 1
    g = Glucose3()

    add_sold_clause(g)
    add_rules_for_sold(g, i + 1)
    add_rules_for_marketing_and_traders_tuples(g, i + 1)
    add_rules_for_marketing_and_traders(g, i + 1)

    s = g.solve()
    m = g.get_model()

    print("steps: %d, solved with model:" %(i + 1), s, m)

    if not s:
        continue
    for var in m:
        if var > 0:
            print(name_dict[var])
