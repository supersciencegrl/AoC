example = """Time:      7  15   30
Distance:  9  40  200"""
example = example.split('\n')

with open('Day6.txt', 'rt') as fin:
    input_text = fin.readlines()

def product(my_list):
    pdt = 1
    for i in my_list:
        pdt *= i

    return pdt

def count_ways(time, record):
    ways = 0
    for button_press in range(1,time):
        distance = (time - button_press) * button_press
        if distance > record:
            ways += 1

    return ways

def day2_part1(input_text):
    times = input_text[0].split()[1:]
    records = input_text[1].split()[1:]

    results = []
    for (idx, time) in enumerate(times):
        ways = count_ways(int(time), int(records[idx]))
        results.append(ways)
    result = product(results)

    return result

def day2_part2(input_text):
    times = input_text[0].split()[1:]
    records = input_text[1].split()[1:]
    new_time = int(('').join(times))
    new_record = int(('').join(records))

    ways = count_ways(new_time, new_record)

    return ways

part1_result = day2_part1(input_text)
print(f'Part 1 result: {part1_result}')
if part1_result == 1195150:
    print('PASS')
part2_result = day2_part2(input_text)
print(f'Part 2 result: {part2_result}')
if part2_result == 42550411:
    print('PASS')
