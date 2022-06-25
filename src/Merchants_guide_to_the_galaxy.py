# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Created By  : Donia Hariz
# Created Date: 24-Jun-2022
# version ='1.0'
# Python 3.6
# ---------------------------------------------------------------------------
""" This code is the merchant's guide to the galaxy, it translates intergalactic numerals to Arabic numerals
:   and answers the questions of the user accordingly.
:   Translators: a class that contains three translators:
:       - get_roman_from_arabic: Arabic to Roman translator, returns a string of Roman numerals from an integer.
:       - get_arabic_from_roman: Roman to Arabic translator, returns an integer from Roman numeral string.
:       - get_roman_from_intergalactic: Intergalactic to roman, returns a dictionary of Intergalactic string : Roman Numeral.
:   GetCurrencyValue: a class that contains the currency value converter:
:       - get_currency_value: returns a dictionary of currency : value
:   AnswerQuestions: a class that contains two methods for answering user's questions:
:       - answer_much: returns the arabic value of intergalactic value
:       - answer_many: returns the number of credits

"""
# ---------------------------------------------------------------------------
# Imports
import fileinput
# ---------------------------------------------------------------------------

class Translators:
    def __init__(self, roman_numeral: list, ints: list, nums: list):
        self.roman_numeral = roman_numeral
        self.ints = ints
        self.nums = nums

    def get_roman_from_arabic(self, arabic_numeral: int) -> str:
        if not 0 < arabic_numeral < 4000:
            raise Exception("Argument must be between 1 and 3999")
        for i in range(len(self.ints)):  # iterate over all valid arabic values for roman numerals
            count = int(arabic_numeral / self.ints[i])  # count units
            self.roman_numeral.append(
                self.nums[i] * count)  # append the roman numeral value to the roman_numeral list
            arabic_numeral -= self.ints[i] * count  # substitute value
            res = "".join(self.roman_numeral)
        return res

    def get_arabic_from_roman(self: str) -> int:
        ints = [1000, 900, 500, 400, 100, 90, 50, 40, 10, 9, 5, 4, 1]
        nums = ["M", "CM", "D", "CD", "C", "XC", "L", "XL", "X", "IX", "V", "IV", "I"]
        roman_numerals = []
        self.upper()
        roman_digit_to_arabic_digit_conversion_table = {
            "M": 1000,
            "D": 500,
            "C": 100,
            "L": 50,
            "X": 10,
            "V": 5,
            "I": 1,
        }
        arabic_numeral = 0
        for i in range(len(self)):
            try:
                value = roman_digit_to_arabic_digit_conversion_table[self[i]]
                # if the next roman digit is smaller, we substitute
                if i + 1 < len(self) and roman_digit_to_arabic_digit_conversion_table[self[i + 1]] > value:
                    arabic_numeral -= value
                # if the next roman digit is greater, we add
                else:
                    arabic_numeral += value
            except KeyError:
                raise Exception("Invalid Roman numeral detected.")

        # Instantiate Translators
        p = Translators(roman_numerals, ints, nums)

        if Translators.get_roman_from_arabic(p, arabic_numeral) != self:
            raise Exception("Invalid Roman numeral detected.")
        return arabic_numeral

    def get_roman_from_intergalactic(self: str, word_dic: dict, roman_array: list) -> dict:
        arr = self.split()
        if arr[-1] in roman_array:
            input_line_array = self.split(' ')
            word_dic[input_line_array[0]] = input_line_array[2]
        else:
            raise Exception("Invalid Roman numeral " + arr[-1])
        return word_dic


class GetCurrencyValue:
    def get_currency_value(self: str, word_dic: dict, coin_dic: dict) -> dict:
        try:
            if self[-1] == 's':
                input_line_array = self.split(' ')
                temp_str = ''
                for i in range(len(input_line_array) - 4):
                    temp_str += word_dic[input_line_array[i]]
                temp_num = Translators.get_arabic_from_roman(temp_str)
                coin_dic[input_line_array[-4]] = int(input_line_array[-2]) / int(temp_num)
            return coin_dic
        except Exception:
            raise Exception("Unable to read Roman numeral")


class AnswerQuestions:
    def answer_much(self: str, word_dic: dict) -> str:
        input_line_array = self.split(' ')
        temp_str1 = ''
        temp_str3 = ''
        for i in range(3, len(input_line_array) - 1):
            temp_str3 += input_line_array[i] + ' '
            temp_str1 += word_dic[input_line_array[i]]
        return temp_str3 + "is " + str(Translators.get_arabic_from_roman(temp_str1))

    def answer_many(self: str, coin_dic: dict, word_dic: dict) -> str:
        value = ''
        input_line_array = self.split(' ')
        temp_str2 = ''
        temp_str4 = ''
        for i in range(4, len(input_line_array) - 2):
            temp_str4 += input_line_array[i] + ' '
            temp_str2 += word_dic[input_line_array[i]]
            value: str = temp_str4 + input_line_array[-2] + ' is ' + str(
                int(coin_dic[input_line_array[-2]]) * Translators.get_arabic_from_roman(
                    temp_str2)) + ' Credits'
        return value


def main():
    # Initialize
    intergalactic_roman_dict = {}
    currency_dict = {}
    roman_array = ['I', 'V', 'X', 'L', 'C', 'D', 'M']

    for line in fileinput.input("input.txt"):  # iterate over every line of the text file
        input_string = line[:-1]
        input_line_array = input_string.split(' ')
        try:
            if input_string[-1] in roman_array:  # case 1: the sentence is informative about values
                intergalactic_roman_dict = Translators.get_roman_from_intergalactic(input_string,
                                                                                    intergalactic_roman_dict,
                                                                                    roman_array)

            elif input_string[-1] == 's':  # case 2: the sentence is informative about number of credits
                currency_dict = GetCurrencyValue.get_currency_value(input_string, intergalactic_roman_dict,
                                                                    currency_dict)

            elif input_string[-1] == '?':  # case 3: the sentence is a question
                if input_line_array[1] == 'much':  # case 3.1: the question is how much
                    arr_data = input_line_array[3:-1]
                    for data in arr_data:
                        if data in intergalactic_roman_dict.keys():
                            continue
                        else:
                            raise Exception(data + " is not a valid Intergalactic numeral")
                    print(AnswerQuestions.answer_much(input_string, intergalactic_roman_dict))

                elif input_line_array[1] == 'many':  # case 3.2: the question is how much
                    arr_data = input_line_array[4:-2]
                    for data in arr_data:
                        if data in intergalactic_roman_dict.keys():
                            continue
                        else:
                            raise Exception(data + " is not a valid Intergalactic numeral")
                    print(AnswerQuestions.answer_many(input_string, currency_dict, intergalactic_roman_dict))

            else:
                raise Exception('I have no idea what you are talking about')

        except Exception as e:
            print(e)


if __name__ == "__main__":
    main()
