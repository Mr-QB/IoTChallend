// ignore_for_file: prefer_const_constructors, prefer_const_literals_to_create_immutables

import 'package:flutter/material.dart';
import 'dart:async';
import 'dart:core';

class HomePage extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    DateTime currentTime = DateTime.now();
    return Scaffold(
      body: SafeArea(
        child: SingleChildScrollView(
          padding: EdgeInsets.all(16.0),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: <Widget>[
              SizedBox(height: 16.0),
              Row(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: <Widget>[
                  // Phần 1 + 2
                  Expanded(
                    flex: 1, // Đặt flex của phần 1 là 1
                    child: Container(
                      padding: EdgeInsets.symmetric(vertical: 16.0),
                      decoration: BoxDecoration(
                        color: Color.fromARGB(224, 67, 123, 180),
                        borderRadius: BorderRadius.circular(12.0),
                      ),
                      child: Column(
                        crossAxisAlignment: CrossAxisAlignment.start,
                        children: <Widget>[
                          Padding(
                            padding: EdgeInsets.symmetric(horizontal: 4.0),
                            child: Text(
                              'Ngôi nhà của Tũn',
                              style: TextStyle(
                                fontSize: 16.0,
                                fontWeight: FontWeight.bold,
                                color: Colors.white,
                              ),
                            ),
                          ),
                          SizedBox(height: 3.0),
                          Padding(
                            padding: EdgeInsets.symmetric(horizontal: 4.0),
                            child: Text(
                              'Cầu giấy, Hà Nội',
                              style: TextStyle(
                                fontSize: 13.0,
                                color: Colors.white,
                              ),
                            ),
                          ),
                          SizedBox(height: 15.0),
                          Padding(
                            padding: EdgeInsets.symmetric(horizontal: 4.0),
                            child: Row(
                              children: <Widget>[
                                Icon(Icons.access_time, color: Colors.white),
                                SizedBox(width: 6.0),
                                Text(
                                  '${currentTime.hour}:${currentTime.minute}',
                                  style: TextStyle(color: Colors.white),
                                ), // Thời gian thực sự sẽ được cập nhật
                                SizedBox(width: 10.0),
                                Text(
                                  ' ${currentTime.day}/${currentTime.month}/${currentTime.year}',
                                  style: TextStyle(color: Colors.white),
                                ),
                              ],
                            ),
                          ),
                          SizedBox(height: 15.0),
                          Padding(
                            padding: EdgeInsets.symmetric(horizontal: 4.0),
                            child: Text(
                              'Nhiệt độ ngoài trời',
                              style: TextStyle(
                                fontSize: 13.0,
                                color: Colors.white,
                              ),
                            ),
                          ),
                          SizedBox(height: 4.0),
                          Padding(
                            padding: EdgeInsets.symmetric(horizontal: 4.0),
                            child: Row(
                              children: <Widget>[
                                Icon(Icons.wb_sunny, color: Colors.white),
                                SizedBox(width: 4.0),
                                Text(
                                  '25°C',
                                  style: TextStyle(color: Colors.white),
                                ), // Nhiệt độ thực sự sẽ được cập nhật
                                SizedBox(width: 8.0),
                                Icon(Icons.opacity, color: Colors.white),
                                SizedBox(width: 4.0),
                                Text(
                                  '70%',
                                  style: TextStyle(color: Colors.white),
                                ), // Độ ẩm thực sự sẽ được cập nhật
                              ],
                            ),
                          ),
                        ],
                      ),
                    ),
                  ),
                  SizedBox(width: 8.0), // Khoảng cách giữa phần 1 và phần 2
                  Expanded(
                    flex: 1, // Đặt flex của phần 2 là 1
                    child: Container(
                      padding: EdgeInsets.all(6.4),
                      decoration: BoxDecoration(
                        color: Color.fromARGB(103, 141, 127, 224),
                        borderRadius: BorderRadius.circular(12.0),
                      ),
                      child: Column(
                        crossAxisAlignment: CrossAxisAlignment.start,
                        children: <Widget>[
                          SizedBox(height: 9.0),
                          Text(
                            'Nhiệt độ trong nhà',
                            style: TextStyle(
                              fontSize: 16.0,
                              fontWeight: FontWeight.bold,
                              color: Colors.white,
                            ),
                          ),
                          SizedBox(height: 10.0),
                          Container(
                            padding: EdgeInsets.symmetric(
                                vertical: 0.0, horizontal: 9.0),
                            decoration: BoxDecoration(
                              shape: BoxShape.rectangle,
                              borderRadius: BorderRadius.circular(20.0),
                              border: Border.all(
                                color: Colors.black87,
                                width: 1.0,
                              ),
                              color: Color.fromARGB(60, 141, 139, 139),
                            ),
                            child: Row(
                              children: [
                                Container(
                                  padding: EdgeInsets.all(
                                      8.0), // Để tạo khoảng cách từ biên của vòng tròn đến biên của Icon
                                  decoration: BoxDecoration(
                                      shape: BoxShape.circle,
                                      border: Border.all(
                                        color: const Color.fromARGB(113, 0, 0,
                                            0), // Màu của đường viền vòng tròn
                                        width:
                                            0.5, // Độ dày của đường viền vòng tròn
                                      ),
                                      color:
                                          Color.fromARGB(139, 141, 139, 139)),
                                  child: Icon(
                                    Icons.wb_sunny,
                                    color: Color.fromARGB(255, 126, 124, 124),
                                    size: 20.0,
                                  ),
                                ),
                                Spacer(),
                                Column(
                                  crossAxisAlignment: CrossAxisAlignment.start,
                                  children: [
                                    Text(
                                      '23°C',
                                      style: TextStyle(
                                          color: Colors.white, fontSize: 20),
                                    ),
                                    Text(
                                      'Nhiệt độ',
                                      style: TextStyle(
                                        color: Colors.white,
                                      ),
                                    )
                                  ],
                                ),
                                Spacer(),
                                SizedBox(),
                              ],
                            ),
                          ),
                          SizedBox(height: 10.0),
                          Container(
                            padding: EdgeInsets.symmetric(
                                vertical: 0.0, horizontal: 12.0),
                            decoration: BoxDecoration(
                                shape: BoxShape.rectangle,
                                borderRadius: BorderRadius.circular(20.0),
                                border: Border.all(
                                  color: Colors.black87,
                                  width: 1.0,
                                ),
                                color: Color.fromARGB(60, 141, 139, 139)),
                            child: Row(
                              // crossAxisAlignment: CrossAxisAlignment.start,
                              children: [
                                Container(
                                  padding: EdgeInsets.all(
                                      8.0), // Để tạo khoảng cách từ biên của vòng tròn đến biên của Icon
                                  decoration: BoxDecoration(
                                      shape: BoxShape.circle,
                                      border: Border.all(
                                        color: const Color.fromARGB(113, 0, 0,
                                            0), // Màu của đường viền vòng tròn
                                        width:
                                            0.5, // Độ dày của đường viền vòng tròn
                                      ),
                                      color:
                                          Color.fromARGB(139, 141, 139, 139)),
                                  child: Icon(
                                    Icons.opacity,
                                    color: Color.fromARGB(255, 126, 124, 124),
                                    size: 20.0,
                                  ),
                                ),

                                Spacer(),
                                Column(
                                  crossAxisAlignment: CrossAxisAlignment.start,
                                  children: [
                                    Text(
                                      '23°C',
                                      style: TextStyle(
                                          color: Colors.white, fontSize: 20),
                                    ),
                                    Text(
                                      'Độ ẩm',
                                      style: TextStyle(color: Colors.white),
                                    ),
                                  ],
                                ),

                                Spacer(),
                                SizedBox(),
                                // Text(
                              ],
                            ),
                          ),
                          SizedBox(height: 10.0),
                        ],
                      ),
                    ),
                  ),
                ],
              ),
              SizedBox(height: 16.0),
              // Phần 3: Danh sách các thiết bị có thể điều khiển
              // Container(
              //   padding: EdgeInsets.all(16.0),
              //   decoration: BoxDecoration(
              //     // color: Colors.grey[200],
              //     borderRadius: BorderRadius.circular(12.0),
              //   ),
              //   child: Column(
              //     crossAxisAlignment: CrossAxisAlignment.start,
              //     children: <Widget>[
              //       Row(
              //         mainAxisAlignment: MainAxisAlignment.spaceBetween,
              //         children: <Widget>[
              //           Text(
              //             'Các thiết bị ',
              //             style: TextStyle(
              //               fontSize: 20.0,
              //               fontWeight: FontWeight.bold,
              //               color: Colors.black,
              //             ),
              //           ),
              //           TextButton(
              //             onPressed: () {
              //               Navigator.push(
              //                 context,
              //                 MaterialPageRoute(
              //                   builder: (context) => DeviceListPage(),
              //                 ),
              //               );
              //             },
              //             child: Text(
              //               'Thêm thiết bị',
              //               style: TextStyle(color: Colors.black),
              //             ),
              //           ),
              //         ],
              //       ),
              //       SizedBox(height: 8.0),
              //       SingleChildScrollView(
              //         scrollDirection: Axis.horizontal,
              //         child: Row(
              //           children: <Widget>[
              //             DeviceControlIcon(
              //                 icon: Icons.lightbulb_outline,
              //                 color: Colors.yellow),
              //             DeviceControlIcon(
              //                 icon: Icons.lock, color: Colors.blue),
              //             DeviceControlIcon(
              //                 icon: Icons.thermostat, color: Colors.red),
              //             DeviceControlIcon(
              //                 icon: Icons.tv, color: Colors.green),
              //             DeviceControlIcon(
              //                 icon: Icons.speaker, color: Colors.orange),
              //           ],
              //         ),
              //       ),
              //     ],
              //   ),
              // ),
              // SizedBox(height: 16.0),

              // Phần 4: Danh sách các phòng trong ngôi nhà
              Container(
                padding: EdgeInsets.all(16.0),
                decoration: BoxDecoration(
                  // color: Colors.grey[200],
                  borderRadius: BorderRadius.circular(12.0),
                ),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: <Widget>[
                    Row(
                      mainAxisAlignment: MainAxisAlignment.spaceBetween,
                      children: <Widget>[
                        Text(
                          'Danh sách phòng',
                          style: TextStyle(
                            fontSize: 20.0,
                            fontWeight: FontWeight.bold,
                            color: Colors.black,
                          ),
                        ),
                        TextButton(
                          onPressed: () {
                            Navigator.push(
                              context,
                              MaterialPageRoute(
                                builder: (context) => RoomListPage(),
                              ),
                            );
                          },
                          child: Text(
                            'Thêm phòng >',
                            style: TextStyle(
                              color: Color.fromARGB(255, 153, 192, 214),
                              decoration: TextDecoration.underline,
                              decorationColor:
                                  Color.fromARGB(255, 153, 192, 214),
                              decorationThickness: 2.5,
                            ),
                          ),
                        ),
                      ],
                    ),
                    SizedBox(height: 8.0),
                    SingleChildScrollView(
                      scrollDirection: Axis.horizontal,
                      child: Row(
                        children: <Widget>[
                          RoomCard(name: 'Phòng khách', color: Colors.orange),
                          RoomCard(name: 'Phòng ngủ', color: Colors.blue),
                          RoomCard(name: 'Phòng bếp', color: Colors.green),
                        ],
                      ),
                    ),
                  ],
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }
}

class DeviceControlIcon extends StatelessWidget {
  final IconData icon;
  final Color color;

  const DeviceControlIcon({Key? key, required this.icon, required this.color})
      : super(key: key);

  @override
  Widget build(BuildContext context) {
    return Container(
      margin: EdgeInsets.symmetric(horizontal: 8.0),
      padding: EdgeInsets.all(12.0),
      decoration: BoxDecoration(
        color: Colors.white,
        borderRadius: BorderRadius.circular(12.0),
        boxShadow: [
          BoxShadow(
            color: Colors.grey.withOpacity(0.5),
            spreadRadius: 1,
            blurRadius: 7,
            offset: Offset(0, 3),
          ),
        ],
      ),
      child: Icon(icon, size: 36.0, color: color),
    );
  }
}

class RoomCard extends StatelessWidget {
  final String name;
  final Color color;

  const RoomCard({Key? key, required this.name, required this.color})
      : super(key: key);

  @override
  Widget build(BuildContext context) {
    return Container(
      margin: EdgeInsets.symmetric(horizontal: 8.0),
      padding: EdgeInsets.all(12.0),
      decoration: BoxDecoration(
        color: color.withOpacity(0.6),
        borderRadius: BorderRadius.circular(12.0),
        boxShadow: [
          BoxShadow(
            color: Colors.grey.withOpacity(0.5),
            spreadRadius: 1,
            blurRadius: 7,
            offset: Offset(0, 3),
          ),
        ],
      ),
      child: Text(
        name,
        style: TextStyle(
          fontSize: 16.0,
          fontWeight: FontWeight.bold,
          color: Colors.white,
        ),
      ),
    );
  }
}

class DeviceListPage extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('Danh sách thiết bị điều khiển'),
        backgroundColor: Colors.blue[900],
      ),
      body: Center(
        child: Text('Đây là trang danh sách thiết bị điều khiển.'),
      ),
    );
  }
}

class RoomListPage extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('Danh sách các phòng trong ngôi nhà'),
        backgroundColor: Colors.blue[900],
      ),
      body: Center(
        child: Text('Đây là trang danh sách các phòng trong ngôi nhà.'),
      ),
    );
  }
}
