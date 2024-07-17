import 'package:flutter/material.dart';
import 'package:rcapp/pages/homePage.dart';
import 'pages/loginPage.dart';
import 'pages/plugPage.dart';

void main() {
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return const MaterialApp(
      debugShowCheckedModeBanner: false,
      home: HomePage(),
    );
  }
}
