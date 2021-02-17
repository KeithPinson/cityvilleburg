"""
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
"""

from inspect import isclass
from bpy.utils import register_class, unregister_class
from .src.addon.preferences import cvb_addon_register, cvb_addon_unregister
from .src.addon.preferences import CVB_AddonPreferences
from .src.panel.n_key_panel import CVB_PT_Main, CVB_OT_NewMap, CVB_OT_GenCity
from .src.panel.n_key_panel import CVB_PT_Help, CVB_OT_GettingStartedHelp
from .src.panel.panel_ops import CVB_OT_NewSketch, CVB_OT_EditCityName
from .src.panel.panel_props import cvb_panel_register, cvb_panel_unregister


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

# Ideally we should declare and define the hooks for the Blender
# classes in their respective packages, but because of the ease at
# which we can break the connections, we keep the class registry here
# and then try to perform a simple verification test of class existence.

CLASS_REGISTRY = (
    CVB_AddonPreferences,    # | Addon classes (keep at top)
    CVB_OT_NewMap,
    CVB_OT_GenCity,
    CVB_OT_GettingStartedHelp,
    CVB_OT_NewSketch,
    CVB_OT_EditCityName,
    CVB_PT_Main,
    CVB_PT_Help,
)


def verify_classes(registry):
    """Verify that we have all our required classes"""
    all_verified = True

    for reg in registry:
        if not isclass(reg):
            all_verified = False
            print(f'''Class missing from registry: {reg}''')

    return all_verified


CLASSES_VERIFIED = verify_classes(CLASS_REGISTRY)


def register():
    """Register the addon"""

    # The addon classes may contain data referenced by the
    # other classes so we make sure they are registered first
    register_class(CVB_AddonPreferences)

    # Setup any additional data the other classes may need
    cvb_addon_register()
    cvb_panel_register()

    # Okay, load the remainder of the classes
    for cls in CLASS_REGISTRY[1:]:
        register_class(cls)


def unregister():
    """Unregister the addon"""

    for cls in reversed(CLASS_REGISTRY):
        unregister_class(cls)

    cvb_panel_unregister()
    cvb_addon_unregister()


if CLASSES_VERIFIED and __name__ == "__main__":
    register()
