# Contributing to Security Tools Collection

Thank you for your interest in contributing! This guide will help you get started with contributing to this collection of security testing tools.

## Code of Conduct

This project is intended for educational and authorized security testing purposes only. By contributing, you agree to:

- **Promote ethical security testing practices only**
- **Include appropriate disclaimers and warnings** in all tools
- **Follow responsible disclosure principles**
- **Not facilitate unauthorized access to systems**
- **Emphasize the need for proper authorization** before testing

## How to Contribute

### Reporting Bugs

1. Check if the issue already exists in GitHub Issues
2. Create a new issue with:
   - Clear description of the problem
   - Steps to reproduce
   - Expected vs actual behavior
   - Your environment (OS, Python version)
   - Tool being used (SQL scanner, network scanner, etc.)

### Suggesting Features

1. Open an issue with the "enhancement" label
2. Describe the feature and its benefits
3. Consider implementation approaches
4. Discuss potential security implications
5. Explain how it fits with ethical testing practices

### Code Contributions

1. **Fork the repository**
2. **Create a feature branch**:
   ```bash
   git checkout -b feature/your-feature-name
   ```
3. **Make your changes**:
   - Follow the existing code style
   - Add comments for complex logic
   - Include comprehensive error handling
   - Maintain security best practices
   - Add appropriate legal disclaimers

4. **Test your changes**:
   - Test with various input formats
   - Verify parallel execution works (where applicable)
   - Check error handling with invalid inputs
   - Test on multiple platforms if possible

5. **Commit your changes**:
   ```bash
   git commit -am "Add feature: description"
   ```

6. **Push to your fork**:
   ```bash
   git push origin feature/your-feature-name
   ```

7. **Create a Pull Request**

## Code Style Guidelines

- **Use Python 3.7+ features**
- **Follow PEP 8 style guide**
- **Use type hints where appropriate**
- **Include docstrings for functions and classes**
- **Keep functions focused and single-purpose**
- **Use meaningful variable names**
- **Handle exceptions gracefully**
- **Include progress indicators for long operations**

## Security Considerations

When contributing to security tools:

- **Never include real credentials** in code or examples
- **Use safe test payloads** that won't cause actual damage
- **Include appropriate warnings** for destructive tests
- **Consider rate limiting** to avoid overwhelming targets
- **Validate inputs** to prevent misuse
- **Add proper session/connection cleanup**
- **Document potential risks** in code comments

## Testing Guidelines

Before submitting:

1. **Test with multiple input formats**
2. **Verify parallel processing works correctly**
3. **Check error handling with invalid inputs**
4. **Ensure proper resource cleanup**
5. **Test timeout handling**
6. **Verify legal disclaimers are shown**

## Documentation Requirements

- **Update README.md** if adding new features or tools
- **Include docstrings** for new functions and classes
- **Add examples** for new command-line options
- **Update help text** appropriately
- **Document any new dependencies**
- **Include security considerations** for new features

## Adding New Tools

When adding a new security tool:

1. **Create descriptive filename** (e.g., `port_scanner.py`)
2. **Include comprehensive help/usage**
3. **Add appropriate legal disclaimers**
4. **Follow the established code structure**
5. **Update main README.md** with tool description
6. **Add tool-specific documentation**
7. **Include example usage**

## Pull Request Guidelines

Good pull requests:

- **Have a clear title and description**
- **Include only related changes**
- **Don't break existing functionality**
- **Include appropriate tests**
- **Follow the code style**
- **Update documentation**
- **Include security considerations**

## Legal and Ethical Guidelines

All contributions must:

- **Include proper authorization warnings**
- **Emphasize educational purposes**
- **Promote responsible disclosure**
- **Not facilitate illegal activities**
- **Include appropriate disclaimers**

## Questions?

Feel free to open an issue for:
- Questions about contributing
- Clarification on security requirements
- Discussion of potential features
- Help with implementation
- Ethical considerations

## Legal Notice

By contributing, you certify that:

- **You have the right to submit your contribution**
- **You understand these are educational security tools**
- **You agree to the MIT license terms**
- **You will not use contributions to facilitate unauthorized access**
- **You promote ethical security testing practices**

Remember: These tools are for authorized testing only. Always get written permission before testing systems you don't own!