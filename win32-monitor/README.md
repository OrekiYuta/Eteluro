# Win32-monitor

**win32-monitor** is practical gadgets for monitor.

It can accomplish the following tasks

- Listen the KeyBoard press.
- Listen the Mouse point.
- Above will store the Screenshot and useful logger.

## Run

```shell
$ pip install -r requirements.txt

$ py .\win32-monitor.py

```

## Py to exe

```shell
$ pip install auto-py-to-exe -i https://pypi.tuna.tsinghua.edu.cn/simple/

$ auto-py-to-exe

```

## Release

- 0.0.4 Fix the keyboard and mouse to store records multiple times at the same time, and optimizing listen mode
- 0.0.3 Fix character set exceptions on Windows Server 2012 R2
- 0.0.2 Fix the lock screen/exit of Remote Desktop Services, resulting in an abnormal pop-up prompt
- 0.0.1 Brilliant on board

`-h : hide the console`


## Requirements
```shell
pipreqs . --encoding UTF-8
```
```shell
python==3.7.0
PyAutoGUI==0.9.54
pynput==1.7.2
pyinstaller=5.11.0
auto-py-to-exe=2.34.0
```

## Confuse

- https://pyob.oxyry.com/

## Reference

- https://nitratine.net/blog/post/how-to-use-pynputs-mouse-and-keyboard-listener-at-the-same-time/
- https://nitratine.net/blog/post/how-to-get-stored-wifi-passwords-in-windows/
- https://nitratine.net/blog/post/how-to-get-mouse-clicks-with-python/
- https://blog.csdn.net/weixin_44985880/article/details/116151434
- https://pyautogui.readthedocs.io/en/latest/
- https://pynput.readthedocs.io/en/latest/
- https://stackoverflow.com/questions/24944558/pyinstaller-built-windows-exe-fails-with-multiprocessing