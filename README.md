# CITYVILLEBURG; <br/>A City Generator

Cityvilleburg is an addon for Blender.

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