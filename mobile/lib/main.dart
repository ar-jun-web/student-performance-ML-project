import 'package:flutter/material.dart';
import 'theme.dart';
import 'services/api_service.dart';
import 'screens/login_screen.dart';
import 'screens/home_screen.dart';

void main() {
  runApp(const AcademyFlowApp());
}

class AcademyFlowApp extends StatelessWidget {
  const AcademyFlowApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'AcademyFlow',
      debugShowCheckedModeBanner: false,
      theme: AppTheme.darkTheme,
      home: const SplashRouter(),
    );
  }
}

/// Checks if user is logged in and routes accordingly
class SplashRouter extends StatefulWidget {
  const SplashRouter({super.key});

  @override
  State<SplashRouter> createState() => _SplashRouterState();
}

class _SplashRouterState extends State<SplashRouter> {
  @override
  void initState() {
    super.initState();
    _checkAuth();
  }

  Future<void> _checkAuth() async {
    // Show splash for at least 1 second
    await Future.delayed(const Duration(milliseconds: 1200));
    try {
      final loggedIn = await ApiService.isLoggedIn();
      if (mounted) {
        Navigator.pushReplacement(
          context,
          MaterialPageRoute(builder: (_) => loggedIn ? const HomeScreen() : const LoginScreen()),
        );
      }
    } catch (_) {
      // If anything fails, go to login
      if (mounted) {
        Navigator.pushReplacement(
          context,
          MaterialPageRoute(builder: (_) => const LoginScreen()),
        );
      }
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: AppTheme.bgDark,
      body: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            const Icon(Icons.track_changes, size: 72, color: AppTheme.primary),
            const SizedBox(height: 16),
            Text('AcademyFlow',
              style: Theme.of(context).textTheme.headlineLarge?.copyWith(
                fontWeight: FontWeight.w800, color: AppTheme.textPrimary,
              ),
            ),
            const SizedBox(height: 8),
            const Text('Student Performance Analytics', style: TextStyle(color: AppTheme.textMuted, fontSize: 14)),
            const SizedBox(height: 30),
            const CircularProgressIndicator(color: AppTheme.primary),
          ],
        ),
      ),
    );
  }
}
