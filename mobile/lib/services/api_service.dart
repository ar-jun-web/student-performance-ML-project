import 'dart:async';
import 'dart:convert';
import 'package:http/http.dart' as http;
import 'package:shared_preferences/shared_preferences.dart';

class ApiService {
  static const String baseUrl = 'https://academyflow-ml.onrender.com';
  static final _client = http.Client();

  // Helper to handle Render cold starts (up to 60s)
  static Future<http.Response> _post(String path, Map<String, dynamic> body, {Map<String, String>? headers}) async {
    final defaultHeaders = {'Content-Type': 'application/json'};
    if (headers != null) defaultHeaders.addAll(headers);
    return await _client.post(
      Uri.parse('$baseUrl$path'),
      headers: defaultHeaders,
      body: jsonEncode(body),
    ).timeout(const Duration(seconds: 90));
  }

  static Future<http.Response> _get(String path, {Map<String, String>? headers}) async {
    return await _client.get(
      Uri.parse('$baseUrl$path'),
      headers: headers,
    ).timeout(const Duration(seconds: 90));
  }

  // ── Auth ──────────────────────────────────────────────

  static Future<Map<String, dynamic>> signup({
    required String email,
    required String password,
    required String name,
    String? department,
    int? year,
  }) async {
    final response = await _post('/api/auth/signup', {
      'email': email,
      'password': password,
      'name': name,
      'department': department,
      'year': year,
    });
    final data = jsonDecode(response.body);
    if (response.statusCode == 200) {
      await _saveToken(data['access_token'], data['user_id']);
    }
    return data;
  }

  static Future<Map<String, dynamic>> login({
    required String email,
    required String password,
  }) async {
    final response = await _post('/api/auth/login', {
      'email': email,
      'password': password,
    });
    final data = jsonDecode(response.body);
    if (response.statusCode == 200) {
      await _saveToken(data['access_token'], data['user_id']);
    }
    return data;
  }

  static Future<void> logout() async {
    final prefs = await SharedPreferences.getInstance();
    await prefs.remove('access_token');
    await prefs.remove('user_id');
  }

  static Future<bool> isLoggedIn() async {
    final prefs = await SharedPreferences.getInstance();
    return prefs.getString('access_token') != null;
  }

  static Future<void> _saveToken(String? token, dynamic userId) async {
    if (token == null) return;
    final prefs = await SharedPreferences.getInstance();
    await prefs.setString('access_token', token);
    if (userId != null) await prefs.setString('user_id', userId.toString());
  }

  static Future<String?> _getToken() async {
    final prefs = await SharedPreferences.getInstance();
    return prefs.getString('access_token');
  }

  // ── Prediction ────────────────────────────────────────

  static Future<Map<String, dynamic>> predict({
    required int hoursStudied,
    required int previousScores,
    required bool extracurricular,
    required int sleepHours,
    required int samplePapers,
    int? targetScore,
  }) async {
    final token = await _getToken();
    final headers = <String, String>{};
    if (token != null) headers['Authorization'] = 'Bearer $token';

    final response = await _post('/api/predict', {
      'hours_studied': hoursStudied,
      'previous_scores': previousScores,
      'extracurricular': extracurricular,
      'sleep_hours': sleepHours,
      'sample_papers': samplePapers,
      'target_score': targetScore,
    }, headers: headers);
    return jsonDecode(response.body);
  }

  // ── History ───────────────────────────────────────────

  static Future<List<dynamic>> getHistory() async {
    final token = await _getToken();
    if (token == null) return [];
    try {
      final response = await _get('/api/history',
        headers: {'Authorization': 'Bearer $token'},
      );
      if (response.statusCode == 200) {
        return jsonDecode(response.body)['history'] ?? [];
      }
      if (response.statusCode == 401) {
        // Token expired - clear it
        await logout();
      }
      return [];
    } catch (_) {
      return [];
    }
  }

  /// Returns a user-friendly error message from an exception
  static String getErrorMessage(Object error) {
    if (error is TimeoutException) {
      return 'Server is starting up. Please wait 30-60 seconds and try again.';
    }
    return 'Connection error. Check your internet.';
  }
}
