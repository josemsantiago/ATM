# Contributing to ATM Simulator

Thank you for your interest in contributing to the ATM Simulator project! This document provides guidelines for contributing to this open source banking simulation.

## Code of Conduct

By participating in this project, you agree to maintain a welcoming, inclusive, and harassment-free environment for all contributors.

## Development Setup

### Prerequisites
- Python 3.7 or higher
- Git for version control

### Getting Started
1. Fork the repository
2. Clone your fork: `git clone https://github.com/yourusername/ATM.git`
3. Create a virtual environment: `python -m venv atm_env`
4. Activate the environment: `source atm_env/bin/activate` (Linux/Mac) or `atm_env\Scripts\activate` (Windows)
5. Install development dependencies: `pip install -r requirements.txt`

## Development Workflow

### Making Changes
1. Create a feature branch: `git checkout -b feature/your-feature-name`
2. Make your changes following the coding standards below
3. Write tests for your changes
4. Ensure all tests pass: `python test_atm.py`
5. Commit your changes with descriptive messages
6. Push to your fork: `git push origin feature/your-feature-name`
7. Create a Pull Request

### Pull Request Process
1. Ensure your PR description clearly describes the problem and solution
2. Include test coverage for new functionality
3. Update documentation if needed
4. Ensure all existing tests continue to pass
5. Request review from maintainers

## Coding Standards

### Python Style Guidelines
- Follow PEP 8 style guidelines
- Use descriptive variable and function names
- Include docstrings for all classes and methods
- Maintain consistent indentation (4 spaces)

### Code Quality
- Write unit tests for all new functionality
- Aim for high test coverage
- Use type hints where appropriate
- Handle exceptions gracefully
- Validate input parameters

### Security Considerations
- Never hardcode sensitive information
- Validate all user inputs
- Follow secure coding practices for financial applications
- Consider security implications of all changes

## Testing

### Running Tests
```bash
# Run all tests
python test_atm.py

# Run with coverage (if installed)
python -m pytest --cov=atm_simulator tests/
```

### Writing Tests
- Write tests for all new functionality
- Include edge cases and error conditions
- Use descriptive test names
- Follow the existing test structure

## Documentation

- Update README.md for significant changes
- Add docstrings to new classes and methods
- Include examples for new features
- Update API documentation if applicable

## Types of Contributions

### Welcome Contributions
- Bug fixes
- Performance improvements
- New banking features
- Security enhancements
- Documentation improvements
- Test coverage improvements

### Feature Requests
- Discuss major changes in issues first
- Ensure features align with project goals
- Consider backward compatibility
- Include comprehensive tests

## Reporting Issues

### Bug Reports
- Use the GitHub issue tracker
- Include steps to reproduce
- Provide system information
- Include error messages/logs

### Feature Requests
- Describe the use case clearly
- Explain the expected behavior
- Consider implementation complexity

## Recognition

Contributors will be acknowledged in:
- GitHub contributor list
- Project documentation
- Release notes for significant contributions

## Questions and Support

- Open an issue for general questions
- Tag maintainers for urgent matters
- Check existing issues before creating new ones

Thank you for contributing to the ATM Simulator project!