import random
from tabulate import tabulate
import math
import scipy.stats

n_days = 120

def delivery_place():
    place = random.randint(1,2) #where 1 - home delivery & 2 - locker delivery
    if place == 1:
        return 'home'
    else:
        return 'lckr'
    
def id_recipient(acceptance):
    recipient = random.randint(0, 100)
    probability = recipient / 100
    if probability < acceptance:
        return 'OC'
    else:
        return 'not OC'

def delivery_picked():
    picked = random.randint(0, 100)
    probability = picked / 100
    if probability < 0.75:
        return 'picked up'
    else:
        return 'not picked up'
    
def PF_total_cost(total_deliveries):
    num_delivery = 0
    i = 1
    for i in range(total_deliveries+1):
        if i <= 10:
            num_delivery = num_delivery + i * 1
        elif i > 10:
            num_delivery = num_delivery + i * 2 
    return num_delivery
    
def simulate(new_acceptance, new_compensation):
    acc_deliveries_pf = 0
    acc_deliveries_oc = 0
    acc_deliveries_lckr = 0
    
    daily_deliveries_pf = 0
    daily_deliveries_oc = 0
    daily_deliveries_lckr = 0

    left_home = 0
    left_lckr = 0

    remainder_home = 0

    status_home = 0
    status_lckr = 0

    acc_total_cost = 0

    rows = []
    
    for day in range(n_days):
        new_home = 0
        new_lckr = 0

        deliver_oc_aux = 0
        deliver_lckr_aux = 0
        deliver_next_day = 0

        daily_cost_pf = 0
        daily_cost_oc = 0

        expected_deliveries = random.randint(10, 50)

        for e in range(expected_deliveries):
            if delivery_place() == 'home':
                new_home = new_home + 1
            else:
                new_lckr = new_lckr + 1

        status_home = status_home + new_home - remainder_home
        status_lckr = status_lckr + new_lckr - daily_deliveries_lckr

        remainder_home = new_home
        left_home = new_home
        lckr_for = new_lckr + left_lckr
        left_lckr = left_lckr + new_lckr
        
        for h in range(new_home):
            if id_recipient(new_acceptance) == 'OC':
                deliver_oc_aux = deliver_oc_aux + 1
                left_home = left_home - 1

        for l in range(lckr_for):
            if delivery_picked() == 'picked up':
                deliver_lckr_aux = deliver_lckr_aux + 1
                left_lckr = left_lckr - 1
            
        deliver_next_day = left_home 

        acc_deliveries_pf = acc_deliveries_pf + daily_deliveries_pf
        acc_deliveries_oc = acc_deliveries_oc + daily_deliveries_oc
        acc_deliveries_lckr = acc_deliveries_lckr + daily_deliveries_lckr

        daily_cost_oc = daily_deliveries_oc * new_compensation
        daily_cost_pf = PF_total_cost(daily_deliveries_pf)
        acc_total_cost = acc_total_cost + daily_cost_oc + daily_cost_pf
        
        rows.append([day+1, new_home, new_lckr, daily_deliveries_pf, daily_deliveries_oc, daily_deliveries_lckr, acc_deliveries_pf, acc_deliveries_oc, acc_deliveries_lckr, daily_cost_pf, daily_cost_oc, acc_total_cost, status_home, status_lckr])
        daily_deliveries_pf = deliver_next_day
        daily_deliveries_oc = deliver_oc_aux
        daily_deliveries_lckr = deliver_lckr_aux

    #print(tabulate(rows, headers=['DAY', 'NEW_HOME', 'NEW_LCKR', 'DEL_PF', 'DEL_OC', 'DEL_LOCKER', 'ACC_PF', 'ACC_OC', 'ACC_LCKR', 'c_PF', 'C_OC', 'C_ACC', 'STATUS_H', 'STATUS_L']))
    return (acc_total_cost, status_lckr)
    
n_sim = 10000

compensation = [0.0, 0.5, 1.0, 1.5, 1.8]
acceptance = [0.01, 0.25, 0.5, 0.6, 0.75]

costs = []
max_items_lckr = []

def run_simulate(new_acceptance, new_compensation):
    for i in range(n_sim):            
        (this_costs, this_max_items_lckr) = simulate(new_acceptance, new_compensation)
        costs.append(this_costs)
        max_items_lckr.append(this_max_items_lckr)
    return (costs, max_items_lckr)

def mean_confidence_interval(data, alpha):
    n = len(data)
    m = float(sum(data))/n
    var = sum([(x - m) ** 2 for x in data]) / float(n - 1)
    tfact = scipy.stats.t._ppf(1 - alpha/2., n-1)
    h = tfact * math.sqrt(var / n)
    return m-h, m+h

if __name__ == "__main__":
    confidence = .99
    alpha = 1 - confidence
    for i in range(len(acceptance)):
        new_acceptance = acceptance[i]
        new_compensation = compensation[i]
        print("For acceptance {} with compensation {}...".format(new_acceptance, new_compensation))
        (data_costs, data_max_items_lckr) = run_simulate(new_acceptance, new_compensation)
        (min_costs, max_costs) = mean_confidence_interval(data_costs, alpha)
        (min_lckr, max_lckr) = mean_confidence_interval(data_max_items_lckr, alpha)
        print("The expected total cost is ({}, {})".format(min_costs, max_costs))
        print("The expected maximum number of items stored in the locker is ({}, {})".format(min_lckr, max_lckr))
