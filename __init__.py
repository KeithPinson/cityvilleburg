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
from .src.panel.n_panel import CVB_OT_PanelMapSegment
from .src.panel.n_panel import CVB_PT_PanelFrame

__CVB_DEBUG__ = True

bl_info = {
    "name": "CITYVILLEBURG",
    "author": "KeithPinson",
    "description": "A City Generator, version  zero.0",
    "blender": (2, 91, 0),
    "version": (0, 0, 1),
    "location": "View3D > N-panel",
    "category": "Add Mesh",
    "support": "COMMUNITY",
    "warning": "This Add-on is Beta software. Please report any bugs encountered.",
    "wiki_url": "https://github.com/KeithPinson/cityvilleburg/wiki",
    "tracker_url": "https://github.com/KeithPinson/cityvilleburg/issues"
}

if __CVB_DEBUG__:
    print("\n", f'''*** {bl_info['name']} ***''')

# Ideally we should declare and define the hooks for the Blender
# classes in their respective packages, but because of the ease at
# which we can break the connections, we keep the class registry here
# and then try to perform a simple verification test of class existence.

CLASS_REGISTRY = (
    CVB_OT_PanelMapSegment,
    CVB_PT_PanelFrame,
    CVB_AddonPreferences,
)


def verify_classes(registry):
    all_verified = True

    for reg in registry:
        if not isclass(reg):
            all_verified = False
            print(f'''Class missing from registry: {reg}''')

    return all_verified


if __CVB_DEBUG__:
    verify_classes(CLASS_REGISTRY)

cvb_icons = None
cvb_thumbnails = None


def register():
    global cvb_icons
    cvb_icons = IconCollection()

    for cls in CLASS_REGISTRY:
        register_class(cls)


def unregister():
    global cvb_icons

    for cls in reversed(CLASS_REGISTRY):
        unregister_class(cls)

    if cvb_icons is not None:
        del cvb_icons


if __name__ == "__main__":
    register()
