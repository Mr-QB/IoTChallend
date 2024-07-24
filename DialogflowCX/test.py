def convert_numbers_to_vietnamese(text):
    import re

    def number_to_vietnamese(n):
        units = ["không", "một", "hai", "ba", "bốn", "năm", "sáu", "bảy", "tám", "chín"]
        tens = [
            "mười",
            "hai mươi",
            "ba mươi",
            "bốn mươi",
            "năm mươi",
            "sáu mươi",
            "bảy mươi",
            "tám mươi",
            "chín mươi",
        ]

        if n < 10:
            return units[n]
        elif n < 20:
            return tens[0] if n == 10 else f"{tens[0]} {units[n - 10]}"
        else:
            ten_part = n // 10
            unit_part = n % 10
            return (
                f"{tens[ten_part - 1]} {units[unit_part]}"
                if unit_part
                else tens[ten_part - 1]
            )

    def replace_number(match):
        number = int(match.group())
        return number_to_vietnamese(number)

    return re.sub(r"\d+", replace_number, text)


text = "giờ là 20 giờ"
print(convert_numbers_to_vietnamese(text))
