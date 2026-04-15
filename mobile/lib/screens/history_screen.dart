import 'package:flutter/material.dart';
import '../services/api_service.dart';
import '../theme.dart';
import '../widgets/glass_card.dart';

class HistoryScreen extends StatefulWidget {
  const HistoryScreen({super.key});

  @override
  State<HistoryScreen> createState() => _HistoryScreenState();
}

class _HistoryScreenState extends State<HistoryScreen> {
  List<dynamic> _history = [];
  bool _loading = true;

  @override
  void initState() {
    super.initState();
    _loadHistory();
  }

  Future<void> _loadHistory() async {
    setState(() => _loading = true);
    final history = await ApiService.getHistory();
    if (mounted) {
      setState(() {
        _history = history;
        _loading = false;
      });
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Prediction History')),
      body: Container(
        decoration: const BoxDecoration(
          gradient: LinearGradient(
            begin: Alignment.topLeft, end: Alignment.bottomRight,
            colors: [AppTheme.bgDark, AppTheme.bgMid, Color(0xFF312E81)],
          ),
        ),
        child: _loading
            ? const Center(child: CircularProgressIndicator(color: AppTheme.primary))
            : _history.isEmpty
                ? Center(
                    child: Column(
                      mainAxisAlignment: MainAxisAlignment.center,
                      children: [
                        const Icon(Icons.history, size: 64, color: AppTheme.textMuted),
                        const SizedBox(height: 16),
                        const Text('No predictions yet', style: TextStyle(color: AppTheme.textMuted, fontSize: 16)),
                        const SizedBox(height: 8),
                        const Text('Make your first prediction to see it here!', style: TextStyle(color: AppTheme.textMuted, fontSize: 13)),
                      ],
                    ),
                  )
                : RefreshIndicator(
                    onRefresh: _loadHistory,
                    color: AppTheme.primary,
                    child: ListView.builder(
                      padding: const EdgeInsets.all(16),
                      itemCount: _history.length,
                      itemBuilder: (context, index) {
                        final item = _history[index];
                        final score = (item['predicted_score'] ?? 0).toDouble();
                        final date = item['created_at'] ?? '';
                        final inputs = item['input_data'] ?? {};
                        return Padding(
                          padding: const EdgeInsets.only(bottom: 10),
                          child: GlassCard(
                            padding: const EdgeInsets.all(16),
                            child: Row(
                              children: [
                                Container(
                                  width: 56, height: 56,
                                  decoration: BoxDecoration(
                                    color: AppTheme.primary.withValues(alpha: 0.2),
                                    borderRadius: BorderRadius.circular(14),
                                  ),
                                  child: Center(
                                    child: Text(score.toStringAsFixed(0),
                                      style: const TextStyle(color: AppTheme.primary, fontWeight: FontWeight.w800, fontSize: 20)),
                                  ),
                                ),
                                const SizedBox(width: 14),
                                Expanded(
                                  child: Column(
                                    crossAxisAlignment: CrossAxisAlignment.start,
                                    children: [
                                      Text('Score: ${score.toStringAsFixed(1)} / 100',
                                        style: const TextStyle(color: AppTheme.textPrimary, fontWeight: FontWeight.w700)),
                                      const SizedBox(height: 4),
                                      Text('${inputs['hours_studied'] ?? '-'}h study  |  ${inputs['sleep_hours'] ?? '-'}h sleep  |  ${inputs['previous_scores'] ?? '-'}% prev',
                                        style: const TextStyle(color: AppTheme.textMuted, fontSize: 12)),
                                      if (date.isNotEmpty) ...[
                                        const SizedBox(height: 2),
                                        Text(date.length > 10 ? date.substring(0, 10) : date,
                                          style: const TextStyle(color: AppTheme.textMuted, fontSize: 11)),
                                      ],
                                    ],
                                  ),
                                ),
                              ],
                            ),
                          ),
                        );
                      },
                    ),
                  ),
      ),
    );
  }
}
