import 'dart:async';
import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';
import 'package:rcapp/config.dart';

class ScriptsPage extends StatefulWidget {
  const ScriptsPage({super.key});

  @override
  State<ScriptsPage> createState() => _ScriptsPageState();
}

class _ScriptsPageState extends State<ScriptsPage> {
  List<List<dynamic>> mySmartPlugs = [];
  List<List<dynamic>> mySensors = [];

  @override
  void initState() {
    super.initState();
    _fetchDevices();
    _fetchSensors();
  }

  Future<void> _fetchDevices() async {
    try {
      final response =
          await http.get(Uri.parse(AppConfig.http_url + "/getdevices"));
      if (response.statusCode == 200) {
        List<dynamic> data = jsonDecode(response.body);
        List<List<dynamic>> nestedList = [];
        for (var item in data) {
          String deviceName = item['device_name'] ?? '';
          String roomName = item['room_name'] ?? '';
          bool status = item['status'] == 1;
          int deviceId = item['id'] ?? 0;

          List<dynamic> subList = [deviceName, roomName, deviceId, status];
          nestedList.add(subList);
        }
        setState(() {
          mySmartPlugs = nestedList;
        });
      } else {
        throw Exception('Failed to load data');
      }
    } catch (error) {
      print('Error: $error');
    }
  }

