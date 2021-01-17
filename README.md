# CITYVILLEBURG; <br/>A City Generator

Cityvilleburg is an addon for Blender.

## Development Notes

- For Blender auto-completions in an IDE, use [fake-bpy-module](https://github.com/nutti/fake-bpy-module) to sidestep the need to install Blender as a Python module.

  
    pip install fake-bpy-module-<Blender version>

- There may be other ways to do this, but if Blender does
not seem to be affected by your changes, then it may be 
necessary to <code>touch</code> the root \_\_init\_\_.py file to test
the addon.

## License

[MIT](./LICENSE) © Keith Pinson