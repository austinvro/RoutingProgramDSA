# Student ID : 010594856
# Name : Austin Patton

import csv
import datetime

# =========================
# Define Hash Map class
# =========================


class CreateHashMap:
    # create a  hash table
    def __init__(self, starting_size=20):
        self.list = []
        for i in range(starting_size):
            self.list.append([])

    # insert package to hashtable
    def ht_insert(self, key, package):
        bucket = hash(key) % len(self.list)
        bucket_items = self.list[bucket]

        # Check if key exists and update if it does
        for val in bucket_items:
            if val[0] == key:
                val[1] = package
                return True

        # If key does not exist, append package.
        key_val = [key, package]
        bucket_items.append(key_val)
        return True

    # Search for package in hash table
    def ht_search(self, key):
        bucket = hash(key) % len(self.list)
        bucket_items = self.list[bucket]
        for vals in bucket_items:
            if key == vals[0]:
                return vals[1]
        return None  # Return None if no match is found

    # Remove package from hash table
    def ht_remove(self, key):
        bucket = hash(key) % len(self.list)
        target = self.list[bucket]
        for item in target:
            if item[0] == key:
                target.remove(item)
                return True
        return False

# =========================
# Define Package Class
# =========================


class Package:
    def __init__(self, ID, address, city, state, zipcode, delivery_deadline, weight, status):
        self.ID = ID
        self.address = address
        self.city = city
        self.state = state
        self.zipcode = zipcode
        self.delivery_deadline = delivery_deadline
        self.weight = weight
        self.status = status
        self.departure_time = None
        self.delivery_time = None
        self.truck = None

    # custom str returns a formatted summary of the package details.
    def __str__(self):
        return "%s, %s, %s, %s, %s, %s, %s, %s, %s, %s" % (self.ID, self.address, self.city, self.state,
                                                           self.zipcode, self.delivery_deadline, self.weight,
                                                           self.delivery_time, self.status, self.truck)

    # Set delivery status based on elapsed time
    def get_status(self, elapsed_time):
        # If delivery_time is set and is before elapsed_time, status is Delivered.
        if self.delivery_time is not None and self.delivery_time < elapsed_time:
            self.status = "Delivered"
        # If the package hasn't left the hub yet, it's still at hub..
        elif self.departure_time is not None and self.departure_time > elapsed_time:
            self.status = "At hub"
        else:
            self.status = "En route"

# =========================
# Define Truck Class
# =========================


class Truck:
    def __init__(self, max_packages, average_speed, num_packages, packages, total_miles, address, depart_time):
        self.maxPackages = max_packages
        self.averageSpeed = average_speed
        self.numPackages = num_packages
        self.packages = packages  # List of package IDs
        self.totalMiles = total_miles
        self.address = address  # Current truck location (starting at hub)
        self.depart_time = depart_time
        self.time = depart_time  # Current time for the truck

    # Overloaded string conversion method for Truck.
    def __str__(self):
        return "%s, %s, %s, %s, %s, %s, %s" % (self.maxPackages, self.averageSpeed, self.numPackages, self.packages,
                                               self.totalMiles, self.address, self.depart_time)

# =========================
# Main Code
# =========================


#  addresses from CSV
with open("CSV/WGUPS_Addresses.csv") as addressFile:
    CSV_Address = csv.reader(addressFile)
    CSV_AddressList = []
    next(CSV_Address)  # Skip header
    for row in CSV_Address:
        CSV_AddressList.append(row)

#  distances from CSV
with open("CSV/WGUPS_Distance.csv") as distanceFile:
    CSV_Distance = csv.reader(distanceFile)
    CSV_DistanceList = []
    next(CSV_Distance)
    for row in CSV_Distance:
        CSV_DistanceList.append(row)

#  packages from CSV
with open("CSV/WGUPS_Packages.csv") as packageFile:
    CSV_Packages = csv.reader(packageFile)
    CSV_PackageList = []
    next(CSV_Packages)
    for row in CSV_Packages:
        CSV_PackageList.append(row)

# Method to create package objects from CSV file and insert into hash table.


