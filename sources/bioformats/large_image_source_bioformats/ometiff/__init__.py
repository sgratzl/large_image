# -*- coding: utf-8 -*-

#############################################################################
#  Copyright Kitware Inc.
#
#  Licensed under the Apache License, Version 2.0 ( the "License" );
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
#############################################################################
import six

from large_image.constants import SourcePriority
from large_image.cache_util import LruCacheMetaclass, methodcache

from ..base import BioFormatsFileTileSource


@six.add_metaclass(LruCacheMetaclass)
class OMETiffBioFormatsFileTileSource(BioFormatsFileTileSource):
    """
    Provides tile access to via Bio Formats for OME Tiff files
    """

    cacheName = 'tilesource'
    name = 'ometiff-bioformats'
    extensions = {
        None: SourcePriority.LOW,
        'ome.tif': SourcePriority.HIGH,
        'tif': SourcePriority.HIGH,
        'tiff': SourcePriority.HIGH,
        'ome': SourcePriority.PREFERRED,
    }

    def computeTiles(self):
        self.tileWidth = int(self._metadata.get('TileWidth', min(self.sizeX, 256)))
        self.tileHeight = int(self._metadata.get('TileLength', min(self.sizeY, 256)))

    @methodcache()
    def getTile(self, x, y, z, pilImageAllowed=False, mayRedirect=False, **kwargs):
        return super(OMETiffBioFormatsFileTileSource, self).getTile(x, y, z, pilImageAllowed=False,
                                                                    mayRedirect=False, **kwargs)