  Future<void> _fetchSensors() async {
    try {
      final response =
          await http.get(Uri.parse(AppConfig.http_url + "/getsensors"));
      if (response.statusCode == 200) {
        List<dynamic> data = jsonDecode(response.body);
        List<List<dynamic>> nestedList = [];
        for (var item in data) {
          String sensorName = item['device_name'] ?? '';
          String sensorType = item['type'] ?? '';
          bool status = item['status'] == 1;
          int sensorId = item['id'] ?? 0;

          List<dynamic> subList = [sensorName, sensorType, sensorId, status];
          nestedList.add(subList);
        }
        setState(() {
          mySensors = nestedList;
          print(mySensors);
        });
      } else {
        throw Exception('Failed to load data');
      }
    } catch (error) {
      print('Error: $error');
    }
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
                  GestureDetector(
                    onTap: () {
                      CustomDialog.show(context, mySmartPlugs, mySensors);
                    },
                    child: RotatedBox(
                      quarterTurns: 2,
                      child: Image.asset(
                        "lib/images/save.png",
                        height: 40,
                        width: 40,
                      ),
                    ),
                  )
                ],
              ),
              const SizedBox(height: 30),
              Container(
                alignment: Alignment(-1, 1),
                child: Text(
                  "Automated scripts",
                  style: TextStyle(fontSize: 20, fontWeight: FontWeight.bold),
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
                    return ScriptBoxs(
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

class ScriptBoxs extends StatefulWidget {
  final String plugName;
  final String iconPath;
  final String roomName;
  final int deviceId;
  final bool initialPowerOn;

  const ScriptBoxs({
    required this.plugName,
    required this.roomName,
    required this.deviceId,
    this.iconPath = 'lib/images/smart-plug.png', // Default value for iconPath
    required this.initialPowerOn,
  });

  @override
  _ScriptBoxs createState() => _ScriptBoxs();
}

class _ScriptBoxs extends State<ScriptBoxs> {
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
      }
    } catch (e) {
      print("Lỗi gửi yêu cầu POST: $e");
    }
  }

  void _onSwitchChanged(bool value) {
    setState(() {
      powerOn = value;
    });

    if (!_isSwitchChanging) {
      _isSwitchChanging = true;
      _debounceTimer?.cancel();

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
          powerOn = !powerOn;
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
                  height: 65,
                ),
                RotatedBox(
                  quarterTurns: 1,
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

class CustomDialog {
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

  static void show(BuildContext context, List<List<dynamic>> mySmartPlugs,
      List<List<dynamic>> mySensors) {
    showDialog(
      context: context,
      builder: (BuildContext context) {
        String selectedOption = 'Timer';
        List<Map<String, dynamic>> rows = [];

        return StatefulBuilder(
          builder: (BuildContext context, StateSetter setState) {
            return AlertDialog(
              title: Text(
                "Add new automated scripts",
                style: TextStyle(fontSize: 17, fontWeight: FontWeight.bold),
              ),
              content: _buildDialogContent(
                  rows, context, setState, mySmartPlugs, mySensors),
              actions: _buildDialogActions(
                selectedOption,
                rows,
                setState,
                context,
                (String newValue) {
                  setState(() {
                    selectedOption = newValue;
                  });
                },
              ),
            );
          },
        );
      },
    );
  }

  static Future<void> _sendJsonData(List<Map<String, dynamic>> rows) async {
    final String url = AppConfig.http_url + "/createscipts";
    final Map<String, String> headers = {
      'Content-Type': 'application/json',
    };

    final String jsonString = jsonEncode(rows);

    try {
      final response = await http.post(
        Uri.parse(url),
        headers: headers,
        body: jsonString,
      );

      if (response.statusCode == 200) {
        print('Dữ liệu đã được gửi thành công.');
      } else {
        print('Lỗi khi gửi dữ liệu: ${response.statusCode}');
      }
    } catch (e) {
      print('Lỗi khi gửi HTTP request: $e');
    }
  }

  static Widget _buildDialogContent(
      List<Map<String, dynamic>> rows,
      BuildContext context,
      StateSetter setState,
      List<List<dynamic>> mySmartPlugs,
      List<List<dynamic>> mySensors) {
    return SingleChildScrollView(
      child: Column(
        mainAxisSize: MainAxisSize.min,
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Text("This is a custom dialog"),
          SizedBox(height: 16),
          // Hiển thị các hàng đã thêm
          ...rows.map((row) {
            try {
              return _buildRow(row, setState, context, mySmartPlugs, mySensors);
            } catch (e) {
              print("Error building row: $e");
              return SizedBox.shrink();
            }
          }).toList(),
          SizedBox(height: 16),
        ],
      ),
    );
  }

  static Widget _buildRow(
      Map<String, dynamic> row,
      StateSetter setState,
      BuildContext context,
      List<List<dynamic>> mySmartPlugs,
      List<List<dynamic>> mySensors) {
    List<String> deviceNames =
        mySmartPlugs.map((plug) => plug[0].toString()).toSet().toList();
    List<String> sensorNames =
        mySensors.map((sensor) => sensor[0].toString()).toSet().toList();
    if (row['type'] == 'Timer') {
      return Row(
        children: [
          Expanded(
            child: DropdownButton<String>(
              value: deviceNames.contains(row['deviceName'])
                  ? row['deviceName']
                  : null,
              isExpanded: true,
              items: deviceNames.map((deviceName) {
                return DropdownMenuItem<String>(
                  value: deviceName,
                  child: Text(
                    deviceName,
                    overflow: TextOverflow.ellipsis,
                    maxLines: 1,
                  ),
                );
              }).toList(),
              onChanged: (String? newValue) {
                setState(() {
                  row['deviceName'] = newValue;
                });
              },
            ),
          ),
          SizedBox(width: 8),
          Expanded(
            child: DropdownButton<String>(
              value: row['status'],
              isExpanded: true,
              items: <String>['ON', 'OFF'].map((String value) {
                return DropdownMenuItem<String>(
                  value: value,
                  child: Text(
                    value,
                    overflow: TextOverflow.ellipsis,
                    maxLines: 1,
                  ),
                );
              }).toList(),
              onChanged: (String? newValue) {
                setState(() {
                  row['status'] = newValue;
                });
              },
            ),
          ),
          SizedBox(width: 8),
          Expanded(
            child: TextButton(
              onPressed: () async {
                TimeOfDay? pickedTime = await showTimePicker(
                  context: context,
                  initialTime: TimeOfDay.now(),
                );
                if (pickedTime != null) {
                  setState(() {
                    row['timer'] =
                        '${pickedTime.hour}:${pickedTime.minute}'; // Chuyển đổi thành chuỗi
                  });
                }
              },
              child: Text(
                row['timer'] == null
                    ? "Select Time"
                    : row['timer']!, // Hiển thị chuỗi thời gian
              ),
            ),
          ),
        ],
      );
    } else if (row['type'] == 'Sensor') {
      return Row(
        children: [
          Expanded(
            child: DropdownButton<String>(
              value: sensorNames.contains(row['sensorName'])
                  ? row['sensorName']
                  : null,
              isExpanded: true,
              items: sensorNames.map((sensorName) {
                return DropdownMenuItem<String>(
                  value: sensorName,
                  child: Text(
                    sensorName,
                    overflow: TextOverflow.ellipsis,
                    maxLines: 1,
                  ),
                );
              }).toList(),
              onChanged: (String? newValue) {
                setState(() {
                  row['sensorName'] = newValue;
                });
              },
            ),
          ),
          SizedBox(width: 8),
          Expanded(
            child: DropdownButton<String>(
              value: row['sensorStatus'],
              isExpanded: true,
              items: <String>['TRUE', 'FALSE'].map((String value) {
                return DropdownMenuItem<String>(
                  value: value,
                  child: Text(
                    value,
                    overflow: TextOverflow.ellipsis,
                    maxLines: 1,
                  ),
                );
              }).toList(),
              onChanged: (String? newValue) {
                setState(() {
                  row['sensorStatus'] = newValue;
                });
              },
            ),
          ),
          SizedBox(width: 8),
          Expanded(
            child: DropdownButton<String>(
              value: deviceNames.contains(row['deviceName'])
                  ? row['deviceName']
                  : null,
              isExpanded: true,
              items: deviceNames.map((deviceName) {
                return DropdownMenuItem<String>(
                  value: deviceName,
                  child: Text(
                    deviceName,
                    overflow: TextOverflow.ellipsis,
                    maxLines: 1,
                  ),
                );
              }).toList(),
              onChanged: (String? newValue) {
                setState(() {
                  row['deviceName'] = newValue;
                });
              },
            ),
          ),
          SizedBox(width: 8),
          Expanded(
            child: DropdownButton<String>(
              value: row['deviceStatus'],
              isExpanded: true,
              items: <String>['ON', 'OFF'].map((String value) {
                return DropdownMenuItem<String>(
                  value: value,
                  child: Text(
                    value,
                    overflow: TextOverflow.ellipsis,
                    maxLines: 1,
                  ),
                );
              }).toList(),
              onChanged: (String? newValue) {
                setState(() {
                  row['deviceStatus'] = newValue;
                });
              },
            ),
          ),
        ],
      );
    } else {
      return SizedBox.shrink();
    }
  }

  static List<Widget> _buildDialogActions(
    String selectedOption,
    List<Map<String, dynamic>> rows,
    StateSetter setState,
    BuildContext context,
    ValueChanged<String> onOptionChanged,
  ) {
    return [
      Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Row(
            children: [
              Expanded(
                child: DropdownButton<String>(
                  value: selectedOption,
                  isExpanded: true,
                  items: <String>['Timer', 'Sensor'].map((String value) {
                    return DropdownMenuItem<String>(
                      value: value,
                      child: ConstrainedBox(
                        constraints: BoxConstraints(
                          maxWidth: 120,
                        ),
                        child: Text(
                          value,
                          overflow: TextOverflow.ellipsis,
                          maxLines: 1,
                        ),
                      ),
                    );
                  }).toList(),
                  onChanged: (String? newValue) {
                    if (newValue != null) {
                      onOptionChanged(newValue);
                    }
                  },
                ),
              ),
              SizedBox(width: 8),
              TextButton(
                onPressed: () {
                  setState(() {
                    if (selectedOption == 'Timer') {
                      rows.add({
                        'type': 'Timer',
                        'deviceName': 'Random1',
                        'status': 'ON',
                        'timer': null,
                      });
                    } else if (selectedOption == 'Sensor') {
                      rows.add({
                        'type': 'Sensor',
                        'sensorName': 'Option1',
                        'sensorStatus': 'TRUE',
                        'deviceName': 'OptionA',
                        'deviceStatus': 'ON',
                      });
                    }
                  });
                },
                child: Text("Add"),
              ),
              SizedBox(width: 8),
              TextButton(
                onPressed: () {
                  Navigator.of(context).pop();
                },
                child: Text("Close"),
              ),
            ],
          ),
        ],
      ),
      Row(
        children: [
          Spacer(),
          TextButton(
            onPressed: () {
              CustomDialog._sendJsonData(rows);
              // String jsonString = jsonEncode(rows);
              // print('JSON data: $jsonString');

              // Đóng dialog sau khi in dữ liệu
              Navigator.of(context).pop();
            },
            child: Text(
              "Done",
              style: TextStyle(color: Colors.white),
            ),
            style: TextButton.styleFrom(
              backgroundColor: Colors.indigo,
            ),
          ),
        ],
      ),
    ];
  }
}
