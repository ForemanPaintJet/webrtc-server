# 🔧 Git Development Workflow

This document outlines the Git workflow for the WebRTC project.

## 📁 Repository Structure

```
webrtc-server/
├── .git/                # Git repository data
├── .gitignore          # Files to ignore in version control
├── .venv/              # Virtual environment (ignored)
├── README.md           # Project overview
├── P2P_GUIDE.md        # Technical P2P implementation guide
├── requirements.txt    # Python dependencies
├── simple_camera.py    # Basic camera capture
├── p2p_webrtc.py      # P2P video chat with signaling
└── start.py           # Quick start script
```

## 🌟 Git Commands

### Basic Commands
```bash
# Check status
git status

# See commit history
git log --oneline

# See what changed
git diff

# Add files
git add filename.py
git add .  # Add all changes

# Commit changes
git commit -m "Your commit message"

# Push to remote (after setting up remote)
git push origin main
```

### Branch Management
```bash
# Create new feature branch
git checkout -b feature/new-feature

# Switch branches
git checkout main
git checkout feature/new-feature

# Merge feature branch
git checkout main
git merge feature/new-feature

# Delete branch
git branch -d feature/new-feature
```

### Remote Repository
```bash
# Add remote repository (GitHub/Bitbucket)
git remote add origin https://github.com/yourusername/webrtc-server.git

# Push to remote
git push -u origin main

# Pull from remote
git pull origin main

# Clone repository
git clone https://github.com/yourusername/webrtc-server.git
```

## 🚀 Development Workflow

### 1. Feature Development
```bash
# Start new feature
git checkout -b feature/video-filters
# Make changes...
git add .
git commit -m "Add video filter functionality"
git push origin feature/video-filters
```

### 2. Bug Fixes
```bash
# Create hotfix branch
git checkout -b hotfix/camera-permission-bug
# Fix the bug...
git add .
git commit -m "Fix camera permission handling"
git checkout main
git merge hotfix/camera-permission-bug
git push origin main
```

### 3. Release Process
```bash
# Tag releases
git tag -a v1.0.0 -m "Release version 1.0.0 - Basic camera and P2P chat"
git push origin v1.0.0

# See all tags
git tag
```

## 📝 Commit Message Convention

### Format:
```
<type>: <description>

[optional body]

[optional footer]
```

### Types:
- **feat**: New feature
- **fix**: Bug fix
- **docs**: Documentation changes
- **style**: Code style changes (formatting)
- **refactor**: Code refactoring
- **test**: Adding or updating tests
- **chore**: Build process or auxiliary tool changes

### Examples:
```bash
git commit -m "feat: add video quality selection"
git commit -m "fix: resolve camera permission error on Safari"
git commit -m "docs: update P2P setup instructions"
git commit -m "refactor: improve signaling server code structure"
```

## 🔄 Release History

### Version 1.0.0 (Initial Release)
- ✅ Basic camera capture (simple_camera.py)
- ✅ P2P video chat with signaling server (p2p_webrtc.py)
- ✅ Room-based video calls
- ✅ STUN server configuration
- ✅ Complete documentation

### Future Versions
- v1.1.0: Video recording functionality
- v1.2.0: Real-time video filters
- v1.3.0: Multiple camera support
- v2.0.0: Screen sharing integration

## 🛠️ Development Setup

### Clone and Setup:
```bash
# Clone repository
git clone https://github.com/yourusername/webrtc-server.git
cd webrtc-server

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Start development server
python p2p_webrtc.py
```

### Contributing:
1. **Fork** the repository
2. **Create** feature branch: `git checkout -b feature/amazing-feature`
3. **Commit** changes: `git commit -m 'Add amazing feature'`
4. **Push** to branch: `git push origin feature/amazing-feature`
5. **Open** Pull Request

## 📊 Git Configuration

### Useful Git Aliases:
```bash
git config --global alias.st status
git config --global alias.co checkout
git config --global alias.br branch
git config --global alias.ci commit
git config --global alias.unstage 'reset HEAD --'
git config --global alias.last 'log -1 HEAD'
git config --global alias.visual '!gitk'
```

### Editor Configuration:
```bash
git config --global core.editor "code --wait"  # VS Code
git config --global core.editor "vim"          # Vim
```

## 🔒 Best Practices

### Do:
- ✅ Write clear, descriptive commit messages
- ✅ Make small, focused commits
- ✅ Test before committing
- ✅ Use branches for features
- ✅ Keep commits atomic (one logical change)

### Don't:
- ❌ Commit sensitive data (passwords, keys)
- ❌ Commit large binary files
- ❌ Make commits without testing
- ❌ Use generic commit messages ("fix", "update")
- ❌ Commit commented-out code

---

**Happy coding with Git! 🎉**
