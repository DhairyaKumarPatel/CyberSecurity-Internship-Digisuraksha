#!/usr/bin/env python3
"""
Homoglyph Detector Tool
A cybersecurity utility to detect homoglyph attacks in domains and text.

Author: Dhairya Kumar Patel
Date: August 2025
"""

import argparse
import sys
import json
import re
from typing import Dict, List, Tuple, Set
from urllib.parse import urlparse
import unicodedata

class HomoglyphDetector:
    """
    A tool to detect homoglyph attacks by identifying visually similar characters
    that could be used to create deceptive domains or text.
    """
    
    def __init__(self):
        # Common homoglyph mappings (suspicious character -> original character)
        # This maps suspicious characters to their legitimate Latin equivalents
        self.homoglyph_map = {
            # Cyrillic to Latin mappings
            'а': 'a',  # Cyrillic small letter A
            'е': 'e',  # Cyrillic small letter E  
            'о': 'o',  # Cyrillic small letter O
            'р': 'p',  # Cyrillic small letter P
            'с': 'c',  # Cyrillic small letter C
            'х': 'x',  # Cyrillic small letter X
            'у': 'y',  # Cyrillic small letter Y
            'А': 'A',  # Cyrillic capital letter A
            'В': 'B',  # Cyrillic capital letter B
            'Е': 'E',  # Cyrillic capital letter E
            'К': 'K',  # Cyrillic capital letter K
            'М': 'M',  # Cyrillic capital letter M
            'Н': 'H',  # Cyrillic capital letter H
            'О': 'O',  # Cyrillic capital letter O
            'Р': 'P',  # Cyrillic capital letter P
            'С': 'C',  # Cyrillic capital letter C
            'Т': 'T',  # Cyrillic capital letter T
            'Х': 'X',  # Cyrillic capital letter X
            'У': 'Y',  # Cyrillic capital letter Y
            
            # Greek to Latin mappings
            'α': 'a',  # Greek small letter alpha
            'ε': 'e',  # Greek small letter epsilon
            'ο': 'o',  # Greek small letter omicron
            'ρ': 'p',  # Greek small letter rho
            'χ': 'x',  # Greek small letter chi
            'γ': 'y',  # Greek small letter gamma
            'ϲ': 'c',  # Greek lunate sigma symbol
            'Α': 'A',  # Greek capital letter alpha
            'Β': 'B',  # Greek capital letter beta
            'Ε': 'E',  # Greek capital letter epsilon
            'Η': 'H',  # Greek capital letter eta
            'Ι': 'I',  # Greek capital letter iota
            'Κ': 'K',  # Greek capital letter kappa
            'Μ': 'M',  # Greek capital letter mu
            'Ν': 'N',  # Greek capital letter nu
            'Ο': 'O',  # Greek capital letter omicron
            'Ρ': 'P',  # Greek capital letter rho
            'Τ': 'T',  # Greek capital letter tau
            'Υ': 'Y',  # Greek capital letter upsilon
            'Χ': 'X',  # Greek capital letter chi
            'Ζ': 'Z',  # Greek capital letter zeta
            
            # Mathematical alphanumeric symbols (commonly abused)
            '𝐚': 'a', '𝑎': 'a', '�': 'a', '�': 'a', '�': 'a', '�': 'a', '�': 'a',
            '𝐞': 'e', '𝑒': 'e', '�': 'e', '�': 'e', '�': 'e', '�': 'e', '�': 'e',
            '𝐨': 'o', '𝑜': 'o', '�': 'o', '�': 'o', '�': 'o', '�': 'o', '�': 'o',
            
            # Full-width characters (commonly used in attacks)
            'Ａ': 'A', 'Ｂ': 'B', 'Ｃ': 'C', 'Ｄ': 'D', 'Ｅ': 'E', 'Ｆ': 'F', 'Ｇ': 'G',
            'Ｈ': 'H', 'Ｉ': 'I', 'Ｊ': 'J', 'Ｋ': 'K', 'Ｌ': 'L', 'Ｍ': 'M', 'Ｎ': 'N',
            'Ｏ': 'O', 'Ｐ': 'P', 'Ｑ': 'Q', 'Ｒ': 'R', 'Ｓ': 'S', 'Ｔ': 'T', 'Ｕ': 'U',
            'Ｖ': 'V', 'Ｗ': 'W', 'Ｘ': 'X', 'Ｙ': 'Y', 'Ｚ': 'Z',
            'ａ': 'a', 'ｂ': 'b', 'ｃ': 'c', 'ｄ': 'd', 'ｅ': 'e', 'ｆ': 'f', 'ｇ': 'g',
            'ｈ': 'h', 'ｉ': 'i', 'ｊ': 'j', 'ｋ': 'k', 'ｌ': 'l', 'ｍ': 'm', 'ｎ': 'n',
            'ｏ': 'o', 'ｐ': 'p', 'ｑ': 'q', 'ｒ': 'r', 'ｓ': 's', 'ｔ': 't', 'ｕ': 'u',
            'ｖ': 'v', 'ｗ': 'w', 'ｘ': 'x', 'ｙ': 'y', 'ｚ': 'z',
            '０': '0', '１': '1', '２': '2', '３': '3', '４': '4', '５': '5',
            '６': '6', '７': '7', '８': '8', '９': '9',
        }
        
        # The homoglyph_map now directly maps suspicious chars to originals
        # No need for char_to_original mapping since homoglyph_map IS the mapping
    
    def analyze_text(self, text: str) -> Dict:
        """
        Analyze text for homoglyph characters.
        
        Args:
            text (str): Text to analyze
            
        Returns:
            Dict: Analysis results containing suspicious characters and statistics
        """
        suspicious_chars = []
        total_chars = len(text)
        suspicious_count = 0
        
        for i, char in enumerate(text):
            if char in self.homoglyph_map:
                suspicious_count += 1
                char_info = {
                    'position': i,
                    'character': char,
                    'unicode_name': unicodedata.name(char, 'UNKNOWN'),
                    'unicode_code': f'U+{ord(char):04X}',
                    'suggested_replacement': self.homoglyph_map[char],
                    'script': unicodedata.category(char)
                }
                suspicious_chars.append(char_info)
        
        # Calculate risk score (percentage of suspicious characters)
        risk_score = (suspicious_count / total_chars * 100) if total_chars > 0 else 0
        
        return {
            'text': text,
            'total_characters': total_chars,
            'suspicious_characters': suspicious_chars,
            'suspicious_count': suspicious_count,
            'risk_score': round(risk_score, 2),
            'is_suspicious': suspicious_count > 0
        }
    
    def analyze_domain(self, domain: str) -> Dict:
        """
        Analyze a domain name for homoglyph attacks.
        
        Args:
            domain (str): Domain name to analyze
            
        Returns:
            Dict: Analysis results for the domain
        """
        # Clean the domain (remove protocol, path, etc.)
        if '://' in domain:
            domain = urlparse(domain).netloc
        
        domain = domain.lower().strip()
        
        # Analyze the domain text
        analysis = self.analyze_text(domain)
        analysis['domain'] = domain
        analysis['type'] = 'domain'
        
        # Additional domain-specific checks
        if analysis['is_suspicious']:
            # Generate legitimate version
            legitimate_domain = self.generate_legitimate_version(domain)
            analysis['legitimate_version'] = legitimate_domain
            analysis['punycode_version'] = domain.encode('idna').decode('ascii')
        
        return analysis
    
    def generate_legitimate_version(self, text: str) -> str:
        """
        Generate a legitimate version by replacing homoglyphs with original characters.
        
        Args:
            text (str): Text containing potential homoglyphs
            
        Returns:
            str: Text with homoglyphs replaced
        """
        result = ""
        for char in text:
            if char in self.homoglyph_map:
                result += self.homoglyph_map[char]
            else:
                result += char
        return result
    
    def batch_analyze_domains(self, domains: List[str]) -> List[Dict]:
        """
        Analyze multiple domains for homoglyph attacks.
        
        Args:
            domains (List[str]): List of domains to analyze
            
        Returns:
            List[Dict]: Analysis results for all domains
        """
        results = []
        for domain in domains:
            analysis = self.analyze_domain(domain)
            results.append(analysis)
        return results
    
    def generate_report(self, analysis: Dict, format_type: str = 'text') -> str:
        """
        Generate a formatted report from analysis results.
        
        Args:
            analysis (Dict): Analysis results
            format_type (str): Report format ('text' or 'json')
            
        Returns:
            str: Formatted report
        """
        if format_type == 'json':
            return json.dumps(analysis, indent=2, ensure_ascii=False)
        
        # Text format
        report = []
        report.append("=" * 60)
        report.append("HOMOGLYPH DETECTION REPORT")
        report.append("=" * 60)
        
        if analysis.get('type') == 'domain':
            report.append(f"Domain: {analysis['domain']}")
        else:
            report.append(f"Text: {analysis['text'][:50]}{'...' if len(analysis['text']) > 50 else ''}")
        
        report.append(f"Total Characters: {analysis['total_characters']}")
        report.append(f"Suspicious Characters: {analysis['suspicious_count']}")
        report.append(f"Risk Score: {analysis['risk_score']}%")
        report.append(f"Status: {'SUSPICIOUS' if analysis['is_suspicious'] else 'CLEAN'}")
        
        if analysis['is_suspicious']:
            report.append("\nSUSPICIOUS CHARACTERS DETECTED:")
            report.append("-" * 40)
            
            for char_info in analysis['suspicious_characters']:
                report.append(f"Position {char_info['position']}: '{char_info['character']}'")
                report.append(f"  Unicode: {char_info['unicode_code']} ({char_info['unicode_name']})")
                report.append(f"  Suggested: '{char_info['suggested_replacement']}'")
                report.append("")
            
            if 'legitimate_version' in analysis:
                report.append(f"Legitimate Version: {analysis['legitimate_version']}")
            
            if 'punycode_version' in analysis:
                report.append(f"Punycode Version: {analysis['punycode_version']}")
        
        report.append("=" * 60)
        return "\n".join(report)

