import 'dart:ffi';
import 'dart:async';
import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';
import 'package:rcapp/config.dart';

class SmartPlug extends StatefulWidget {
  final int notificationCount; // Thêm biến này

  const SmartPlug({Key? key, required this.notificationCount})
      : super(key: key);

  @override
  State<SmartPlug> createState() => _SmartPlugPageState();
}

class _SmartPlugPageState extends State<SmartPlug> {
  List mySmartPlugs = [];
  List plugNotConfig = [];

  Future<List<dynamic>> fetchDevices() async {
    final response = await http.get(Uri.parse(
        AppConfig.http_url + "/getdevices")); // Thay đổi URL nếu cần thiết
    if (response.statusCode == 200) {
      return jsonDecode(response.body);
    } else {
      throw Exception('Failed to load data');
    }
  }

  Future<List<dynamic>> fetchDeviceNoConfig() async {
    print(AppConfig.http_url);
    final response = await http.get(Uri.parse(AppConfig.http_url +
        "/checkdevicesnotconfig")); // Thay đổi URL nếu cần thiết
    if (response.statusCode == 200) {
      return jsonDecode(response.body);
    } else {
      throw Exception('Failed to load data');
    }
  }

  Future<void> _refreshData() async {
    try {
      final data = await fetchDeviceNoConfig();
      List<List<dynamic>> nestedList = [];

      for (var item in data) {
        String deviceName = item['device_name'] ?? '';
        String roomName = item['room_name'] ?? '';
        bool status =
            item['status'] == 1; // Chuyển đổi '1' thành true, '0' thành false
        int deviceId = int.tryParse(item['id'].toString()) ??
            0; // Parse id thành số nguyên, mặc định là 0 nếu không thành công

        List<dynamic> subList = [deviceName, roomName, deviceId, status];
        nestedList.add(subList);
      }

      setState(() {
        plugNotConfig = nestedList;
      });
    } catch (error) {
      print('Error: $error');
      // Xử lý lỗi khi gọi API
    }
  }

  @override
  void initState() {
    _refreshData();
    super.initState();
    fetchDevices().then((data) {
      List<List<dynamic>> nestedList = [];

      for (var item in data) {
        String deviceName = item['device_name'] ?? '';
        String roomName = item['room_name'] ?? '';
        bool status =
            item['status'] == 1; // Chuyển đổi '1' thành true, '0' thành false
        int deviceId = (item['id']) ?? '';

        List<dynamic> subList = [deviceName, roomName, deviceId, status];
        nestedList.add(subList);
      }

      setState(() {
        mySmartPlugs = nestedList;
      });
    }).catchError((error) {
      print('Error: $error');
      // Xử lý lỗi khi gọi API
    });
  }

