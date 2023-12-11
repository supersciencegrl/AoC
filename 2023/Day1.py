example = """
1abc2
pqr3stu8vwx
a1b2c3d4e5f
treb7uchet
"""
example = example.split('\n')

example2 = """
two1nine
eightwothree
abcone2threexyz
xtwone3four
4nineeightseven2
zoneight234
7pqrstsixteen
"""
example2 = example2.split('\n')

with open('Day1.txt', 'rt') as fin:
    input_text = fin.readlines()

number_words = ['one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine']

def day1(include_words = False):
    results = []

    for line in [my_string.replace('\n', '') for my_string in input_text]:
        if line:
            numbers = []
            for (pos, char) in enumerate(line):
                if char.isdigit():
                    numbers.append((pos, char))
                elif include_words:
                    try:
                        if any([number == line[pos:][:len(number)] for number in number_words]):
                            digit = line[pos:][:5]
                            for (idx, number_word) in enumerate(number_words):
                                if digit.startswith(number_word):
                                    numbers.append((pos, idx+1))
                                    break
                    except IndexError:
                        pass
            result = int(f'{numbers[0][1]}{numbers[-1][1]}')
            results.append(result)

    result = sum(results)
    return result

part1_result = day1(include_words = False)
print(f'Part 1 result: {part1_result}')
if part1_result == 55172:
    print('PASS')

part2_result = day1(include_words = True)
print(f'Part 2 result: {part2_result}')
if part2_result == 54925:
    print('PASS')
