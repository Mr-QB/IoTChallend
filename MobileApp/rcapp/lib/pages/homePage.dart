// ignore_for_file: prefer_const_constructors, prefer_const_literals_to_create_immutables

import 'package:flutter/material.dart';
import 'package:rcapp/pages/temperature.dart';
import 'dart:async';
import 'dart:core';
import 'plugPage.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';
import 'package:rcapp/config.dart';
import 'scriptPage.dart';

class HomePage extends StatefulWidget {
  const HomePage({Key? key}) : super(key: key);

  @override
  _HomePageState createState() => _HomePageState();
}

class _HomePageState extends State<HomePage> {
  List plugNotConfig = [];
  late Timer _timer;

  @override
  void initState() {
    super.initState();

    // Khởi tạo Timer với khoảng thời gian là 10 giây (10000 milliseconds)
    _timer = Timer.periodic(Duration(seconds: 7), (Timer timer) {
      _refreshData(); // Gọi hàm để fetch dữ liệu từ server
    });
  }

  @override
  void dispose() {
    _timer
        .cancel(); // Hủy Timer khi widget không còn sử dụng để ngừng gọi định kỳ
    super.dispose();
  }

  Future<List<dynamic>> fetchDevices() async {
    print(AppConfig.http_url);
    final response = await http.get(Uri.parse(AppConfig.http_url +
        "/checkdevicesnotconfig")); // Thay đổi URL nếu cần thiết
    if (response.statusCode == 200) {
      return jsonDecode(response.body);
    } else {
      throw Exception('Failed to load data');
    }
  }

  void _refreshData() {
    fetchDevices().then((data) {
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
    }).catchError((error) {
      print('Error: $error');
      // Xử lý lỗi khi gọi API
    });
  }

  @override
  void didChangeDependencies() {
    super.didChangeDependencies();
    _refreshData(); // Gọi lại hàm để tải dữ liệu khi quay lại trang chính
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Colors.indigo.shade50,
      body: SafeArea(
        child: Container(
          margin: const EdgeInsets.only(top: 18, left: 24, right: 24),
          child: Column(
            mainAxisAlignment: MainAxisAlignment.start,
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Row(
                mainAxisAlignment: MainAxisAlignment.spaceBetween,
                children: const [
                  Text(
                    'HI JOHN',
                    style: TextStyle(
                      fontSize: 18,
                      color: Colors.indigo,
                      fontWeight: FontWeight.bold,
                    ),
                  ),
                  RotatedBox(
                    quarterTurns: 135,
                    child: Icon(
                      Icons.bar_chart_rounded,
                      color: Colors.indigo,
                      size: 28,
                    ),
                  )
                ],
              ),
              Expanded(
                child: ListView(
                  physics: const BouncingScrollPhysics(),
                  children: [
                    const SizedBox(height: 32),
                    Center(
                      child: Image.asset(
                        'lib/images/banner.png',
                        scale: 1.2,
                      ),
                    ),
                    const SizedBox(height: 16),
                    const Center(
                      child: Text(
                        'Smart Home',
                        style: TextStyle(
                          fontSize: 32,
                          fontWeight: FontWeight.bold,
                        ),
                      ),
                    ),
                    const SizedBox(height: 48),
                    const Text(
                      'SERVICES',
                      style: TextStyle(
                        fontSize: 14,
                        fontWeight: FontWeight.bold,
                      ),
                    ),
                    const SizedBox(height: 16),
                    Row(
                      mainAxisAlignment: MainAxisAlignment.spaceBetween,
                      children: [
                        _cardMenu(
                            icon: 'lib/images/energy.png',
                            title: 'Plug',
                            notificationCount: plugNotConfig.length,
                            onTap: () {
                              Navigator.push(
                                context,
                                MaterialPageRoute(
                                  builder: (context) => SmartPlug(),
                                ),
                              );
                            }),
                        _cardMenu(
                          onTap: () {
                            Navigator.push(
                              context,
                              MaterialPageRoute(
                                builder: (context) => const TemperaturePage(),
                              ),
                            );
                          },
                          icon: 'lib/images/temperature.png',
                          title: 'TEMPERATURE',
                        ),
                      ],
                    ),
                    const SizedBox(height: 28),
                    Row(
                      mainAxisAlignment: MainAxisAlignment.spaceBetween,
                      children: [
                        _cardMenu(
                          icon: 'lib/images/script.png',
                          title: 'SCRIPT',
                          onTap: () {
                            Navigator.push(
                              context,
                              MaterialPageRoute(
                                builder: (context) => const ScriptsPage(),
                              ),
                            );
                          },
                        ),
                        _cardMenu(
                          icon: 'lib/images/camera.png',
                          title: 'CAMERA',
                          onTap: () {
                            Navigator.push(
                              context,
                              MaterialPageRoute(
                                builder: (context) => const TemperaturePage(),
                              ),
                            );
                          },
                        ),
                      ],
                    ),
                    const SizedBox(height: 28),
                  ],
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }

  Widget _cardMenu({
    required String title,
    required String icon,
    int notificationCount = 0, // Thêm tham số cho số thông báo
    VoidCallback? onTap,
    Color color = Colors.white,
    Color fontColor = Colors.grey,
    double iconWidth = 50.0, // Thêm tham số cho chiều rộng của icon
    double iconHeight = 50.0, // Thêm tham số cho chiều cao của icon
  }) {
    return GestureDetector(
      onTap: onTap,
      child: Container(
        padding: const EdgeInsets.symmetric(
          vertical: 36,
        ),
        width: 150,
        decoration: BoxDecoration(
          color: color,
          borderRadius: BorderRadius.circular(24),
        ),
        child: Column(
          children: [
            Stack(
              children: [
                Image.asset(
                  icon,
                  width: iconWidth,
                  height: iconHeight,
                ),
                if (notificationCount > 0)
                  Positioned(
                    right: 0,
                    top: 0,
                    child: Container(
                      padding: EdgeInsets.all(4),
                      decoration: BoxDecoration(
                        color: Colors.red,
                        shape: BoxShape.circle,
                      ),
                      child: Text(
                        '$notificationCount',
                        style: TextStyle(
                          color: Colors.white,
                          fontSize: 12,
                        ),
                      ),
                    ),
                  ),
              ],
            ),
            const SizedBox(height: 10),
            Text(
              title,
              style: TextStyle(fontWeight: FontWeight.bold, color: fontColor),
            )
          ],
        ),
      ),
    );
  }
}
