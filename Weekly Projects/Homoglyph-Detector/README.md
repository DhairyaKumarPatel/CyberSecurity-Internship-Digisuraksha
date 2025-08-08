# Homoglyph Detector Tool

A powerful Python-based cybersecurity utility designed to detect homoglyph attacks in domains and text. Homoglyphs are characters that look visually similar but have different Unicode values, often used in phishing attacks and domain spoofing.

## 🔍 What are Homoglyphs?

Homoglyphs are characters that appear visually identical or very similar but are actually different Unicode characters. Attackers exploit this by creating deceptive domains or text that look legitimate but use different character encodings.

**Examples of Homoglyph Attacks:**
- `аpple.com` (uses Cyrillic 'а' instead of Latin 'a')
- `g00gle.com` (uses zeros instead of 'o')
- `microsoft.com` with Cyrillic characters

## 🚀 Features

- **Domain Analysis**: Detect suspicious characters in domain names
- **Text Analysis**: Analyze any text string for homoglyph characters
- **Batch Processing**: Analyze multiple domains or text strings from files
- **Multiple Output Formats**: Text and JSON reporting
- **Unicode Analysis**: Detailed character information including Unicode codes
- **Risk Scoring**: Percentage-based risk assessment
- **Legitimate Version Generation**: Automatically suggest correct versions
- **Punycode Support**: Display punycode representation of suspicious domains

## 📋 Requirements

- Python 3.6 or higher
- No external dependencies (uses only standard library)

## 🛠️ Installation

1. Clone or download the script:
```bash
git clone <repository-url>
cd Homoglyph-Detector
```

2. Make the script executable (Linux/macOS):
```bash
chmod +x homoglyph_detector.py
```

## 📖 Usage

### Command Line Interface

```bash
python homoglyph_detector.py [OPTIONS]
```

### Options

- `-d, --domain`: Analyze a single domain
- `-t, --text`: Analyze a text string
- `-f, --file`: Analyze domains/text from a file (one per line)
- `--format`: Output format (`text` or `json`)
- `-o, --output`: Save results to a file
- `--batch`: Enable batch processing mode for files

### Examples

#### Analyze a Single Domain
```bash
python homoglyph_detector.py -d google.com
python homoglyph_detector.py -d аpple.com  # Contains Cyrillic 'а'
```

#### Analyze Text
```bash
python homoglyph_detector.py -t "This is а test with homoglуphs"
```

#### Batch Analysis from File
```bash
python homoglyph_detector.py -f domains.txt --batch
```

#### JSON Output
```bash
python homoglyph_detector.py -d аpple.com --format json
```

#### Save Results to File
```bash
python homoglyph_detector.py -f suspicious_domains.txt -o report.txt
```

## 📊 Sample Output

### Text Format
```
============================================================
HOMOGLYPH DETECTION REPORT
============================================================
Domain: аpple.com
Total Characters: 9
Suspicious Characters: 1
Risk Score: 11.11%
Status: SUSPICIOUS

SUSPICIOUS CHARACTERS DETECTED:
----------------------------------------
Position 0: 'а'
  Unicode: U+0430 (CYRILLIC SMALL LETTER A)
  Suggested: 'a'

Legitimate Version: apple.com
Punycode Version: xn--pple-43d.com
============================================================
```

### JSON Format
```json
{
  "domain": "аpple.com",
  "total_characters": 9,
  "suspicious_characters": [
    {
      "position": 0,
      "character": "а",
      "unicode_name": "CYRILLIC SMALL LETTER A",
      "unicode_code": "U+0430",
      "suggested_replacement": "a",
      "script": "Ll"
    }
  ],
  "suspicious_count": 1,
  "risk_score": 11.11,
  "is_suspicious": true,
  "type": "domain",
  "legitimate_version": "apple.com",
  "punycode_version": "xn--pple-43d.com"
}
```

## 🔧 Integration Examples

