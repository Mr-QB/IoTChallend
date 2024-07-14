import 'package:flutter/material.dart';

class ForgotPasswordPage extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('Quên mật khẩu'),
        backgroundColor: Colors.grey[300],
      ),
      backgroundColor: Colors.grey[300],
      body: Center(
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
              'Bạn quên mật khẩu ?',
              style: TextStyle(fontSize: 24),
            ),
            SizedBox(height: 20),
            Text(
              'Vui lòng nhập địa chỉ email của bạn để thiết lập lại.',
              style: TextStyle(fontSize: 13),
              textAlign: TextAlign.center,
            ),
            SizedBox(height: 20),
            Padding(
              padding: EdgeInsets.symmetric(horizontal: 20),
              child: TextFormField(
                decoration: InputDecoration(
                  labelText: 'Email',
                  border: OutlineInputBorder(),
                ),
              ),
            ),
            SizedBox(height: 20),
            ElevatedButton(
              onPressed: () {
                Navigator.pop(context); // Go back to the previous screen
                ScaffoldMessenger.of(context).showSnackBar(
                  SnackBar(
                    content: Text(
                        'Chức năng này tạm thời không sử dụng được, hãy thử lại sau.'),
                  ),
                );
              },
              child: Text('Đặt lại mật khẩu'),
            ),
          ],
        ),
      ),
    );
  }
}
