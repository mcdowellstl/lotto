import random
import csv
import datetime

num_dict = {}  # type: Dict[int, int]

# Knobs to turn
sample_size = 24    # how big of a set of numbers to choose from
ticket_numbers = 8   # how many numbers to generate
hot_number_weight = 3  # counter bonus for hot numbers
random_generation = 5000  # how many random numbers to add to the formula

print "[[[ Missouri Lottery - Number Generator ]]]"
print "Get the most recent csv from: http://www.molottery.com/winningNumbers.do?method=forward#Lotto"
print "---------------------------------------------------------------------------------------------"


# Set the empty dictionary
for i in range(44):
    num_dict[i+1] = 0

# Read the entire lotto history to get a counter for each number
with open('lo.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=",")
    line_count = 0
    for row in csv_reader:
        if line_count != 0:
            for n in range(7):
                if n > 0:
                    number = int(row[n])
                    number_total = num_dict[number]
                    num_dict[number] = number_total + 1
        line_count += 1

# Read the most recent lotto numbers (last year) as a subset and add weight
with open('lo_2018.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=",")
    line_count = 0
    for row in csv_reader:
        if line_count != 0:
            for n in range(7):
                if n > 0:
                    number = int(row[n])
                    number_total = num_dict[number]
                    num_dict[number] = number_total + hot_number_weight
        line_count += 1

# Add in random number generation to the weighting
for i in range(random_generation):
    rnum = random.randint(1, 44)
    num_dict[number] = number_total + 1

# Generate subset of numbers based on the most likely numbers to surface
lotto_set = []
num_dict_sorted_keys = sorted(num_dict, key=num_dict.get, reverse=True)
number_selected = 0
for r in num_dict_sorted_keys:
    if r > 0 and r < 45:
        lotto_set.append(r)
        number_selected += 1
    if number_selected >= sample_size:
        break

print "Today's Recommended plays:"

all_picks = []
for tickets in range(ticket_numbers):
    ticket_nums = []
    rando = sorted(random.sample(range(1,len(lotto_set)), 6))

    for j in rando:

        ticket_nums.append(lotto_set[j])



    ticket_nums.sort(key=int)
    all_picks.append(ticket_nums)
    print ticket_nums

playing = raw_input("Playing these numbers? (Y or N)")
if playing in ['y', 'yes', 'Y', "Yes", 'YES']:
    with open("play_history.txt", "a") as logfile:
        logfile.write((datetime.datetime.now().ctime()) + ":\n")
        for num in all_picks:
            logfile.write(str(num) + "\n")
        logfile.write("\n")