  @override
  Widget build(BuildContext context) {
    return SafeArea(
      child: Scaffold(
        backgroundColor: Colors.indigo.shade50,
        body: Container(
          margin: const EdgeInsets.only(top: 18, left: 24, right: 24),
          child: Column(
            children: [
              // Container(
              //   child: Row(
              //     children: [
              //       Container(
              //         child: Icon(Icons.messenger),
              //       ),
              //       SizedBox(
              //         width: 280,
              //       ),
              //       Container(
              //         child: Image(
              //           image: AssetImage('lib/images/user_avatar.png'),
              //           width: 40,
              //           height: 60,
              //         ),
              //       )
              //     ],
              //   ),
              // ), //app bar
              // Container(
              //   child: Row(
              //     children: [
              //       Container(
              //         child: Column(
              //           mainAxisAlignment: MainAxisAlignment.start,
              //           children: [
              //             Text("Welcome home"),
              //             Text(
              //               "shoaib aslam",
              //               style: TextStyle(fontWeight: FontWeight.w500),
              //             )
              //           ],
              //         ),
              //       ),
              //       Container(
              //         child: Image(
              //           image: AssetImage("lib/images/home.png"),
              //           width: 200,
              //           height: 100,
              //         ),
              //       )
              //     ],
              //   ),
              // ), //title and the illustration section
              Row(
                mainAxisAlignment: MainAxisAlignment.spaceBetween,
                children: [
                  GestureDetector(
                    onTap: () {
                      Navigator.pop(context);
                    },
                    child: const Icon(
                      Icons.arrow_back_ios,
                      color: Colors.indigo,
                    ),
                  ),
                  Stack(
                    alignment: Alignment
                        .topRight, // Căn chỉnh số màu đỏ ở góc trên bên phải
                    children: [
                      GestureDetector(
                        onTap: () async {
                          await _refreshData();
                          showDialog(
                            context: context,
                            builder: (BuildContext context) {
                              return CustomDialog(
                                onRefreshData: () {
                                  _refreshData(); // Gọi hàm `_refreshData` khi dialog được hiển thị
                                },
                                deviceId: plugNotConfig[0]
                                    [2], // Cung cấp giá trị deviceId
                              );
                            },
                          );
                        },
                        child: const RotatedBox(
                          quarterTurns:
                              1, // Đã thay đổi từ 135 thành 1 (90 độ) để đúng với góc xoay
                          child: Icon(Icons.bar_chart_rounded,
                              color: Colors.indigo, size: 35),
                        ),
                      ),
                      Positioned(
                        child: Container(
                          padding: EdgeInsets.all(2),
                          decoration: BoxDecoration(
                            color: Colors.red,
                            borderRadius: BorderRadius.circular(10),
                          ),
                          constraints: BoxConstraints(
                            minWidth: 18,
                            minHeight: 18,
                          ),
                          child: Text(
                            '${plugNotConfig.length}', // Thay đổi số này thành số thông báo bạn muốn hiển thị
                            style: TextStyle(
                              color: Colors.white,
                              fontSize: 12,
                            ),
                            textAlign: TextAlign.center,
                          ),
                        ),
                      ),
                    ],
                  )
                ],
              ),
              const SizedBox(height: 30),
              Container(
                alignment: Alignment(-1, 1),
                child: Text(
                  "Smart Plug",
                  style: TextStyle(fontSize: 25),
                ),
              ),
              const SizedBox(height: 15),
              Expanded(
                child: GridView.builder(
                  gridDelegate: const SliverGridDelegateWithFixedCrossAxisCount(
                    crossAxisCount: 2,
                    mainAxisSpacing: 14.0, // Khoảng cách giữa các hàng
                    crossAxisSpacing: 8, // Khoảng cách giữa các cột
                    childAspectRatio:
                        1.0, // Tỷ lệ chiều rộng so với chiều cao của mỗi item
                  ),
                  itemCount:
                      mySmartPlugs.length, // Số lượng item trong GridView
                  itemBuilder: (context, int index) {
                    return SmartPlugBox(
                        plugName: mySmartPlugs[index][0],
                        roomName: mySmartPlugs[index][1],
                        deviceId: mySmartPlugs[index][2],
                        initialPowerOn: mySmartPlugs[index][3]);
                  },
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }
}

class SmartPlugBox extends StatefulWidget {
  final String plugName;
  final String iconPath;
  final String roomName;
  final int deviceId;
  final bool initialPowerOn;

  const SmartPlugBox({
    required this.plugName,
    required this.roomName,
    required this.deviceId,
    this.iconPath = 'lib/images/smart-plug.png', // Default value for iconPath
    required this.initialPowerOn,
  });

  @override
  _SmartPlugBoxState createState() => _SmartPlugBoxState();
}

class _SmartPlugBoxState extends State<SmartPlugBox> {
  late bool powerOn;
  bool _isSwitchChanging = false;
  Timer? _debounceTimer;

  @override
  void initState() {
    super.initState();
    powerOn = widget.initialPowerOn;
  }

  @override
  void dispose() {
    _debounceTimer?.cancel(); // Hủy timer trước khi dispose State
    super.dispose();
  }

  void _sentHttp() async {
    try {
      if (widget.deviceId == null || powerOn == null) {
        print('widget.deviceId hoặc powerOn là null.');
        return;
      }

      final response = await http.post(
        Uri.parse(AppConfig.http_url + "/control"),
        headers: {
          'Content-Type': 'application/json', // Thiết lập loại nội dung là JSON
        },
        body: jsonEncode({
          'topic': widget.deviceId.toString(),
          'msg': powerOn.toString(),
        }),
      );

      if (response.statusCode == 200) {
        print("Yêu cầu POST thành công");
      } else {
        print(
            "Yêu cầu POST thất bại với mã trạng thái: ${response.statusCode}");
        // Xử lý lỗi hoặc hiển thị thông báo phù hợp tại đây
      }
    } catch (e) {
      print("Lỗi gửi yêu cầu POST: $e");
      // Xử lý lỗi khi có lỗi kết nối hoặc xử lý khác
    }
  }

  void _onSwitchChanged(bool value) {
    setState(() {
      powerOn = value; // Cập nhật trạng thái khi Switch thay đổi
    });

    if (!_isSwitchChanging) {
      _isSwitchChanging = true;
      _debounceTimer?.cancel(); // Hủy timer hiện tại nếu có

      // Thiết lập timer để gọi _sentHttp() sau khi dừng thay đổi trong 500ms
      _debounceTimer = Timer(Duration(milliseconds: 500), () {
        _sentHttp();
        _isSwitchChanging = false;
      });
    }
  }

  @override
  Widget build(BuildContext context) {
    return GestureDetector(
      onTap: () {
        setState(() {
          powerOn = !powerOn; // Toggle the power state
        });
        _sentHttp();
      },
      child: Container(
        padding: EdgeInsets.all(12),
        decoration: BoxDecoration(
          color: Colors.white,
          borderRadius: BorderRadius.circular(23),
        ),
        child: Row(
          mainAxisAlignment: MainAxisAlignment.spaceBetween,
          children: [
            Column(
              mainAxisAlignment: MainAxisAlignment.start,
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Image.asset(
                  widget.iconPath,
                  width: 40,
                  height: 40,
                ),
                SizedBox(height: 16),
                Text(
                  widget.plugName,
                  style: TextStyle(
                    fontSize: 18,
                    fontWeight: FontWeight.bold,
                  ),
                ),
                SizedBox(height: 5),
                Text(
                  widget.roomName,
                  style: TextStyle(
                    fontSize: 11,
                    fontWeight: FontWeight.bold,
                  ),
                ),
                SizedBox(height: 5),
                Text(
                  'Power: ${powerOn ? "ON" : "OFF"}',
                  style: TextStyle(
                    fontSize: 14,
                    color: powerOn ? Colors.green : Colors.red,
                  ),
                ),
              ],
            ),
            Column(
              children: [
                SizedBox(
                  // width: 15,
                  height: 65,
                ),
                RotatedBox(
                  quarterTurns: 1, // Xoay 90 độ theo chiều kim đồng hồ
                  child: SizedBox(
                    child: Switch(
                      value: powerOn,
                      onChanged: _onSwitchChanged,
                    ),
                  ),
                ),
              ],
            )
          ],
        ),
      ),
    );
  }
}

class CustomDialog extends StatelessWidget {
  final VoidCallback
      onRefreshData; // Tham số nhận hàm không có tham số và không trả giá trị
  final int deviceId; // Thêm tham số deviceId

  // Constructor nhận tham số này
  CustomDialog({required this.onRefreshData, required this.deviceId});

  @override
  Widget build(BuildContext context) {
    // Gọi hàm onRefreshData khi dialog được hiển thị
    WidgetsBinding.instance.addPostFrameCallback((_) {
      onRefreshData(); // Thực thi hàm được truyền từ bên ngoài
    });
    final TextEditingController deviceNameController = TextEditingController();
    final TextEditingController roomNameController = TextEditingController();
    return AlertDialog(
      title: Text('Custom Dialog'),
      content: Column(
        mainAxisSize: MainAxisSize.min,
        children: [
          // Trường nhập văn bản cho device_name
          TextField(
            controller: deviceNameController,
            decoration: InputDecoration(
              hintText: 'Nhập tên thiết bị', // Chữ nền mờ
              border: OutlineInputBorder(),
            ),
          ),
          SizedBox(height: 16), // Khoảng cách giữa hai trường nhập liệu
          // Trường nhập văn bản cho room_name
          TextField(
            controller: roomNameController,
            decoration: InputDecoration(
              hintText: 'Nhập tên phòng', // Chữ nền mờ
              border: OutlineInputBorder(),
            ),
          ),
          SizedBox(height: 16),
          Text('Device ID: $deviceId'), // Hiển thị deviceId nếu cần
        ],
      ),
      actions: [
        Row(
          mainAxisAlignment: MainAxisAlignment.spaceBetween,
          children: [
            TextButton(
              onPressed: () {
                Navigator.of(context).pop(); // Đóng cửa sổ con
              },
              child: Text('Đóng'),
            ),
            TextButton(
              onPressed: () async {
                String deviceName = deviceNameController.text;
                String roomName = roomNameController.text;

                print('Device Name: $deviceName');
                print('Room Name: $roomName');
                print('Device ID: $deviceId'); // In ra deviceId nếu cần

                // Gửi yêu cầu HTTP POST
                try {
                  final response = await http.post(
                    Uri.parse(
                        AppConfig.http_url + "/adddivice"), // Thay đổi URL
                    headers: {
                      'Content-Type': 'application/json',
                    },
                    body: jsonEncode({
                      'device_name': deviceName,
                      'room_name': roomName,
                      'device_id': deviceId,
                    }),
                  );

                  if (response.statusCode == 200) {
                    print('Yêu cầu POST thành công');
                  } else {
                    print(
                        'Yêu cầu POST thất bại với mã trạng thái: ${response.statusCode}');
                    // Xử lý lỗi hoặc hiển thị thông báo phù hợp tại đây
                  }
                } catch (e) {
                  print('Lỗi gửi yêu cầu POST: $e');
                  // Xử lý lỗi khi có lỗi kết nối hoặc xử lý khác
                }

                Navigator.of(context).pop(); // Đóng cửa sổ con
              },
              child: Text('Xác nhận'),
            ),
          ],
        ),
      ],
    );
  }
}
