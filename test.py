import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import pandas as pd
import openpyxl


# Hàm nhóm dữ liệu theo một cột nhất định trong DataFrame
def groupData(df, group_name):
    unique_group = df[
        group_name
    ].unique()  # Lấy danh sách các giá trị duy nhất trong cột group_name
    grouped_data = {}  # Khởi tạo từ điển để lưu dữ liệu nhóm
    for unique in unique_group:
        group = df[df[group_name] == unique]  # Lọc dữ liệu theo từng giá trị duy nhất
        grouped_data[unique] = group  # Lưu dữ liệu nhóm vào từ điển

    return grouped_data


# Hàm tạo bảng và xuất dữ liệu màu theo nhóm
def createTablesColor(dataraw, group_type="Lớp khóa học"):
    raw_data = pd.read_excel(dataraw)  # Đọc dữ liệu từ file Excel

    grouped_data = groupData(raw_data, group_type)  # Nhóm dữ liệu theo group_type

    excel_file_outcome = "final_2.xlsx"  # Đặt tên file Excel đầu ra

    with pd.ExcelWriter(
        excel_file_outcome, engine="openpyxl"
    ) as writer:  # Mở file Excel để ghi dữ liệu

        for (
            element_name,
            element_list,
        ) in grouped_data.items():  # Lặp qua từng nhóm dữ liệu
            if not element_list.empty:
                schedule = [
                    [0] * 13 for _ in range(7)
                ]  # Khởi tạo lịch học với 7 ngày và 13 tiết
                for (
                    index,
                    row,
                ) in element_list.iterrows():  # Lặp qua từng dòng trong nhóm dữ liệu
                    if row["Thứ"] != "CN":
                        if int(row["Tiết"].split("-")[0]) == int(
                            row["Tiết"].split("-")[1]
                        ):
                            schedule[int(row["Thứ"]) - 2][
                                int(row["Tiết"].split("-")[0]) - 1
                            ] = row["Mã lớp HP"]
                        else:
                            for lesson in range(
                                int(row["Tiết"].split("-")[0]),
                                int(row["Tiết"].split("-")[1]) + 1,
                            ):
                                schedule[int(row["Thứ"]) - 2][lesson - 1] = row[
                                    "Mã lớp HP"
                                ]
                    else:
                        if int(row["Tiết"].split("-")[0]) == int(
                            row["Tiết"].split("-")[1]
                        ):
                            schedule[6][int(row["Tiết"].split("-")[0]) - 1] = row[
                                "Mã lớp HP"
                            ]
                        for lesson in range(
                            int(row["Tiết"].split("-")[0]),
                            int(row["Tiết"].split("-")[1]) + 1,
                        ):
                            schedule[6][lesson - 1] = row["Mã lớp HP"]

                df = pd.DataFrame(
                    schedule,
                    columns=[
                        "Tiết 1",
                        "Tiết 2",
                        "Tiết 3",
                        "Tiết 4",
                        "Tiết 5",
                        "Tiết 6",
                        "Tiết 7",
                        "Tiết 8",
                        "Tiết 9",
                        "Tiết 10",
                        "Tiết 11",
                        "Tiết 12",
                        "Tiết 13",
                    ],
                )  # Tạo DataFrame từ lịch học
                index_values = [
                    "Thứ 2",
                    "Thứ 3",
                    "Thứ 4",
                    "Thứ 5",
                    "Thứ 6",
                    "Thứ 7",
                    "Chủ nhật",
                ]

                df = df.set_index(pd.Index(index_values))  # Đặt chỉ số cho các dòng
                df_transposed = df.transpose()  # Chuyển đổi DataFrame
                df_transposed.to_excel(
                    writer, sheet_name=element_name, index=False
                )  # Xuất dữ liệu ra sheet trong file Excel


