#!/usr/bin/env python3
"""
Test script for Homoglyph Detector Tool
Demonstrates various features and usage examples.
"""

import sys
import os

# Add the current directory to Python path to import the detector
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from homoglyph_detector import HomoglyphDetector

def test_basic_functionality():
    """Test basic functionality of the HomoglyphDetector."""
    print("🧪 Testing Homoglyph Detector Tool")
    print("=" * 50)
    
    detector = HomoglyphDetector()
    
    # Test cases with known homoglyphs
    test_cases = [
        ("apple.com", "Clean domain"),
        ("аpple.com", "Cyrillic 'а' instead of Latin 'a'"),
        ("g00gle.com", "Zeros instead of 'o'"),
        ("micrоsoft.com", "Cyrillic 'о' instead of Latin 'o'"),
        ("рaypal.com", "Cyrillic 'р' instead of Latin 'p'"),
        ("Hello wоrld!", "Text with Cyrillic 'о'"),
        ("This is а test", "Text with Cyrillic 'а'"),
        ("Normal text", "Clean text"),
    ]
    
    print("\n🔍 DOMAIN AND TEXT ANALYSIS TESTS")
    print("-" * 50)
    
    for i, (test_input, description) in enumerate(test_cases, 1):
        print(f"\nTest {i}: {description}")
        print(f"Input: {test_input}")
        
        # Determine if it's a domain or text
        if '.' in test_input and ' ' not in test_input:
            result = detector.analyze_domain(test_input)
        else:
            result = detector.analyze_text(test_input)
        
        print(f"Status: {'SUSPICIOUS' if result['is_suspicious'] else 'CLEAN'}")
        print(f"Risk Score: {result['risk_score']}%")
        
        if result['is_suspicious']:
            print(f"Suspicious Characters: {result['suspicious_count']}")
            if 'legitimate_version' in result:
                print(f"Legitimate Version: {result['legitimate_version']}")
    
    print("\n" + "=" * 50)

def test_batch_processing():
    """Test batch processing functionality."""
    print("\n🔄 BATCH PROCESSING TEST")
    print("-" * 50)
    
    detector = HomoglyphDetector()
    
    # Create test domain list
    test_domains = [
        "google.com",
        "аpple.com",
        "microsoft.com",
        "аmazon.com",
        "facebook.com"
    ]
    
    results = detector.batch_analyze_domains(test_domains)
    
    print(f"Analyzed {len(results)} domains:")
    
    for result in results:
        status = "SUSPICIOUS" if result['is_suspicious'] else "CLEAN"
        print(f"  {result['domain']}: {status} (Risk: {result['risk_score']}%)")

def test_character_details():
    """Test detailed character analysis."""
    print("\n🔬 CHARACTER ANALYSIS TEST")
    print("-" * 50)
    
    detector = HomoglyphDetector()
    
    # Test with a string containing multiple homoglyphs
    test_text = "аpple and gооgle"
    result = detector.analyze_text(test_text)
    
    print(f"Text: {test_text}")
    print(f"Suspicious Characters Found: {result['suspicious_count']}")
    
    if result['suspicious_characters']:
        print("\nDetailed Character Analysis:")
        for char_info in result['suspicious_characters']:
            print(f"  Position {char_info['position']}: '{char_info['character']}'")
            print(f"    Unicode: {char_info['unicode_code']}")
            print(f"    Name: {char_info['unicode_name']}")
            print(f"    Suggested: '{char_info['suggested_replacement']}'")

def test_report_generation():
    """Test report generation in different formats."""
    print("\n📊 REPORT GENERATION TEST")
    print("-" * 50)
    
    detector = HomoglyphDetector()
    
    # Test with a suspicious domain
    result = detector.analyze_domain("аpple.com")
    
    print("Text Report:")
    text_report = detector.generate_report(result, 'text')
    print(text_report)
    
    print("\nJSON Report (first 200 characters):")
    json_report = detector.generate_report(result, 'json')
    print(json_report[:200] + "..." if len(json_report) > 200 else json_report)

def main():
    """Run all tests."""
    print("🚀 Homoglyph Detector Tool - Test Suite")
    print("=" * 60)
    
    try:
        test_basic_functionality()
        test_batch_processing()
        test_character_details()
        test_report_generation()
        
        print("\n✅ All tests completed successfully!")
        print("\n💡 Try running the tool with:")
        print("   python homoglyph_detector.py -d аpple.com")
        print("   python homoglyph_detector.py -f sample_domains.txt")
        print("   python homoglyph_detector.py -t 'This is а test'")
        
    except Exception as e:
        print(f"\n❌ Error during testing: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