def main():
    """Main function to handle command line interface."""
    parser = argparse.ArgumentParser(
        description="Homoglyph Detector - Detect potential homoglyph attacks in domains and text",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s -d google.com
  %(prog)s -d аpple.com
  %(prog)s -t "This is а test with homoglуphs"
  %(prog)s -f domains.txt
  %(prog)s -d example.com --format json
        """
    )
    
    parser.add_argument('-d', '--domain', help='Single domain to analyze')
    parser.add_argument('-t', '--text', help='Text string to analyze')
    parser.add_argument('-f', '--file', help='File containing domains/text to analyze (one per line)')
    parser.add_argument('--format', choices=['text', 'json'], default='text', 
                       help='Output format (default: text)')
    parser.add_argument('-o', '--output', help='Output file (default: stdout)')
    parser.add_argument('--batch', action='store_true', 
                       help='Treat file input as batch processing')
    
    args = parser.parse_args()
    
    if not any([args.domain, args.text, args.file]):
        parser.error("Must specify either --domain, --text, or --file")
    
    detector = HomoglyphDetector()
    results = []
    
    try:
        if args.domain:
            analysis = detector.analyze_domain(args.domain)
            results.append(analysis)
        
        elif args.text:
            analysis = detector.analyze_text(args.text)
            results.append(analysis)
        
        elif args.file:
            with open(args.file, 'r', encoding='utf-8') as f:
                lines = [line.strip() for line in f if line.strip()]
            
            if args.batch:
                # Batch processing for domains
                results = detector.batch_analyze_domains(lines)
            else:
                # Individual analysis
                for line in lines:
                    if '.' in line and not ' ' in line:
                        # Likely a domain
                        analysis = detector.analyze_domain(line)
                    else:
                        # Treat as text
                        analysis = detector.analyze_text(line)
                    results.append(analysis)
    
    except FileNotFoundError:
        print(f"Error: File '{args.file}' not found.")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)
    
    # Generate output
    output_content = []
    
    if args.format == 'json':
        if len(results) == 1:
            output_content.append(json.dumps(results[0], indent=2, ensure_ascii=False))
        else:
            output_content.append(json.dumps(results, indent=2, ensure_ascii=False))
    else:
        for i, result in enumerate(results):
            if i > 0:
                output_content.append("\n")
            output_content.append(detector.generate_report(result, 'text'))
    
    final_output = "\n".join(output_content)
    
    # Write output
    if args.output:
        with open(args.output, 'w', encoding='utf-8') as f:
            f.write(final_output)
        print(f"Results written to {args.output}")
    else:
        print(final_output)

if __name__ == "__main__":
    main()
