import 'package:flutter_test/flutter_test.dart';
import 'package:academyflow/main.dart';

void main() {
  testWidgets('App launches', (WidgetTester tester) async {
    await tester.pumpWidget(const AcademyFlowApp());
    expect(find.text('AcademyFlow'), findsOneWidget);
  });
}
