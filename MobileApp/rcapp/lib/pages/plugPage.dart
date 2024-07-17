import 'dart:ffi';
import 'dart:async';
import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';
import 'package:rcapp/config.dart';

class SmartPlug extends StatefulWidget {
  const SmartPlug({super.key});

  @override
  State<SmartPlug> createState() => _SmartPlugPageState();
}

class _SmartPlugPageState extends State<SmartPlug> {
  List mySmartPlugs = [];

  Future<List<dynamic>> fetchDevices() async {
    final response = await http.get(Uri.parse(
        AppConfig.http_url + "/getdevices")); // Thay đổi URL nếu cần thiết
    if (response.statusCode == 200) {
      return jsonDecode(response.body);
    } else {
      throw Exception('Failed to load data');
    }
  }

  @override
  void initState() {
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
                  const RotatedBox(
                    quarterTurns: 135,
                    child: Icon(
                      Icons.bar_chart_rounded,
                      color: Colors.indigo,
                      size: 28,
                    ),
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
