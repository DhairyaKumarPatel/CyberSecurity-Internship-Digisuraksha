#!/usr/bin/env python3
"""
Integration Example for Homoglyph Detector
Shows how to integrate the detector into security tools and workflows.
"""

import sys
import os

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from homoglyph_detector import HomoglyphDetector

def security_check_domains(domains):
    """
    Example security function to check multiple domains for homoglyph attacks.
    
    Args:
        domains (list): List of domains to check
        
    Returns:
        dict: Summary of results
    """
    detector = HomoglyphDetector()
    results = detector.batch_analyze_domains(domains)
    
    summary = {
        'total_domains': len(domains),
        'suspicious_domains': 0,
        'clean_domains': 0,
        'high_risk_domains': [],
        'suspicious_details': []
    }
    
    for result in results:
        if result['is_suspicious']:
            summary['suspicious_domains'] += 1
            summary['suspicious_details'].append({
                'domain': result['domain'],
                'risk_score': result['risk_score'],
                'legitimate_version': result.get('legitimate_version', ''),
                'suspicious_count': result['suspicious_count']
            })
            
            # Flag high-risk domains (>25% risk score)
            if result['risk_score'] > 25:
                summary['high_risk_domains'].append(result['domain'])
        else:
            summary['clean_domains'] += 1
    
    return summary

def email_security_check(email_content):
    """
    Example function to scan email content for homoglyph attacks.
    
    Args:
        email_content (str): Email text content
        
    Returns:
        dict: Analysis results
    """
    detector = HomoglyphDetector()
    result = detector.analyze_text(email_content)
    
    return {
        'is_suspicious': result['is_suspicious'],
        'risk_score': result['risk_score'],
        'suspicious_count': result['suspicious_count'],
        'warning_level': get_warning_level(result['risk_score']),
        'recommendation': get_recommendation(result['risk_score'])
    }

def get_warning_level(risk_score):
    """Get warning level based on risk score."""
    if risk_score == 0:
        return "SAFE"
    elif risk_score <= 10:
        return "LOW"
    elif risk_score <= 25:
        return "MEDIUM"
    elif risk_score <= 50:
        return "HIGH"
    else:
        return "CRITICAL"

def get_recommendation(risk_score):
    """Get security recommendation based on risk score."""
    if risk_score == 0:
        return "Content appears safe to process."
    elif risk_score <= 10:
        return "Monitor for context - may be legitimate international content."
    elif risk_score <= 25:
        return "Review manually - potential homoglyph attack detected."
    elif risk_score <= 50:
        return "Block and investigate - likely homoglyph attack."
    else:
        return "Block immediately - high confidence homoglyph attack."

def phishing_detector_example():
    """Example phishing detection workflow."""
    print("🎣 Phishing Detection Example")
    print("=" * 40)
    
    # Simulate suspicious domains from a phishing email
    suspicious_domains = [
        "google.com",           # Legitimate
        "аpple.com",           # Cyrillic 'а'
        "micrоsoft.com",       # Cyrillic 'о'
        "аmazon.com",          # Cyrillic 'а'
        "payрal.com",          # Cyrillic 'р'
        "facebook.com"         # Legitimate
    ]
    
    summary = security_check_domains(suspicious_domains)
    
    print(f"📊 Domain Analysis Summary:")
    print(f"Total Domains: {summary['total_domains']}")
    print(f"Clean Domains: {summary['clean_domains']}")
    print(f"Suspicious Domains: {summary['suspicious_domains']}")
    print(f"High Risk Domains: {len(summary['high_risk_domains'])}")
    
    if summary['suspicious_details']:
        print(f"\n⚠️  Suspicious Domains Detected:")
        for detail in summary['suspicious_details']:
            print(f"  - {detail['domain']} (Risk: {detail['risk_score']}%)")
            print(f"    Suggested: {detail['legitimate_version']}")
    
    if summary['high_risk_domains']:
        print(f"\n🚨 High Risk Domains (Block Immediately):")
        for domain in summary['high_risk_domains']:
            print(f"  - {domain}")

def email_content_example():
    """Example email content analysis."""
    print("\n📧 Email Content Analysis Example")
    print("=" * 40)
    
    # Simulate email content with homoglyphs
    email_samples = [
        "Dear customer, please visit our website at apple.com",
        "Urgent: Update your Micrоsoft account immediately",
        "Your Gооgle account has been compromised",
        "Contact suppоrt@company.com for assistance"
    ]
    
    for i, content in enumerate(email_samples, 1):
        print(f"\nEmail {i}: {content}")
        result = email_security_check(content)
        
        print(f"Warning Level: {result['warning_level']}")
        print(f"Risk Score: {result['risk_score']}%")
        print(f"Recommendation: {result['recommendation']}")

def main():
    """Run integration examples."""
    print("🔍 Homoglyph Detector - Integration Examples")
    print("=" * 60)
    
    try:
        phishing_detector_example()
        email_content_example()
        
        print(f"\n✅ Integration examples completed!")
        print(f"\n💡 Integration Tips:")
        print(f"  - Use risk scores for automated decision making")
        print(f"  - Combine with other security tools for better detection")
        print(f"  - Consider context when evaluating international content")
        print(f"  - Monitor and log all suspicious detections")
        
    except Exception as e:
        print(f"❌ Error during examples: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
