# CITYVILLEBURG
## Synthetic Cities<br/>for Research, Art, and Gaming
*Cityvilleburg is an addon for Blender*


## Geographic Coordinate System

We don't use one. No latitude. No longitude. 
This is not a mapping tool. What we use is the
default Blender coordinate system where zero; x, y, and z,
marks the center of everything and an offset of
1 is equivalent to 1 meter.

## Development Notes

- For Blender auto-completions in an IDE, use [fake-bpy-module](https://github.com/nutti/fake-bpy-module) to sidestep the need to install Blender as a Python module.

  
    pip install fake-bpy-module-<Blender version>

- If clicking *Refresh* on the Add-ons tab of Blender 
does not seem to refresh your changes, then it may be 
necessary to force Blender to reload the add-ons. In the
Blender Python Console, run:
  

    bpy.ops.script.reload()

## License

[MIT](./LICENSE) © Keith Pinson