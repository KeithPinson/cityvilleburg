# Copyright (c) Keith Pinson.
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

import bpy
from bpy.utils import register_class, unregister_class
from inspect import isclass
from .src.utils.icons import IconCollection
# from .src.utils.thumbnails import ThumbnailCollection
from .src.addon.preferences import CVB_AddonPreferences
from .src.addon.preferencesProps import CVB_AddonPreferenceProps
from .src.panel.nPanel import CVB_PT_Main, CVB_OT_NewMap, CVB_OT_GenCity
from .src.panel.nPanel import CVB_PT_Help, CVB_OT_GettingStartedHelp


bl_info = {
    "name": "CITYVILLEBURG",
    "author": "KeithPinson",
    "description": "A City Generator, version  zero.0",
    "blender": (2, 91, 0),
    "version": (0, 0, 1),
    "location": "View3D > N-panel",
    "category": "Add Mesh",
    "support": "COMMUNITY",
    "warning": "This Add-on is under development. Use at this time is not advised.",
    "saved_warning": "This Add-on is Beta software. Please report any bugs encountered.",
    "wiki_url": "https://github.com/KeithPinson/cityvilleburg/wiki",
    "tracker_url": "https://github.com/KeithPinson/cityvilleburg/issues"
}

# Make it clear where the output on the console for this addon begins
print("\n", f'''*** {bl_info['name']} ***''')

# Ideally we should declare and define the hooks for the Blender
# classes in their respective packages, but because of the ease at
# which we can break the connections, we keep the class registry here
# and then try to perform a simple verification test of class existence.

CLASS_REGISTRY = (
    CVB_AddonPreferenceProps,  # | Addon classes (keep at the top)
    CVB_AddonPreferences,  # |
    CVB_OT_NewMap,
    CVB_OT_GenCity,
    CVB_OT_GettingStartedHelp,
    CVB_PT_Main,
    CVB_PT_Help,
)


def verify_classes(registry):
    all_verified = True

    for reg in registry:
        if not isclass(reg):
            all_verified = False
            print(f'''Class missing from registry: {reg}''')

    return all_verified


classes_verified = verify_classes(CLASS_REGISTRY)


def register():

    # The addon classes may contain data referenced by the
    # other classes so we make sure they are registered first
    register_class(CVB_AddonPreferenceProps)
    register_class(CVB_AddonPreferences)

    # Setup any additional data the other classes may need
    CVB_AddonPreferences.cvb_icons = IconCollection()

    # Okay, load the remainder of the classes
    for cls in CLASS_REGISTRY[2:]:
        register_class(cls)


def unregister():

    if CVB_AddonPreferences.cvb_icons is not None:
        del CVB_AddonPreferences.cvb_icons

    for cls in reversed(CLASS_REGISTRY):
        unregister_class(cls)


if classes_verified and __name__ == "__main__":
    register()
