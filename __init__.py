#
# Copyright (c) 2021 Keith Pinson.
#
#  @see [[LICENSE]] file in the root directory of this source.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

# pylint: disable=invalid-name, missing-module-docstring, redefined-builtin

__doc__ = """A Blender addon for generating cities"""
__name__ = "CITYVILLEBURG"

from inspect import isclass
from bpy.utils import register_class, unregister_class
from .src.addon.preferences import cvb_addon_register, cvb_addon_unregister
from .src.addon.preferences import CVB_AddonPreferences
# Hold off on importing the modules with properties

bl_info = {
    "name": "CITYVILLEBURG",
    "author": "Copyright (c) 2021 Keith Pinson",
    "description": "A City Generator   (To start quickly, press n key and click the \"CVB\" tab)",
    "blender": (2, 91, 0),
    "version": (0, 0, 1),
    "location": "View3D > N-key-Panel",
    "category": "Add Mesh",
    "support": "COMMUNITY",
    "warning": "This Add-on is under development. Use at this time is not advised.",
    "saved_warning": "This Add-on is Beta software. Please report any bugs encountered.",
    "wiki_url": "https://github.com/KeithPinson/cityvilleburg/wiki",
    "tracker_url": "https://github.com/KeithPinson/cityvilleburg/issues"
}

# Make it clear in the console output where the output of this addon begins
print("\n", f'''*** {bl_info['name']} ***''')


# The addon class may contain data referenced by the
# other classes so we make sure it is pre-registered
register_class(CVB_AddonPreferences)


# Now that the addon preferences are loaded, import the modules with properties
from .src.panel.n_key_panel import CVB_PT_Main, CVB_OT_NewMapButton, CVB_OT_GenCityButton
from .src.panel.n_key_panel import CVB_OT_SketchEditButton, CVB_OT_TerrainEditButton
from .src.panel.n_key_panel import CVB_PT_Help, CVB_OT_GettingStartedHelp
from .src.panel.panel_ops import CVB_OT_NewSketchButton
from .src.panel.panel_props import cvb_panel_register, cvb_panel_unregister
from .src.terrain.terrain_editor \
    import CVB_PT_Terrain, CVB_OT_TerrainHelpButton, CVB_OT_TerrainClearButton, CVB_OT_TerrainAutogenButton


# Ideally we should declare and define the hooks for the Blender
# classes in their respective packages, but because of the ease at
# which we can break the connections, we keep the class registry here
# and then try to perform a simple verification test of class existence.

_CLASS_REGISTRY = (
    CVB_AddonPreferences,  # | Addon classes (keep at top)
    CVB_OT_NewMapButton,
    CVB_OT_GenCityButton,
    CVB_OT_GettingStartedHelp,
    CVB_OT_NewSketchButton,
    CVB_OT_SketchEditButton,
    CVB_OT_TerrainEditButton,
    CVB_PT_Main,
    CVB_PT_Help,
    CVB_PT_Terrain,
    CVB_OT_TerrainHelpButton,
    CVB_OT_TerrainClearButton,
    CVB_OT_TerrainAutogenButton,
)

def verify_classes(registry):
    """Verify that we have all our required classes"""
    all_verified = True

    for reg in registry:
        if not isclass(reg):
            all_verified = False
            print(f'''Class missing from registry: {reg}''')

    return all_verified


_CLASSES_VERIFIED = verify_classes(_CLASS_REGISTRY)


def register():
    """Register the rest of the addon"""

    # Setup any additional data the other classes may need
    cvb_addon_register()
    cvb_panel_register()

    # Okay, load the remainder of the classes (skip what we pre-registered)
    for cls in _CLASS_REGISTRY[1:]:
        register_class(cls)


def unregister():
    """Unregister the addon"""

    for cls in reversed(_CLASS_REGISTRY):
        unregister_class(cls)

    cvb_panel_unregister()
    cvb_addon_unregister()


if _CLASSES_VERIFIED and __name__ == "__main__":
    register()
