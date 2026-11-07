

# -------------------- MODULE 2 --------------------
# Final Bill Calculation and Summary Report


def compute_net_invoice(gross_cost, total_units, overload_days, has_solar):
    """Calculate the final invoice after fees, penalties, rebate and tax."""
    net_payable = gross_cost

    # Grid block maintenance fee: PKR 30 for every complete 50-kWh block.
    full_blocks = total_units // 50
    net_payable += full_blocks * 30.0

    # Quadratic penalty for days with consumption above 25 kWh.
    if overload_days != 0:
        penalty = 10.0 * (overload_days ** 2)
        net_payable += penalty

    # Apply a 10% eco-rebate for solar users or households with no overload days.
    if has_solar or not (overload_days > 0):
        net_payable -= net_payable * 0.10

    # Apply 5% government energy sales tax.
    net_payable *= 1.05

    return net_payable


def get_yes_no(prompt):
    """Read a yes/no answer and return True for yes, otherwise False."""
    answer = input(prompt).strip().lower()

    while answer != "yes" and answer != "no":
        print("Please enter yes or no.")
        answer = input(prompt).strip().lower()

    return answer == "yes"


def main():
    # Start the system.
    display_system_banner()

    # Customer registration.
    customer_name = input("Enter Customer Full Name: ").strip()
    meter_id = input("Enter Smart Meter ID: ").strip()
    has_solar = get_yes_no("Does the customer have solar net-metering? (yes/no): ")

    num_days = int(input("Enter Audit Duration in Days: "))
    while num_days <= 0:
        print("Audit duration must be at least 1 day.")
        num_days = int(input("Enter Audit Duration in Days: "))

    # Initialize accumulators before the daily audit loop.
    total_units = 0.0
    gross_bill = 0.0
    overload_days = 0

    print("\n--------------- DAILY METER AUDIT ---------------")

    # Collect and process daily meter readings.
    for day in range(1, num_days + 1):
        print("\nDay", day)

        daily_units = float(input("Enter consumed units (kWh): "))
        is_peak = get_yes_no("Was this a Peak Grid-Demand Day? (yes/no): ")

        daily_cost = calculate_daily_tariff(daily_units, is_peak)

        print("Consumed Units : {:.2f} kWh".format(daily_units))
        print("Daily Charge   : PKR {:.2f}".format(daily_cost))

        total_units += daily_units
        gross_bill += daily_cost

        if daily_units > 25:
            overload_days += 1

    # Summary metrics.
    average_usage = total_units / num_days
    full_blocks = int(total_units // 50)
    remainder_units = total_units % 50

    final_invoice = compute_net_invoice(
        gross_bill, total_units, overload_days, has_solar
    )

    # Print the final audit report.
    print("\n" + "=" * 55)
    print("             FINAL SMART AUDIT REPORT")
    print("=" * 55)
    print("Customer Name       :", customer_name)
    print("Smart Meter ID      :", meter_id)
    print("Solar Net-Metering  :", "Yes" if has_solar else "No")
    print("Audit Duration      :", num_days, "days")
    print("-" * 55)
    print("Total Units         : {:.2f} kWh".format(total_units))
    print("Average Daily Usage : {:.2f} kWh".format(average_usage))
    print("Gross Bill          : PKR {:.2f}".format(gross_bill))
    print("Overload Days       :", overload_days)
    print("Complete 50-kWh Blocks:", full_blocks)
    print("Remaining Units     : {:.2f} kWh".format(remainder_units))
    print("-" * 55)
    print("FINAL PAYABLE INVOICE: PKR {:.2f}".format(final_invoice))
    print("=" * 55)

    # Print the automated inspection schedule (every second day).
    print("\nBI-DAILY SMART METER INSPECTION SCHEDULE")
    inspection_found = False

    for day in range(2, num_days + 1, 2):
        print("Automated inspection scheduled for Day", day)
        inspection_found = True

    if not inspection_found:
        print("No inspection scheduled during this audit period.")

    print("\nThank you for using EcoWatt Smart Grid Auditor System")


if __name__ == "__main__":
    main()