# Hàm đếm số lượng các phần tử None liên tiếp trong danh sách
def countNone(ls):
    first_part = ls[:6]  # Lấy 6 phần tử đầu tiên
    second_part = ls[6:]  # Lấy các phần tử còn lại

    def count_consecutive_none(part):
        max_consecutive_none = 0  # Số lượng lớn nhất của các phần tử None liên tiếp
        current_consecutive_none = 0  # Số lượng hiện tại của các phần tử None liên tiếp
        for item in part:
            if item is None:
                current_consecutive_none += 1
                if current_consecutive_none > max_consecutive_none:
                    max_consecutive_none = current_consecutive_none
            else:
                current_consecutive_none = 0
        return max_consecutive_none

    count_first_part = count_consecutive_none(first_part)  # Đếm trong phần đầu tiên
    count_second_part = count_consecutive_none(second_part)  # Đếm trong phần thứ hai
    count_second_part[0] += 6
    count_second_part[1] += 6

    return max(
        count_first_part, count_second_part
    )  # Trả về số lượng lớn nhất liên tiếp


# Hàm sắp xếp danh sách theo số lần xuất hiện của các phần tử
def sort_list_by_elements(elements, lst=[0, 1, 2, 3, 4, 5], limit=2):
    count_dict = {}  # Từ điển lưu số lần xuất hiện của mỗi phần tử
    for item in elements:
        count_dict[item] = count_dict.get(item, 0) + 1  # Đếm số lần xuất hiện

    elements = [
        item for item in elements if count_dict.get(item, 0) <= limit
    ]  # Lọc các phần tử theo số lần xuất hiện
    lst = [
        item for item in lst if count_dict.get(item, 0) <= limit
    ]  # Lọc danh sách theo số lần xuất hiện
    elements = list(set(elements))  # Loại bỏ các phần tử trùng lặp
    sorted_list = sorted(
        lst, key=lambda x: x in elements, reverse=True
    )  # Sắp xếp danh sách dựa trên sự hiện diện trong elements
    return sorted_list


# Hàm kiểm tra và cập nhật giá trị trong lst_total dựa trên lst
def checkNoneValue(lst, lst_total):
    for i in range(6):  # Lặp qua các hàng
        for j in range(12):  # Lặp qua các cột
            if lst[i][j] is None:
                lst_total[i][j] += 0  # Không thay đổi giá trị
            else:
                lst_total[i][j] += 1  # Tăng giá trị lên 1
    return lst_total


# Hàm vẽ đồ thị 3D của các cột trong ma trận
def plot_matrix_columns_3d(matrix):
    num_rows, num_cols = matrix.shape  # Lấy số hàng và số cột của ma trận
    fig = plt.figure(figsize=(12, 6))  # Tạo hình vẽ với kích thước 12x6
    ax = fig.add_subplot(111, projection="3d")  # Thêm subplot 3D

    x = np.arange(num_rows)  # Tạo mảng x từ 0 đến số hàng
    for i in range(num_cols):  # Lặp qua từng cột
        y = matrix[:, i]  # Lấy dữ liệu của cột hiện tại
        z = i * np.ones(num_rows)  # Tạo mảng z với giá trị bằng chỉ số cột
        color = y  # Sử dụng giá trị của cột để xác định màu sắc
        colormap = plt.get_cmap("viridis")  # Chọn colormap
        normalize = plt.Normalize(min(color), max(color))  # Bình thường hóa giá trị màu
        colors = colormap(normalize(color))  # Tạo màu sắc từ colormap

        ax.bar(
            x, y, z, zdir="y", width=1, color=colors, alpha=0.8, label=f"Column {i + 1}"
        )  # Vẽ cột

    ax.set_xlabel("Row")
    ax.set_ylabel("Column")
    ax.set_zlabel("Value")
    ax.set_title("Matrix Columns in 3D")

    ax.legend()  # Thêm chú thích
    plt.show()  # Hiển thị đồ thị


