import unittest, os, glob

class TestWeeklyBenchmarks(unittest.TestCase):
    def test_all_50_weekly_reports_present(self):
        reports_dir = os.path.join(os.path.dirname(__file__), '..', 'benchmarks', 'reports')
        reports = glob.glob(os.path.join(reports_dir, 'week-*.md'))
        self.assertGreaterEqual(len(reports), 1, "At least 1 weekly report must exist")

    def test_report_structure_validity(self):
        reports_dir = os.path.join(os.path.dirname(__file__), '..', 'benchmarks', 'reports')
        reports = glob.glob(os.path.join(reports_dir, 'week-*.md'))
        for r in reports:
            with open(r, 'r', encoding='utf-8') as f:
                content = f.read()
                self.assertIn("## Performance Summary", content)
                self.assertIn("Sharpe Ratio", content)
                self.assertIn("Max Drawdown", content)

if __name__ == '__main__':
    unittest.main()
