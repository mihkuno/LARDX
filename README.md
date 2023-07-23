# LARDX
Google Bard for the Linux Terminal

<h2 align="center"></h2>

### Requirements
- **Google Chrome** with **bard.google.com** is logged in
- Make sure there's only one user using chrome [Issue #8](https://github.com/USTP-CSCORE/LARDX/issues/8)

<h2 align="center"></h2>

### Installation

#### Clone this repository
```
git clone https://github.com/USTP-CSCORE/LARDX.git
```

#### Run the install script
```
./install && exit
```

#### Open a new terminal, then run
```
lardx
```

<h2 align="center"></h2>

### Uninstalling
```
./uninstall
```

## How does it work?
The script uses a wrapped executable of libraries to allow usage even without python installed on the end-user
It emulates queries using a reverse engineered open-source `bardapi` with a Google Chrome browser session extractor
