import 'package:flutter/material.dart';
import '../services/api_service.dart';
import '../theme.dart';
import 'home_screen.dart';

class SignupScreen extends StatefulWidget {
  const SignupScreen({super.key});

  @override
  State<SignupScreen> createState() => _SignupScreenState();
}

class _SignupScreenState extends State<SignupScreen> {
  final _nameController = TextEditingController();
  final _emailController = TextEditingController();
  final _passwordController = TextEditingController();
  final _confirmPasswordController = TextEditingController();
  final _deptController = TextEditingController();
  int _year = 1;
  bool _loading = false;
  String? _error;

  @override
  void dispose() {
    _nameController.dispose();
    _emailController.dispose();
    _passwordController.dispose();
    _confirmPasswordController.dispose();
    _deptController.dispose();
    super.dispose();
  }

  Future<void> _signup() async {
    // Input validation
    final name = _nameController.text.trim();
    final email = _emailController.text.trim();
    final password = _passwordController.text;
    final confirmPassword = _confirmPasswordController.text;

    if (name.isEmpty || email.isEmpty || password.isEmpty) {
      setState(() => _error = 'Please fill in all required fields.');
      return;
    }
    if (!email.contains('@') || !email.contains('.')) {
      setState(() => _error = 'Please enter a valid email address.');
      return;
    }
    if (password.length < 6) {
      setState(() => _error = 'Password must be at least 6 characters.');
      return;
    }
    if (password != confirmPassword) {
      setState(() => _error = 'Passwords do not match.');
      return;
    }

    setState(() { _loading = true; _error = null; });
    try {
      final result = await ApiService.signup(
        email: email,
        password: password,
        name: name,
        department: _deptController.text.trim().isEmpty ? null : _deptController.text.trim(),
        year: _year,
      );
      if (!mounted) return;
      if (result['access_token'] != null) {
        Navigator.pushReplacement(context, MaterialPageRoute(builder: (_) => const HomeScreen()));
      } else {
        setState(() => _error = result['detail'] ?? result['message'] ?? 'Signup failed');
      }
    } catch (e) {
      if (!mounted) return;
      setState(() => _error = ApiService.getErrorMessage(e));
    }
    if (mounted) setState(() => _loading = false);
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Container(
        decoration: const BoxDecoration(
          gradient: LinearGradient(
            begin: Alignment.topLeft,
            end: Alignment.bottomRight,
            colors: [AppTheme.bgDark, AppTheme.bgMid, Color(0xFF312E81)],
          ),
        ),
        child: SafeArea(
          child: Center(
            child: SingleChildScrollView(
              padding: const EdgeInsets.all(24),
              child: Column(
                children: [
                  Text('Create Account',
                    style: Theme.of(context).textTheme.headlineMedium?.copyWith(
                      fontWeight: FontWeight.w800, color: AppTheme.textPrimary,
                    ),
                  ),
                  const SizedBox(height: 8),
                  const Text('Join AcademyFlow', style: TextStyle(color: AppTheme.textMuted)),
                  const SizedBox(height: 32),
                  TextField(
                    controller: _nameController,
                    style: const TextStyle(color: AppTheme.textPrimary),
                    decoration: const InputDecoration(
                      labelText: 'Full Name *',
                      prefixIcon: Icon(Icons.person_outlined, color: AppTheme.primary),
                    ),
                  ),
                  const SizedBox(height: 14),
                  TextField(
                    controller: _emailController,
                    keyboardType: TextInputType.emailAddress,
                    style: const TextStyle(color: AppTheme.textPrimary),
                    decoration: const InputDecoration(
                      labelText: 'Email *',
                      prefixIcon: Icon(Icons.email_outlined, color: AppTheme.primary),
                    ),
                  ),
                  const SizedBox(height: 14),
                  TextField(
                    controller: _passwordController,
                    obscureText: true,
                    style: const TextStyle(color: AppTheme.textPrimary),
                    decoration: const InputDecoration(
                      labelText: 'Password * (min 6 chars)',
                      prefixIcon: Icon(Icons.lock_outlined, color: AppTheme.primary),
                    ),
                  ),
                  const SizedBox(height: 14),
                  TextField(
                    controller: _confirmPasswordController,
                    obscureText: true,
                    style: const TextStyle(color: AppTheme.textPrimary),
                    decoration: const InputDecoration(
                      labelText: 'Confirm Password *',
                      prefixIcon: Icon(Icons.lock_outlined, color: AppTheme.primary),
                    ),
                  ),
                  const SizedBox(height: 14),
                  TextField(
                    controller: _deptController,
                    style: const TextStyle(color: AppTheme.textPrimary),
                    decoration: const InputDecoration(
                      labelText: 'Department (optional)',
                      prefixIcon: Icon(Icons.school_outlined, color: AppTheme.primary),
                    ),
                  ),
                  const SizedBox(height: 14),
                  DropdownButtonFormField<int>(
                    value: _year,
                    dropdownColor: AppTheme.bgMid,
                    style: const TextStyle(color: AppTheme.textPrimary),
                    decoration: const InputDecoration(
                      labelText: 'Year',
                      prefixIcon: Icon(Icons.calendar_today, color: AppTheme.primary),
                    ),
                    items: [1, 2, 3, 4].map((y) => DropdownMenuItem(value: y, child: Text('Year $y'))).toList(),
                    onChanged: (v) => setState(() => _year = v ?? 1),
                  ),
                  if (_error != null) ...[
                    const SizedBox(height: 12),
                    Text(_error!, style: const TextStyle(color: AppTheme.danger, fontSize: 13)),
                  ],
                  const SizedBox(height: 24),
                  SizedBox(
                    width: double.infinity,
                    child: ElevatedButton(
                      onPressed: _loading ? null : _signup,
                      child: _loading
                          ? const SizedBox(height: 20, width: 20, child: CircularProgressIndicator(strokeWidth: 2, color: Colors.white))
                          : const Text('Sign Up'),
                    ),
                  ),
                  const SizedBox(height: 16),
                  TextButton(
                    onPressed: () => Navigator.pop(context),
                    child: const Text('Already have an account? Login', style: TextStyle(color: AppTheme.primary)),
                  ),
                ],
              ),
            ),
          ),
        ),
      ),
    );
  }
}
