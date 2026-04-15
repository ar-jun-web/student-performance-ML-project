import 'package:flutter/material.dart';
import '../services/api_service.dart';
import '../theme.dart';
import '../widgets/glass_card.dart';
import 'predict_screen.dart';
import 'history_screen.dart';
import 'login_screen.dart';

class HomeScreen extends StatelessWidget {
  const HomeScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Container(
        decoration: const BoxDecoration(
          gradient: LinearGradient(
            begin: Alignment.topLeft, end: Alignment.bottomRight,
            colors: [AppTheme.bgDark, AppTheme.bgMid, Color(0xFF312E81)],
          ),
        ),
        child: SafeArea(
          child: Padding(
            padding: const EdgeInsets.all(20),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                // Header
                Row(
                  mainAxisAlignment: MainAxisAlignment.spaceBetween,
                  children: [
                    Expanded(
                      child: Column(
                        crossAxisAlignment: CrossAxisAlignment.start,
                        children: [
                          Text('AcademyFlow',
                            style: Theme.of(context).textTheme.headlineSmall?.copyWith(
                              fontWeight: FontWeight.w800, color: AppTheme.textPrimary,
                            ),
                          ),
                          const Text('Student Performance Analytics', style: TextStyle(color: AppTheme.textMuted, fontSize: 13)),
                        ],
                      ),
                    ),
                    IconButton(
                      icon: const Icon(Icons.logout, color: AppTheme.textMuted),
                      onPressed: () async {
                        final confirm = await showDialog<bool>(
                          context: context,
                          builder: (ctx) => AlertDialog(
                            backgroundColor: AppTheme.bgMid,
                            title: const Text('Logout', style: TextStyle(color: AppTheme.textPrimary)),
                            content: const Text('Are you sure you want to logout?', style: TextStyle(color: AppTheme.textSecondary)),
                            actions: [
                              TextButton(onPressed: () => Navigator.pop(ctx, false), child: const Text('Cancel')),
                              TextButton(onPressed: () => Navigator.pop(ctx, true), child: const Text('Logout', style: TextStyle(color: AppTheme.danger))),
                            ],
                          ),
                        );
                        if (confirm == true) {
                          await ApiService.logout();
                          if (context.mounted) {
                            Navigator.pushReplacement(context, MaterialPageRoute(builder: (_) => const LoginScreen()));
                          }
                        }
                      },
                    ),
                  ],
                ),
                const SizedBox(height: 30),

                // Hero Card
                GlassCard(
                  borderColor: AppTheme.primary.withValues(alpha: 0.3),
                  child: Column(
                    children: [
                      const Icon(Icons.track_changes, size: 48, color: AppTheme.primary),
                      const SizedBox(height: 10),
                      const Text('Predict Your Performance',
                        style: TextStyle(fontSize: 20, fontWeight: FontWeight.w800, color: AppTheme.textPrimary),
                      ),
                      const SizedBox(height: 8),
                      const Text(
                        'Enter your study habits and get AI-powered predictions with personalized recommendations.',
                        textAlign: TextAlign.center,
                        style: TextStyle(color: AppTheme.textSecondary, fontSize: 14),
                      ),
                      const SizedBox(height: 20),
                      SizedBox(
                        width: double.infinity,
                        height: 50,
                        child: ElevatedButton.icon(
                          onPressed: () => Navigator.push(context, MaterialPageRoute(builder: (_) => const PredictScreen())),
                          icon: const Icon(Icons.auto_awesome, size: 20),
                          label: const Text('Start Prediction'),
                          style: ElevatedButton.styleFrom(
                            backgroundColor: AppTheme.primary,
                            shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(14)),
                          ),
                        ),
                      ),
                    ],
                  ),
                ),
                const SizedBox(height: 20),

                // Quick Features
                const Text('Quick Features', style: TextStyle(fontSize: 16, fontWeight: FontWeight.w700, color: AppTheme.textPrimary)),
                const SizedBox(height: 12),
                Expanded(
                  child: GridView.count(
                    crossAxisCount: 2,
                    mainAxisSpacing: 12,
                    crossAxisSpacing: 12,
                    childAspectRatio: 1.3,
                    children: [
                      _FeatureCard(icon: Icons.analytics_outlined, title: 'Performance\nAnalysis', color: AppTheme.primary,
                        onTap: () => Navigator.push(context, MaterialPageRoute(builder: (_) => const PredictScreen()))),
                      _FeatureCard(icon: Icons.flag_outlined, title: 'Goal\nTracker', color: AppTheme.secondary,
                        onTap: () => Navigator.push(context, MaterialPageRoute(builder: (_) => const PredictScreen()))),
                      _FeatureCard(icon: Icons.people_outlined, title: 'Peer\nComparison', color: AppTheme.success,
                        onTap: () => Navigator.push(context, MaterialPageRoute(builder: (_) => const PredictScreen()))),
                      _FeatureCard(icon: Icons.history_outlined, title: 'Prediction\nHistory', color: AppTheme.warning,
                        onTap: () => Navigator.push(context, MaterialPageRoute(builder: (_) => const HistoryScreen()))),
                    ],
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

class _FeatureCard extends StatelessWidget {
  final IconData icon;
  final String title;
  final Color color;
  final VoidCallback onTap;
  const _FeatureCard({required this.icon, required this.title, required this.color, required this.onTap});

  @override
  Widget build(BuildContext context) {
    return GestureDetector(
      onTap: onTap,
      child: GlassCard(
        borderColor: color.withValues(alpha: 0.3),
        padding: const EdgeInsets.all(16),
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            Icon(icon, size: 32, color: color),
            const SizedBox(height: 8),
            Text(title, textAlign: TextAlign.center,
              style: TextStyle(color: color, fontWeight: FontWeight.w700, fontSize: 13)),
          ],
        ),
      ),
    );
  }
}
