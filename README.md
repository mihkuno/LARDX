# LARDX
Google Bard for the Linux Terminal

![use](https://github.com/USTP-CSCORE/LARDX/assets/26486389/7b220982-6449-4a82-8c3c-c22804616278)

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
![downloading](https://github.com/USTP-CSCORE/LARDX/assets/26486389/b28e1b07-3f28-4c93-b5e2-de43b9c75cab)


#### Run the install script
```
./install && exit
```
#### Open a new terminal, then run
```
lardx
```
![install](https://github.com/USTP-CSCORE/LARDX/assets/26486389/1fa3d9f8-7230-417d-b52e-185bbc126f94)

<h2 align="center"></h2>

### Uninstalling
```
./uninstall
```
![uninstall](https://github.com/USTP-CSCORE/LARDX/assets/26486389/6e767e04-77dc-44b2-b7da-042ce5b2619c)

## How does it work?
- It uses `pyinstaller` to wrap libraries in an executable to be able to run even without python installed on the user's computer

- It emulates queries using a reverse engineered open-source `bardapi` using cookies of the user on Google Chrome
