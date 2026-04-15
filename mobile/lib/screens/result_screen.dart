import 'package:flutter/material.dart';
import '../theme.dart';
import '../widgets/glass_card.dart';
import 'predict_screen.dart';

class ResultScreen extends StatelessWidget {
  final Map<String, dynamic> data;
  const ResultScreen({super.key, required this.data});

  Color _gradeColor(String grade) {
    switch (grade) {
      case 'excellent': return AppTheme.success;
      case 'good': return const Color(0xFF3B82F6);
      case 'average': return AppTheme.warning;
      default: return AppTheme.danger;
    }
  }

  IconData _gradeIcon(String grade) {
    switch (grade) {
      case 'excellent': return Icons.emoji_events;
      case 'good': return Icons.star;
      case 'average': return Icons.trending_up;
      default: return Icons.warning_amber;
    }
  }

  @override
  Widget build(BuildContext context) {
    final prediction = data['prediction'] ?? {};
    final score = (prediction['score'] ?? 0).toDouble();
    final grade = prediction['grade'] ?? 'average';
    final status = prediction['status'] ?? '';
    final message = prediction['message'] ?? '';
    final goalAnalysis = data['goal_analysis'];
    final recommendations = data['recommendations'] as List? ?? [];
    final insights = data['insights'] as List? ?? [];
    final peerComparison = data['peer_comparison'] as List? ?? [];
    final color = _gradeColor(grade);

    return Scaffold(
      appBar: AppBar(title: const Text('Results')),
      body: Container(
        decoration: const BoxDecoration(
          gradient: LinearGradient(
            begin: Alignment.topLeft, end: Alignment.bottomRight,
            colors: [AppTheme.bgDark, AppTheme.bgMid, Color(0xFF312E81)],
          ),
        ),
        child: ListView(
          padding: const EdgeInsets.all(16),
          children: [
            // Score Card
            GlassCard(
              borderColor: color.withValues(alpha: 0.5),
              child: Column(
                children: [
                  Icon(_gradeIcon(grade), size: 48, color: color),
                  const SizedBox(height: 8),
                  Text(status, style: TextStyle(fontSize: 18, fontWeight: FontWeight.w800, color: color, letterSpacing: 2)),
                  const SizedBox(height: 4),
                  Text(score.toStringAsFixed(1), style: const TextStyle(fontSize: 48, fontWeight: FontWeight.w900, color: AppTheme.textPrimary)),
                  const Text('/ 100', style: TextStyle(color: AppTheme.textMuted, fontSize: 16)),
                  const SizedBox(height: 8),
                  Text(message, textAlign: TextAlign.center, style: const TextStyle(color: AppTheme.textSecondary)),
                ],
              ),
            ),

            // Goal Analysis
            if (goalAnalysis != null) ...[
              const SizedBox(height: 16),
              GlassCard(
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    const Row(children: [
                      Icon(Icons.flag, size: 20, color: AppTheme.primary),
                      SizedBox(width: 8),
                      Text('Goal Progress', style: TextStyle(fontSize: 16, fontWeight: FontWeight.w700, color: AppTheme.textPrimary)),
                    ]),
                    const SizedBox(height: 12),
                    Row(
                      mainAxisAlignment: MainAxisAlignment.spaceBetween,
                      children: [
                        Text('Current: ${goalAnalysis['current_score']}', style: const TextStyle(color: AppTheme.primary, fontWeight: FontWeight.w700)),
                        Text('Target: ${goalAnalysis['target_score']}', style: const TextStyle(color: AppTheme.secondary, fontWeight: FontWeight.w700)),
                      ],
                    ),
                    const SizedBox(height: 8),
                    ClipRRect(
                      borderRadius: BorderRadius.circular(10),
                      child: LinearProgressIndicator(
                        value: (goalAnalysis['progress_percentage'] ?? 0) / 100,
                        minHeight: 12,
                        backgroundColor: AppTheme.primary.withValues(alpha: 0.2),
                        valueColor: const AlwaysStoppedAnimation(AppTheme.primary),
                      ),
                    ),
                    const SizedBox(height: 6),
                    Text('${goalAnalysis['progress_percentage']}% complete',
                      style: const TextStyle(color: AppTheme.textMuted, fontSize: 13),
                    ),
                    if ((goalAnalysis['gap'] ?? 0) > 0) ...[
                      const SizedBox(height: 8),
                      Text('${goalAnalysis['gap']} points to reach your goal',
                        style: const TextStyle(color: AppTheme.warning, fontWeight: FontWeight.w600),
                      ),
                    ],
                  ],
                ),
              ),
            ],

            // Recommendations
            if (recommendations.isNotEmpty) ...[
              const SizedBox(height: 16),
              const Row(children: [
                Icon(Icons.lightbulb_outline, size: 20, color: AppTheme.primary),
                SizedBox(width: 8),
                Text('Recommendations', style: TextStyle(fontSize: 16, fontWeight: FontWeight.w700, color: AppTheme.textPrimary)),
              ]),
              const SizedBox(height: 8),
              ...recommendations.map((rec) => Padding(
                padding: const EdgeInsets.only(bottom: 8),
                child: GlassCard(
                  padding: const EdgeInsets.all(14),
                  borderColor: AppTheme.primary.withValues(alpha: 0.3),
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      Text(rec['title'] ?? '', style: const TextStyle(fontWeight: FontWeight.w700, color: AppTheme.primary)),
                      const SizedBox(height: 4),
                      Text(rec['description'] ?? '', style: const TextStyle(color: AppTheme.textSecondary, fontSize: 13)),
                    ],
                  ),
                ),
              )),
            ],

            // Peer Comparison
            if (peerComparison.isNotEmpty) ...[
              const SizedBox(height: 16),
              const Row(children: [
                Icon(Icons.people_outline, size: 20, color: AppTheme.primary),
                SizedBox(width: 8),
                Text('Peer Comparison', style: TextStyle(fontSize: 16, fontWeight: FontWeight.w700, color: AppTheme.textPrimary)),
              ]),
              const SizedBox(height: 8),
              ...peerComparison.map((comp) {
                final diff = (comp['difference'] ?? 0).toDouble();
                final isStrength = comp['is_strength'] == true;
                return Padding(
                  padding: const EdgeInsets.only(bottom: 6),
                  child: GlassCard(
                    padding: const EdgeInsets.all(12),
                    borderColor: isStrength ? AppTheme.success.withValues(alpha: 0.3) : AppTheme.cardBorder,
                    child: Row(
                      children: [
                        Expanded(
                          child: Text(comp['category'] ?? '', style: const TextStyle(color: AppTheme.textSecondary, fontWeight: FontWeight.w600)),
                        ),
                        Text('You: ${(comp['student_score'] ?? 0).toStringAsFixed(0)}%', style: const TextStyle(color: AppTheme.primary, fontWeight: FontWeight.w700, fontSize: 13)),
                        const SizedBox(width: 10),
                        Text('Avg: ${comp['class_average'] ?? 0}%', style: const TextStyle(color: AppTheme.textMuted, fontSize: 13)),
                        const SizedBox(width: 6),
                        Icon(diff >= 0 ? Icons.arrow_upward : Icons.arrow_downward,
                          color: diff >= 0 ? AppTheme.success : AppTheme.warning, size: 16),
                      ],
                    ),
                  ),
                );
              }),
            ],

            // Insights
            if (insights.isNotEmpty) ...[
              const SizedBox(height: 16),
              const Row(children: [
                Icon(Icons.insights, size: 20, color: AppTheme.primary),
                SizedBox(width: 8),
                Text('Study Insights', style: TextStyle(fontSize: 16, fontWeight: FontWeight.w700, color: AppTheme.textPrimary)),
              ]),
              const SizedBox(height: 8),
              ...insights.map((ins) {
                final level = ins['level'] ?? 'info';
                final insColor = level == 'success' ? AppTheme.success : level == 'warning' ? AppTheme.warning : const Color(0xFF3B82F6);
                return Padding(
                  padding: const EdgeInsets.only(bottom: 8),
                  child: GlassCard(
                    padding: const EdgeInsets.all(14),
                    borderColor: insColor.withValues(alpha: 0.4),
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        Text(ins['title'] ?? '', style: TextStyle(fontWeight: FontWeight.w700, color: insColor)),
                        const SizedBox(height: 4),
                        Text(ins['description'] ?? '', style: const TextStyle(color: AppTheme.textSecondary, fontSize: 13)),
                      ],
                    ),
                  ),
                );
              }),
            ],

            // Action Buttons
            const SizedBox(height: 24),
            Row(
              children: [
                Expanded(
                  child: SizedBox(
                    height: 50,
                    child: OutlinedButton.icon(
                      onPressed: () => Navigator.pop(context),
                      icon: const Icon(Icons.home, size: 20),
                      label: const Text('Home'),
                      style: OutlinedButton.styleFrom(
                        foregroundColor: AppTheme.textPrimary,
                        side: const BorderSide(color: AppTheme.cardBorder),
                        shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(14)),
                      ),
                    ),
                  ),
                ),
                const SizedBox(width: 12),
                Expanded(
                  child: SizedBox(
                    height: 50,
                    child: ElevatedButton.icon(
                      onPressed: () => Navigator.pushReplacement(context, MaterialPageRoute(builder: (_) => const PredictScreen())),
                      icon: const Icon(Icons.refresh, size: 20),
                      label: const Text('Try Again'),
                      style: ElevatedButton.styleFrom(
                        backgroundColor: AppTheme.primary,
                        shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(14)),
                      ),
                    ),
                  ),
                ),
              ],
            ),
            const SizedBox(height: 20),
          ],
        ),
      ),
    );
  }
}