# Hàm sao chép giá trị từ list1 vào list2 nếu giá trị trong list1 <= 0
def copy_values_below_zero(list1, list2, exceptions):
    for exception in exceptions:  # Xử lý các ngoại lệ
        if isinstance(exception, str) and exception:
            time_exception_start, time_exception_end, day_exception = exception.split(
                "-"
            )  # Tách thông tin ngoại lệ
            for i in range(int(time_exception_start) - 1, int(time_exception_end)):
                list2[int(day_exception) - 2][
                    i
                ] = "exception"  # Đặt giá trị là "exception"

    for i in range(len(list1)):  # Lặp qua các hàng
        for j in range(len(list1[i])):  # Lặp qua các cột
            if list1[i][j] <= 0:  # Nếu giá trị <= 0
                list2[i][j] = list1[i][j]  # Sao chép giá trị vào list2

    return list2


# Lớp công cụ để xử lý và tạo lịch học
class Tool:
    def __init__(self, raw_data_path, threshold=35):
        # Đọc vào file excel chứa dữ liệu
        self.raw_data_path = raw_data_path
        self.raw_data = pd.read_excel(self.raw_data_path)  # Đọc dữ liệu từ file Excel

        # Khởi tạo mẫu thời khóa biểu
        self.schedule = [
            [None] * 13 for _ in range(6)
        ]  # Khởi tạo lịch học với 6 ngày và 13 tiết mỗi ngày
        self.final_schedule = pd.DataFrame(
            columns=self.raw_data.columns
        )  # DataFrame để lưu kết quả cuối cùng
        self.schedule_total = [[0] * 13 for _ in range(6)]  # Tương tự như self.schedule

        self.threshold = [
            [threshold] * 13 for _ in range(6)
        ]  # Khởi tạo ngưỡng để phân bổ lịch
        self.exception = None

        self.courses_code = {}  # Từ điển lưu mã học phần và các ngoại lệ

    def groupData(self, group_name):
        # Thực hiện chia nhóm các dòng dữ liệu theo group_name
        unique_group = self.raw_data[group_name].unique()  # Lấy các giá trị duy nhất
        grouped_data = {}
        for unique in unique_group:
            group = self.raw_data[
                self.raw_data[group_name] == unique
            ]  # Lọc dữ liệu theo giá trị duy nhất
            grouped_data[unique] = group  # Lưu vào từ điển

        return grouped_data

    def makeSchedule(self):
        ## Chia nhóm theo "Lớp khóa học"
        nganh_grouped_data = self.groupData("Lớp khóa học")

        for (
            element_name,
            element_list,
        ) in nganh_grouped_data.items():  # Lặp qua từng nhóm
            self.prioritize = []  # Danh sách ưu tiên các ngày học

            self.schedule = [[None] * 13 for _ in range(6)]  # Khởi tạo lại lịch học
            for index, row in element_list.iterrows():  # Lặp qua từng dòng dữ liệu
                ## Các môn không cần xếp lịch
                if row["Số tiết/tuần"] == 0:
                    self.final_schedule = pd.concat(
                        [self.final_schedule, pd.DataFrame([row])], ignore_index=True
                    )

                ## Các môn đã xếp lịch cố định
                elif pd.notna(row["Thứ"]):
                    if row["Thứ"] in [2, 3, 4, 5, 6, 7]:
                        self.prioritize.append(
                            int(row["Thứ"]) - 2
                        )  # Thêm ngày học vào danh sách ưu tiên
                        self.final_schedule = pd.concat(
                            [self.final_schedule, pd.DataFrame([row])],
                            ignore_index=True,
                        )
                        for lesson in range(
                            int(row["Tiết"].split("-")[0]),
                            int(row["Tiết"].split("-")[1]) + 1,
                        ):
                            self.schedule[int(row["Thứ"]) - 2][lesson - 1] = row[
                                "Mã lớp HP"
                            ]
                            self.threshold[int(row["Thứ"]) - 2][lesson - 1] -= 1

                            new_exception = (
                                row["Tiết"].split("-")[0]
                                + "-"
                                + row["Tiết"].split("-")[1]
                                + "-"
                                + str(int(row["Thứ"]))
                            )
                            if row["Mã học phần"] in self.courses_code:
                                self.courses_code[row["Mã học phần"]].append(
                                    new_exception
                                )
                            else:
                                self.courses_code[row["Mã học phần"]] = []
                                self.courses_code[row["Mã học phần"]].append(
                                    new_exception
                                )
                ## Các lớp chưa được xếp lịch
                else:
                    if row["Số buổi học"] >= 2:
                        for i in range(int(row["Số buổi học"])):
                            self.arrangementSchedule(row=row)
                    else:
                        self.arrangementSchedule(row=row)
        print(self.threshold)

    def arrangementSchedule(self, row):
        prioritize = sort_list_by_elements(self.prioritize)  # Sắp xếp các ngày ưu tiên
        if row["Mã học phần"] in self.courses_code:
            exceptions = [row["Tránh lịch"]] + self.courses_code[
                row["Mã học phần"]
            ]  # Lấy các ngoại lệ
        else:
            exceptions = [row["Tránh lịch"]]
        schedule = copy_values_below_zero(
            self.threshold, self.schedule, exceptions
        )  # Cập nhật lịch học
        for day in prioritize:  # Lặp qua các ngày ưu tiên
            if countNone(schedule[day]) >= (
                int(row["Số tiết/tuần"]) / (row["Số buổi học"])
            ):
                self.prioritize.append(day)
                row["Thứ"] = day + 2  # Cập nhật ngày học
                time_lesson = self.selectLesson(
                    schedule[day], int(row["Số tiết/tuần"] / row["Số buổi học"])
                )
                row["Tiết"] = str(time_lesson[0] + 1) + "-" + str(time_lesson[1] + 1)
                self.final_schedule = pd.concat(
                    [self.final_schedule, pd.DataFrame([row])], ignore_index=True
                )

                new_exception = (
                    str(time_lesson[0] + 1)
                    + "-"
                    + str(time_lesson[1] + 1)
                    + "-"
                    + str(day + 2)
                )
                if row["Mã học phần"] in self.courses_code:
                    self.courses_code[row["Mã học phần"]].append(new_exception)
                else:
                    self.courses_code[row["Mã học phần"]] = []
                    self.courses_code[row["Mã học phần"]].append(new_exception)

                for i in range(time_lesson[0], time_lesson[1] + 1):
                    self.schedule[day][i] = row["Mã lớp HP"]
                    self.threshold[day][i] -= 1
                break

    def selectLesson(self, time_day, quantity):
        first_part = time_day[:6]  # Phần đầu tiên của thời gian
        second_part = time_day[6:]  # Phần thứ hai của thời gian

        def count_consecutive_none(part):
            current_consecutive_none = 0
            for i, item in enumerate(part):
                if item is None:
                    current_consecutive_none += 1
                    if current_consecutive_none == quantity:
                        return [i - quantity + 1, i]
                else:
                    current_consecutive_none = 0
            return [0, 0]

        count_first_part = count_consecutive_none(
            first_part
        )  # Đếm số lượng liên tiếp trong phần đầu tiên
        count_second_part = count_consecutive_none(
            second_part
        )  # Đếm số lượng liên tiếp trong phần thứ hai
        count_second_part[0] += 6
        count_second_part[1] += 6

        max_positions = max(
            [count_first_part, count_second_part], key=lambda x: x[1] - x[0]
        )  # Chọn vị trí tốt nhất
        return max_positions

    def exportResult(self):
        self.final_schedule.to_excel(
            "final.xlsx", index=False
        )  # Xuất kết quả ra file Excel

    def run(self):
        # Thực hiện chạy tuần tự chương trình và xuất ra file kết quả cuối cùng
        self.makeSchedule()
        self.exportResult()
