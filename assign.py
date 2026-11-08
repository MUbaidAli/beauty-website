def display_system_banner():
    print("===============================================")
    print("          EcoWatt Smart Grid Auditor             ")
    print("===============================================")

def calculate_daily_tariff(units,is_peak_day):
    
    if(units <=0 ):
        daily_cost = 0.0
    elif(units > 0 and units <= 10):
        daily_cost = units * 10.0
    elif(units > 10 and units <= 25):
        daily_cost = units * 15.0
    else:
        daily_cost = (units * 20.0) + ((units - 25) * 5.0)

    if(is_peak_day and units > 20):
        daily_cost *= 1.10
    return daily_cost;


# net invoice calculation function

def compute_net_invoice(gross_cost , total_units , overload_days, has_solar):
    net_payable = gross_cost

    # grid Block maintaince fee
    full_block = total_units // 50
    net_payable += full_block * 30

    # quadratic overload penalty
    if overload_days != 0:
        penalty = 10.2 * (overload_days ** 2)
        net_payable += penalty

    # green eco rebate
    if has_solar or not (overload_days > 0):
        net_payable -= net_payable * 0.10

     # 5% government energy sales tax.
    net_payable *= 1.05

    return net_payable;



# main function to run the system 
def main():
    # system banner function
    display_system_banner()
    # user inputs

    customer_name = input("Enter Customer Name: ")
    smart_meter_id = int(input("Enter Smart Meter ID: "))
    solor_net_metering_status = input("Does the customer have solar net-metering? Answer in (Yes/No): ").lower()
    audit_duration_days = int(input("Enter Audit Duration Days: "))

    print("\n--------------- DAILY METER AUDIT ---------------")
    

    total_units = 0.0
    gross_bill  = 0.0
    overload_days = 0

    for day in range(1, audit_duration_days + 1 ):
        # get daily units consumed
        daily_units = float(input("Enter consumed units (kWh) for Day {}: ".format(day)))
        is_peak_day_input = input("Was this a Peak Grid-Demand Day? (Yes/No): ").lower()
        is_peak_day = is_peak_day_input == "yes"
        daily_cost = calculate_daily_tariff(daily_units, is_peak_day);

        print("Daily Units Consumed: {:.2f} kWh".format(daily_units))
        print("Daily Cost: PKR {:.2f}".format(daily_cost))

        total_units += daily_units
        gross_bill += daily_cost

        if(daily_units >   25):
            overload_days += 1

    # summary metrics
    average_daily_usage = total_units / audit_duration_days
    full_block = int(total_units // 50)
    remainder_units = total_units % 50

    net_invoice = compute_net_invoice(gross_bill, total_units, overload_days, solor_net_metering_status == "yes")

    # summary
    print("===============================================")
    print("    FINAL AUDIT REPORT                ")
    print("===============================================")
    print("Customer Name: ", customer_name)
    print("Smart Meter ID: ", smart_meter_id)
    print("Solar Net-Metering Status: ", solor_net_metering_status)
    print("Audit Duration: ", audit_duration_days, "days")
    print("Total Units Consumed: " , "{:.2f} kWh".format(total_units))  
    print("Average Daily Usage: " , "{:.2f} kWh".format(average_daily_usage))
    print("Gross Bill Amount: PKR {:.2f}".format(gross_bill))
    print("Total Overload Days: ", overload_days)
    print("Complete 50-kWh Blocks: ", full_block)
    print("Remaining Units: ", "{:.2f} kWh".format(remainder_units))
    print("Final Invoice Amount: PKR {:.2f}".format(net_invoice))
    print("===============================================")

    is_inspection_found = False

    for day in range(2 ,audit_duration_days + 1 ,2):
        print("Automated inspection scheduled for Day", day)
        is_inspection_found = True

    print("\nThank you for using EcoWatt Smart Grid Auditor System")
    




main()

