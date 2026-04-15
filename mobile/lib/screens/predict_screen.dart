import 'package:flutter/material.dart';
import '../services/api_service.dart';
import '../theme.dart';
import '../widgets/glass_card.dart';
import 'result_screen.dart';

class PredictScreen extends StatefulWidget {
  const PredictScreen({super.key});

  @override
  State<PredictScreen> createState() => _PredictScreenState();
}

class _PredictScreenState extends State<PredictScreen> {
  double _hoursStudied = 6;
  double _previousScores = 75;
  bool _extracurricular = false;
  double _sleepHours = 7;
  double _samplePapers = 4;
  double _targetScore = 85;
  bool _loading = false;

  Future<void> _predict() async {
    setState(() => _loading = true);
    try {
      final result = await ApiService.predict(
        hoursStudied: _hoursStudied.round(),
        previousScores: _previousScores.round(),
        extracurricular: _extracurricular,
        sleepHours: _sleepHours.round(),
        samplePapers: _samplePapers.round(),
        targetScore: _targetScore.round(),
      );
      if (mounted) {
        Navigator.push(context, MaterialPageRoute(builder: (_) => ResultScreen(data: result)));
      }
    } catch (e) {
      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(content: Text(ApiService.getErrorMessage(e))),
        );
      }
    }
    if (mounted) setState(() => _loading = false);
  }

  Widget _buildSlider(String label, IconData icon, double value, double min, double max, int divisions, Function(double) onChanged) {
    return GlassCard(
      padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 12),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Row(
            mainAxisAlignment: MainAxisAlignment.spaceBetween,
            children: [
              Row(children: [
                Icon(icon, size: 18, color: AppTheme.primary),
                const SizedBox(width: 8),
                Text(label, style: const TextStyle(color: AppTheme.textSecondary, fontWeight: FontWeight.w600)),
              ]),
              Text('${value.round()}', style: const TextStyle(color: AppTheme.primary, fontWeight: FontWeight.w800, fontSize: 20)),
            ],
          ),
          Slider(
            value: value, min: min, max: max, divisions: divisions,
            activeColor: AppTheme.primary,
            inactiveColor: AppTheme.primary.withValues(alpha: 0.2),
            onChanged: onChanged,
          ),
        ],
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Predict Performance')),
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
            _buildSlider('Hours Studied / Day', Icons.menu_book, _hoursStudied, 0, 12, 12, (v) => setState(() => _hoursStudied = v)),
            const SizedBox(height: 10),
            _buildSlider('Previous Scores (%)', Icons.assessment, _previousScores, 0, 100, 100, (v) => setState(() => _previousScores = v)),
            const SizedBox(height: 10),
            GlassCard(
              padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 8),
              child: SwitchListTile(
                title: const Row(children: [
                  Icon(Icons.emoji_events, size: 18, color: AppTheme.primary),
                  SizedBox(width: 8),
                  Text('Extracurricular Activities', style: TextStyle(color: AppTheme.textSecondary, fontWeight: FontWeight.w600)),
                ]),
                value: _extracurricular,
                activeColor: AppTheme.primary,
                onChanged: (v) => setState(() => _extracurricular = v),
              ),
            ),
            const SizedBox(height: 10),
            _buildSlider('Sleep Hours / Night', Icons.bedtime, _sleepHours, 4, 12, 8, (v) => setState(() => _sleepHours = v)),
            const SizedBox(height: 10),
            _buildSlider('Practice Papers Done', Icons.description, _samplePapers, 0, 10, 10, (v) => setState(() => _samplePapers = v)),
            const SizedBox(height: 10),
            _buildSlider('Target Score', Icons.flag, _targetScore, 50, 100, 50, (v) => setState(() => _targetScore = v)),
            const SizedBox(height: 24),
            SizedBox(
              height: 54,
              child: ElevatedButton.icon(
                onPressed: _loading ? null : _predict,
                icon: _loading ? const SizedBox.shrink() : const Icon(Icons.auto_awesome, size: 20),
                label: _loading
                    ? const SizedBox(height: 22, width: 22, child: CircularProgressIndicator(color: Colors.white, strokeWidth: 2))
                    : const Text('Predict Performance', style: TextStyle(fontSize: 17, fontWeight: FontWeight.w700)),
                style: ElevatedButton.styleFrom(
                  backgroundColor: AppTheme.primary,
                  shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(16)),
                ),
              ),
            ),
            const SizedBox(height: 20),
          ],
        ),
      ),
    );
  }
}
