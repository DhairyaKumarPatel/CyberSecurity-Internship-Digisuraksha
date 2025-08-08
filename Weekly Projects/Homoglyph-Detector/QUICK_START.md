# Quick Start Guide - Homoglyph Detector

## 🚀 Quick Setup and Usage

### 1. Basic Setup
```bash
# No installation required - uses Python standard library only
# Just ensure Python 3.6+ is installed
python --version  # Should show 3.6 or higher
```

### 2. Quick Test
```bash
# Run the test suite to verify everything works
python test_detector.py

# Test with a simple domain
python homoglyph_detector.py -d аpple.com
```

### 3. Common Use Cases

#### Check a Suspicious Domain
```bash
python homoglyph_detector.py -d suspicious-domain.com
```

#### Analyze Multiple Domains
```bash
python homoglyph_detector.py -f sample_domains.txt
```

#### Check Text for Homoglyphs
```bash
python homoglyph_detector.py -t "Your text here"
```

#### Get JSON Output for Automation
```bash
python homoglyph_detector.py -d domain.com --format json
```

### 4. Sample Outputs

#### Clean Domain
```
Status: CLEAN
Risk Score: 0.0%
```

#### Suspicious Domain
```
Status: SUSPICIOUS
Risk Score: 11.11%
Suspicious Characters: 1
Legitimate Version: apple.com
```

### 5. Integration Example

```python
from homoglyph_detector import HomoglyphDetector

detector = HomoglyphDetector()
result = detector.analyze_domain("suspicious-domain.com")

if result['is_suspicious']:
    print(f"⚠️  Suspicious domain detected!")
    print(f"Risk Score: {result['risk_score']}%")
else:
    print("✅ Domain appears clean")
```

### 6. Troubleshooting

- **Unicode Display Issues**: Ensure your terminal supports UTF-8
- **Permission Errors**: Make sure you have read access to input files
- **Python Version**: Use Python 3.6 or higher

For detailed documentation, see README.md
