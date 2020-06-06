import random
from tabulate import tabulate
#import math
#import scipy.stats


n_sim = 10000

n_days = 5

compensation = [0.0, 0.5, 1.0, 1.5, 1.8]
acceptance = [0.01, 0.25, 0.5, 0.6, 0.75]

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
    for i in range(total_deliveries):
        if i <= 10:
            num_delivery = num_delivery + i * 1
        elif i > 10:
            num_delivery = num_delivery + i * 2 
    return num_delivery

#50/50 probabilidade entregue em casa e entregue em locker
#desses 50% entregue em locker, 75% apanhado pelo OC, 25% apanhado pelo PF
        
    
def simulate():
    remainder_lckr = 0
    remainder_home = 0
    remainder_oc = 0
    remainder_pf = 0

    pf_cost = 0
    oc_cost = 0
    acc_cost = 0

    n_deliveries_oc = 0
    n_deliveries_pf = 0
    n_deliveries_lckr = 0

    accept = 0

    rows = []
        
    for day in range(n_days):
        n_home = 0
        n_lckr = 0
        
        pf_cost_aux = 0
        oc_cost_aux = 0
        
        n_deliveries_pf_aux = 0
        n_deliveries_lckr_aux = 0
        n_deliveries_oc_aux = 0
        
        remainder_lckr_aux = 0
        remainder_oc_aux = 0
        remainder_pf_aux = 0

        new_acceptance = 0
        
        acc_cost_aux = 0

        status_home = 0

        status_lckr = 0
        
        expected_deliveries = random.randint(10, 50)
        for j in range(expected_deliveries):
            if (delivery_place()) == 'lckr':
                n_lckr = n_lckr + 1
            else:
                n_home = n_home + 1
        remainder_lckr_aux = n_lckr
        for k in range(n_lckr):
            if(delivery_picked() == 'picked up'):
                n_deliveries_lckr_aux = n_deliveries_lckr_aux + 1
                remainder_lckr_aux = remainder_lckr_aux - 1
                if remainder_home > 0:
                    new_acceptance = acceptance[accept]
                    #print("Acceptance: ", new_acceptance)
                    if(id_recipient(new_acceptance)) == 'OC':
                        n_deliveries_oc_aux = n_deliveries_oc_aux + 1
                        remainder_home = remainder_home - 1
        n_deliveries_pf_aux = remainder_home + remainder_lckr_aux
        
        remainder_oc_aux = remainder_oc + n_deliveries_oc_aux
        remainder_pf_aux = remainder_pf + n_deliveries_pf_aux
        remainder_lckr_aux = remainder_lckr + n_deliveries_lckr_aux
        
        oc_cost_aux = n_deliveries_oc_aux * compensation[accept]
        #print("Compensation: ", compensation[accept])
        pf_cost_aux = PF_total_cost(n_deliveries_pf_aux)
        acc_cost_aux = acc_cost + oc_cost_aux + pf_cost_aux

        status_home = n_home + remainder_home
        status_lckr = n_lckr + remainder_lckr
        
        if status_home < 0:
            status_home = 0
        if status_lckr < 0:
            status_lckr = 0
        
        rows.append([day+1, n_home, n_lckr, n_deliveries_pf, n_deliveries_oc, n_deliveries_lckr, remainder_pf, remainder_oc, remainder_lckr, pf_cost, oc_cost, acc_cost, status_home, status_lckr])
        n_deliveries_oc = n_deliveries_oc_aux
        n_deliveries_pf = n_deliveries_pf_aux
        n_deliveries_lckr = n_deliveries_lckr_aux
        remainder_oc = remainder_oc_aux
        remainder_pf = remainder_pf_aux
        remainder_lckr = remainder_lckr_aux
        oc_cost = oc_cost_aux
        pf_cost = pf_cost_aux
        acc_cost = acc_cost_aux
        
    print(tabulate(rows, headers=['DAY', 'NEW_HOME', 'NEW_LCKR', 'DEL_PF', 'DEL_OC', 'DEL_LOCKER', 'ACC_PF', 'ACC_OC', 'ACC_LCKR', 'c_PF', 'C_OC', 'C_ACC', 'STATUS_H', 'STATUS_L']))
    accept = accept + 1
    if accept == 4:
        accept = 0

simulate()

'''
def mean_confidence interval(data, alpha):
    m = float(sum(data))/n_sim
    var = sum([(x - m) ** 2 for x in data]) / float(n_sim - 1)
    tfact = scipy.stats.t._ppf(1 - alpha/2., n_sim-1)
    h = tfact * math.sqrt(var / n)
    return m-h, m+h

if __name__ == "__main__":
    confidence = .99
    alpha = 1 - confidence
'''