def add_packages(filename, hash_table):
    with open(filename) as package_file:
        package_data = csv.reader(package_file)
        next(package_data)  # Skip header
        for package in package_data:
            pack_id = int(package[0])
            pack_address = package[1]
            pack_city = package[2]
            pack_state = package[3]
            pack_zip = package[4]
            pack_deadline = package[5]
            pack_weight = package[6]
            pack_status = "At hub"

            # Create new Package object (assumes __init__ sets delivery_deadline attribute)
            pack = Package(pack_id, pack_address, pack_city, pack_state,
                           pack_zip, pack_deadline, pack_weight, pack_status)
            # Insert package into hash table
            hash_table.ht_insert(pack_id, pack)

# Method to determine distance between two addresses using the CSV_DistanceList


def calculate_distance(x, y):
    distance = CSV_DistanceList[x][y]
    if distance == '':
        distance = CSV_DistanceList[y][x]
    return float(distance)

# Method to get the address ID from CSV_AddressList based on an address string


def get_address_id(address):
    for r in CSV_AddressList:
        if address in r[2]:
            return int(r[0])


# =========================
# Create Truck Objects with Updated Package Assignments
# =========================
# - Truck 1: Regular packages with grouping requirement (packages 14, 15, and 19 together)
# - Truck 2: Contains truck-2–only packages (3, 18, 36, 38) plus others
# - Truck 3: Contains delayed packages (6, 25, 28, 32) plus remaining packages
truck1 = Truck(16, 18, None,
               [1, 13, 14, 15, 16, 19, 20, 29, 30, 31, 34, 37, 40],
               0.0, "4001 South 700 East", datetime.timedelta(hours=8))
truck2 = Truck(16, 18, None,
               [3, 12, 17, 18, 21, 22, 23, 24, 26, 27, 35, 36, 38, 39],
               0.0, "4001 South 700 East", datetime.timedelta(hours=8))
truck3 = Truck(16, 18, None,
               [2, 4, 5, 6, 7, 8, 9, 10, 11, 25, 28, 32, 33],
               0.0, "4001 South 700 East", datetime.timedelta(hours=9, minutes=5))

# Set truck_id attributes for UI purposes
truck1.truck_id = 1
truck2.truck_id = 2
truck3.truck_id = 3

# Create hash table and load in packages
hash_Table = CreateHashMap()
add_packages("CSV/WGUPS_Packages.csv", hash_Table)

# Method to assign packages to a truck using a nearest neighbor algorithm


def assign_packages(truck):
    unsorted = []
    # Move packages (by ID) into an unsorted list (of package objects)
    for idNum in truck.packages:
        package = hash_Table.ht_search(idNum)
        unsorted.append(package)
    truck.packages.clear()

    # Greedy nearest neighbor assignment
    while len(unsorted) > 0:
        destination = 2000
        next_package = None
        for package in unsorted:
            dist = calculate_distance(get_address_id(
                truck.address), get_address_id(package.address))
            if dist <= destination:
                destination = dist
                next_package = package
        truck.packages.append(next_package.ID)
        unsorted.remove(next_package)
        truck.totalMiles += destination  # Add distance to truck's total mileage
        truck.address = next_package.address  # Update truck's current location
        # Update truck's time (at 18 mph)
        truck.time += datetime.timedelta(hours=destination / 18)
        next_package.delivery_time = truck.time
        next_package.departure_time = truck.depart_time


# Assign packages to each truck
assign_packages(truck1)
assign_packages(truck2)
assign_packages(truck3)
totalMiles = truck1.totalMiles + truck2.totalMiles + truck3.totalMiles

# =========================
# UI Functions to Print Status
# =========================
# Function to print overall package status in a table format


