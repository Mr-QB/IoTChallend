import 'package:flutter/material.dart';
import 'forgotPasswordPage.dart';
import 'singUpPage.dart';
import 'package:rcapp/config.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';
import 'homePage.dart';

final TextEditingController _username = TextEditingController();
final TextEditingController _password = TextEditingController();

class LoginPage extends StatelessWidget {
  const LoginPage({super.key});

  Future<void> _login(BuildContext context) async {
    String username = _username.text.trim();
    String password = _password.text.trim();

    final response = await http.post(
      Uri.parse(AppConfig.http_url + "/login"),
      headers: {
        'Content-Type': 'application/json',
      },
      body: jsonEncode({
        'username': username,
        'password': password,
      }),
    );

    if (response.statusCode == 200) {
      Navigator.pushReplacement(
        context,
        MaterialPageRoute(builder: (context) => HomePage()),
      );
    } else if (response.statusCode == 401) {
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(
          content: Text('Tài khoản hoặc mật khẩu sai'),
        ),
      );
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Colors.grey[300],
      body: SafeArea(
        child: Center(
          child: SingleChildScrollView(
            padding: EdgeInsets.symmetric(horizontal: 30),
            child: Column(
              mainAxisAlignment: MainAxisAlignment.center,
              crossAxisAlignment: CrossAxisAlignment.stretch,
              children: [
                SizedBox(height: 0),
                // Logo
                Image.asset(
                  "lib/images/logo.png",
                  height: 70,
                  width: 70,
                ),
                SizedBox(height: 20),
                // Welcome back text
                Text(
                  'Chào mừng trở lại!',
                  style: TextStyle(
                    fontSize: 24,
                    fontWeight: FontWeight.bold,
                  ),
                  textAlign: TextAlign.center,
                ),
                SizedBox(height: 20),
                // Username field
                TextFormField(
                  controller: _username,
                  decoration: InputDecoration(
                    labelText: 'Tên đăng nhập',
                    border: OutlineInputBorder(),
                  ),
                ),
                SizedBox(height: 10),
                // Password field
                TextFormField(
                  controller: _password,
                  obscureText: true,
                  decoration: InputDecoration(
                    labelText: 'Mật khẩu',
                    border: OutlineInputBorder(),
                  ),
                ),

                SizedBox(height: 10),
                // Sign in button
                ElevatedButton(
                  onPressed: () => _login(context),
                  child: Text('Đăng nhập'),
                ),
                SizedBox(height: 6),
                // Forgot password text
                Align(
                  alignment: Alignment.centerLeft,
                  child: Padding(
                    padding: const EdgeInsets.only(left: 0.0),
                    child: Row(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        TextButton(
                          onPressed: () {
                            Navigator.push(
                              context,
                              MaterialPageRoute(
                                  builder: (context) => ForgotPasswordPage()),
                            );
                          },
                          child: Text('Quên mật khẩu ?'),
                        ),
                        TextButton(
                          onPressed: () {
                            Navigator.push(
                              context,
                              MaterialPageRoute(
                                  builder: (context) => SignUpPage()),
                            );
                          },
                          child: Text('Đăng ký tài khoản mới.'),
                        ),
                      ],
                    ),
                  ),
                ),
              ],
            ),
          ),
        ),
      ),
    );
  }
}
