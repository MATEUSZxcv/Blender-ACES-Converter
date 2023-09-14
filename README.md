# Blender ACES converter

### What it does?

Converts **all** textures' color spaces to their ACES counterparts. By default, it works with [Blender-ACES-Config](https://github.com/Ginurx/Blender-ACES-Config/tree/main) by *Ginurx* but can be easily [modified](#modifying) to work with any other one (or simply batch change color spaces, ACES not required).

Before             |  After
:-------------------------:|:-------------------------:
![](images/before.png)  |  ![](images/after.png)

### Where to find it?

3D Viewport -> Sidebar -> Tool -> ACES Converter

<img width="75%" src="images/location.png">


### How to use?

1. Open a blend file with **default** color management
2. Click the *`Save`* button
3. Close Blender and change color config
4. Reopen the blend file and click the *`Load`* button

## Extras

### How it works?

- *`save`* writes the name of the current color space for each texture into `ACES-Converter_tmp.txt`
- *`load`* reads every color space from `ACES-Converter_tmp.txt` and sets a new one accordingly (based on definitions inside `Blender-ACES-Converter.py`)

### Modifying

If you want to use it for other colorspaces (it will be implemented in UI, someday...) then simply change these lines in `Blender-ACES-Converter.py`:
  
```py
58            if color[i] == "sRGB":
59                m.colorspace_settings.name = 'role_matte_paint'
60            elif color[i] == "Non-Color":
61                m.colorspace_settings.name = 'role_data'
62            elif color[i] == "Linear":
63                m.colorspace_settings.name = 'Utility - Linear - sRGB'
```