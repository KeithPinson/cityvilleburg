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

bl_info = {
    "name" : "CITYVILLEBURG zero.0",
    "author" : "KeithPinson",
    "description" : "City Generator",
    "blender" : (2, 91, 0),
    "version" : (0, 0, 1),
    "location" : "View3D > Sidebar > CreateTab",
    "category" : "Add Mesh",
    "wiki_url": "",
    "tracker_url": ""
}

from src.addon import addons

classes = addons.get_classes()

register, unregister = bpy.utils.register_classes_factory(classes)