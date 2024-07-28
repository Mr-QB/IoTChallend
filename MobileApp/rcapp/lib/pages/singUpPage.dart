import 'package:flutter/material.dart';
import 'package:rcapp/config.dart';
import 'loginPage.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';

class SignUpPage extends StatelessWidget {
  final TextEditingController _username = TextEditingController();
  final TextEditingController _password = TextEditingController();
  final TextEditingController _email = TextEditingController();

  Future<void> _register(BuildContext context) async {
    String username = _username.text.trim();
    String password = _password.text.trim();
    String email = _email.text.trim();

    if (username == "") {
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(
          content: Text('Tên đăng nhập trống, vui lòng cập nhật'),
        ),
      );
    } else if (password == "") {
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(
          content: Text('Mật khẩu trống, vui lòng cập nhật'),
        ),
      );
    } else if (email == "") {
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(
          content: Text('Email trống, vui lòng cập nhật'),
        ),
      );
    } else {
      final response = await http.post(
        Uri.parse(AppConfig.http_url + "/register"),
        headers: {
          'Content-Type': 'application/json',
        },
        body: jsonEncode({
          'username': username,
          'password': password,
          'email': email,
        }),
      );

      if (response.statusCode == 200) {
        Navigator.pop(context);
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(
            content: Text('Đăng ký người dùng mới thành công.'),
          ),
        );
      } else if (response.statusCode == 402) {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(
            content: Text('Tên người dùng đã tồn tại'),
          ),
        );
      } else {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(
            content: Text('Xảy ra lỗi khi đăng ký người dùng mới.'),
          ),
        );
      }
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('Đăng ký mới'),
        backgroundColor: Colors.grey[300],
      ),
      backgroundColor: Colors.grey[300],
      body: Center(
        child: Padding(
          padding: EdgeInsets.all(20.0),
          child: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            children: <Widget>[
              Image.asset(
                "lib/images/logo.png",
                height: 70,
                width: 70,
              ),
              SizedBox(height: 20),
              Text(
                'Vui lòng điền các trường thông tin phía dưới.',
                style: TextStyle(fontSize: 13),
                textAlign: TextAlign.center,
              ),
              SizedBox(height: 12),
              TextFormField(
                controller: _username,
                decoration: InputDecoration(
                  labelText: 'Tên đăng nhập',
                  border: OutlineInputBorder(),
                ),
              ),
              SizedBox(height: 12),
              TextFormField(
                controller: _email,
                decoration: InputDecoration(
                  labelText: 'Địa chỉ email',
                  border: OutlineInputBorder(),
                ),
              ),
              SizedBox(height: 12),
              TextFormField(
                obscureText: true,
                controller: _password,
                decoration: InputDecoration(
                  labelText: 'Mật khẩu',
                  border: OutlineInputBorder(),
                ),
              ),
              SizedBox(height: 12),
              ElevatedButton(
                onPressed: () => _register(context),
                child: Text('Đăng ký'),
              ),
            ],
          ),
        ),
      ),
    );
  }
}