def print_overall_status(query_delta, user_time):
    header = (f"{'ID':<3} {'Address':<40} {'City':<15} {'State':<8} {'Zip':<6} "
              f"{'Deadline':<10} {'Wt':<4} {'Del Time':<12} {'Status':<10} {'Truck':<8}")
    print("\n" + header)
    print("-" * len(header))
    for packageID in range(1, 41):
        package = hash_Table.ht_search(packageID)
        package.get_status(query_delta)
        # Update package #9's address if query time is past 10:20 AM
        if package.ID == 9 and query_delta >= datetime.timedelta(hours=10, minutes=20):
            package.address = '410 S. State St.'
            package.city = 'Salt Lake City'
            package.state = 'Utah'
            package.zipcode = '84111'
        # Determine truck assignment based on package ID
        if package.ID in truck1.packages:
            package.truck = 'Truck 1'
        elif package.ID in truck2.packages:
            package.truck = 'Truck 2'
        elif package.ID in truck3.packages:
            package.truck = 'Truck 3'
        delivery_time = package.delivery_time if package.delivery_time else "N/A"
        # Use package.delivery_deadline for deadline display
        print(f"{package.ID:<3} {package.address:<40} {package.city:<15} {package.state:<8} "
              f"{package.zipcode:<6} {package.delivery_deadline:<10} {package.weight:<4} "
              f"{str(delivery_time):<12} {package.status:<10} {package.truck:<8}")
    print(f"\nTotal combined mileage: {totalMiles:.1f} miles")

# Function to print truck-specific package status in a table format


def print_truck_status(truck, query_delta, user_time):
    header = (f"{'ID':<3} {'Address':<40} {'City':<15} {'State':<8} {'Zip':<6} "
              f"{'Deadline':<10} {'Wt':<4} {'Del Time':<12} {'Status':<10} {'Truck':<8}")
    print(f"\n--- Status for Truck {truck.truck_id} at {user_time} ---")
    print(header)
    print("-" * len(header))
    for pkg_id in truck.packages:
        package = hash_Table.ht_search(pkg_id)
        package.get_status(query_delta)
        if package.ID == 9 and query_delta >= datetime.timedelta(hours=10, minutes=20):
            package.address = '410 S. State St.'
            package.city = 'Salt Lake City'
            package.state = 'Utah'
            package.zipcode = '84111'
        package.truck = f"Truck {truck.truck_id}"
        delivery_time = package.delivery_time if package.delivery_time else "N/A"
        print(f"{package.ID:<3} {package.address:<40} {package.city:<15} {package.state:<8} "
              f"{package.zipcode:<6} {package.delivery_deadline:<10} {package.weight:<4} "
              f"{str(delivery_time):<12} {package.status:<10} {package.truck:<8}")
    print(
        f"Truck {truck.truck_id} total miles so far: {truck.totalMiles:.1f} miles")

# =========================
# Main UI
# =========================


def main():
    print("WGU Parcel Tracking Service:")
    while True:
        print("\nMENU:")
        print("  1: Overall package status at a specific time")
        print("  2: Single truck status at a specific time")
        print("  3: Credits")
        print("  (Type 'exit' to quit)")
        choice = input("Enter selection: ").strip().lower()

        if choice == "exit":
            break

        elif choice == "1":
            user_time = input("Enter time (e.g., '08:35 AM'): ").strip()
            try:
                query_time = datetime.datetime.strptime(
                    user_time, "%I:%M %p").time()
                query_delta = datetime.timedelta(hours=query_time.hour,
                                                 minutes=query_time.minute,
                                                 seconds=query_time.second)
                print(f"\n--- Overall Package Status at {user_time} ---")
                print_overall_status(query_delta, user_time)
            except ValueError:
                print("Invalid time format. Please try again.")

        elif choice == "2":
            truck_choice = input("Enter truck number (1, 2, or 3): ").strip()
            if truck_choice not in {"1", "2", "3"}:
                print("Invalid truck number. Please try again.")
                continue
            user_time = input("Enter time (e.g., '08:35 AM'): ").strip()
            try:
                query_time = datetime.datetime.strptime(
                    user_time, "%I:%M %p").time()
                query_delta = datetime.timedelta(hours=query_time.hour,
                                                 minutes=query_time.minute,
                                                 seconds=query_time.second)
                if truck_choice == "1":
                    selected_truck = truck1
                elif truck_choice == "2":
                    selected_truck = truck2
                else:
                    selected_truck = truck3
                print_truck_status(selected_truck, query_delta, user_time)
            except ValueError:
                print("Invalid time format. Please try again.")

        elif choice == "3":
            print("\nWGUPS Routing Program by: Austin Patton Student ID : 010594856 ")
        else:
            print("Invalid option. Please try again.")


if __name__ == "__main__":
    main()