### Python Script Integration

```python
from homoglyph_detector import HomoglyphDetector

# Initialize detector
detector = HomoglyphDetector()

# Analyze a domain
result = detector.analyze_domain("аpple.com")
print(f"Risk Score: {result['risk_score']}%")
print(f"Suspicious: {result['is_suspicious']}")

# Analyze text
text_result = detector.analyze_text("Hello wоrld!")
if text_result['is_suspicious']:
    print("Suspicious characters found!")
    
# Batch analysis
domains = ["google.com", "аpple.com", "microsoft.com"]
batch_results = detector.batch_analyze_domains(domains)
```

## 🎯 Use Cases

### Cybersecurity Applications
- **Phishing Detection**: Identify spoofed domains in emails and URLs
- **Brand Protection**: Monitor for domain typosquatting attempts
- **Security Awareness**: Educational tool for demonstrating homoglyph attacks
- **Incident Response**: Analyze suspicious domains during investigations

### SOC Operations
- **URL Analysis**: Screen URLs before allowing access
- **Email Security**: Check sender domains for authenticity
- **Threat Intelligence**: Analyze indicators of compromise (IOCs)
- **Forensics**: Examine artifacts for hidden malicious content

## 🛡️ Supported Character Sets

The tool detects homoglyphs from various Unicode blocks:
- **Latin vs Cyrillic**: Common in domain spoofing
- **Greek Letters**: Mathematical and scientific contexts
- **Mathematical Alphanumeric**: Unicode blocks for styled text
- **Numbers**: Digit lookalikes (0 vs O, 1 vs l)

## 📁 File Format Examples

### domains.txt
```
google.com
аpple.com
microsoft.com
аmazon.com
facebook.com
```

### suspicious_text.txt
```
Welcome to оur website
This is а legitimate service
Contact suppоrt@company.com
```

## ⚠️ Limitations

- **Visual Similarity**: The tool uses predefined mappings and may not catch all possible homoglyphs
- **Context Awareness**: Cannot determine intent; legitimate use of international characters may be flagged
- **Character Coverage**: Limited to commonly abused character sets
- **False Positives**: International domains using legitimate non-Latin characters may be flagged

## 🔍 Detection Methods

1. **Unicode Normalization**: Analyzes character encoding differences
2. **Script Mixing**: Detects mixing of different writing systems
3. **Visual Similarity**: Uses predefined mappings of lookalike characters
4. **Statistical Analysis**: Calculates risk scores based on suspicious character density

## 📈 Risk Score Calculation

Risk Score = (Number of Suspicious Characters / Total Characters) × 100

- **0%**: Clean, no suspicious characters
- **1-25%**: Low risk, few suspicious characters
- **26-50%**: Medium risk, moderate suspicious content
- **51-75%**: High risk, significant suspicious content
- **76-100%**: Very high risk, heavily suspicious

## 🤝 Contributing

Contributions are welcome! Areas for improvement:
- Additional homoglyph mappings
- Better visual similarity detection
- Performance optimizations
- Additional output formats
- Integration with security tools

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 👨‍💻 Author

**Dhairya Kumar Patel**
- Cybersecurity Intern
- Digisuraksha Parhari Foundation Internship Program 2025

## 🆘 Support

If you encounter any issues or have questions:
1. Check the examples above
2. Ensure proper Unicode support in your terminal
3. Verify Python version compatibility
4. Report bugs with sample input/output

## 🔮 Future Enhancements

- [ ] Machine learning-based similarity detection
- [ ] Real-time domain monitoring
- [ ] Integration with threat intelligence feeds
- [ ] Visual diff highlighting in output
- [ ] Support for additional character sets
- [ ] Web-based interface
- [ ] API endpoint for integration

---

**⚠️ Disclaimer**: This tool is for educational and defensive cybersecurity purposes only. Users are responsible for compliance with applicable laws and regulations when using this tool.
