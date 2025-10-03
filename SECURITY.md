# Security Policy

## Supported Versions

The following versions of the ATM Simulator are currently supported with security updates:

| Version | Supported          |
| ------- | ------------------ |
| 1.x.x   | :white_check_mark: |
| < 1.0   | :x:                |

## Reporting a Vulnerability

We take the security of the ATM Simulator seriously. If you discover a security vulnerability, please follow these steps:

### How to Report

1. **DO NOT** open a public issue on GitHub
2. Email the security concern to the project maintainer
3. Include the following information:
   - Description of the vulnerability
   - Steps to reproduce the issue
   - Potential impact
   - Suggested fix (if available)

### What to Expect

- **Initial Response**: Within 48 hours of your report
- **Status Updates**: Every 5-7 business days
- **Resolution Timeline**: Depends on severity
  - Critical: 1-7 days
  - High: 7-14 days
  - Medium: 14-30 days
  - Low: 30-60 days

### Security Best Practices

When using the ATM Simulator:

1. **Never commit credentials** to version control
2. **Use strong passwords** for ATM accounts
3. **Rotate passwords** regularly in production environments
4. **Enable encryption** for sensitive data storage
5. **Keep dependencies updated** to patch known vulnerabilities
6. **Use environment variables** for sensitive configuration
7. **Implement proper access controls** in production deployments
8. **Regular security audits** are recommended

### Known Security Considerations

- This is a simulator intended for educational purposes
- Not designed for production financial systems
- Default configurations should be hardened for any real-world use
- PIN storage uses hashing but should be enhanced for production use

### Security Updates

Security patches will be released as soon as possible after verification. Users will be notified through:
- GitHub Security Advisories
- Release notes
- CHANGELOG.md updates

## Vulnerability Disclosure Policy

We follow coordinated vulnerability disclosure:

1. Reporter submits vulnerability privately
2. We confirm and assess the issue
3. We develop and test a fix
4. We release the fix
5. We publicly disclose the vulnerability after users have time to update

Thank you for helping keep the ATM Simulator secure!
