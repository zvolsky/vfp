# vfp

Few **python utils**, f.e. **file utils**.
*Syntax of some of them is similar to visual foxpro.*

```python
.filetostr(filename)                        # read the file AS IS
.strtofile(content, filename, additive)     # write str or encode&write unicode
.strtoutf8file(content, filename, additive) # write unicode or decode&write str
                                            #       into utf8 file
.suredir(path)                              # create dir if not present
```

see source code for more parameters and parameters details

## how to instal

copy vfp.py somewhere into PYTHONPATH
```python
import vfp
content = vfp.filetostr('/dirname/filename.txt')
```
