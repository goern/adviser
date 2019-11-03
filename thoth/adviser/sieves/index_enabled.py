#!/usr/bin/env python3
# thoth-adviser
# Copyright(C) 2019 Fridolin Pokorny
#
# This program is free software: you can redistribute it and / or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

"""A step for filtering out disabled Python package indexes."""

import logging
from typing import Any
from typing import Optional
from typing import Dict
from typing import TYPE_CHECKING

from thoth.python import PackageVersion
from thoth.storages.exceptions import NotFoundError

from ..sieve import Sieve
from ..exceptions import NotAcceptable

if TYPE_CHECKING:
    from ..pipeline_builder import PipelineBuilderContext

_LOGGER = logging.getLogger(__name__)


class PackageIndexSieve(Sieve):
    """Filter out disabled Python package indexes."""

    @classmethod
    def should_include(
        cls, context: "PipelineBuilderContext"
    ) -> Optional[Dict[str, Any]]:
        """Remove indexes which are not enabled in pipeline configuration."""
        if not context.is_included(cls):
            return {}

        return None

    def run(self, package_version: PackageVersion) -> None:
        """Filter out package versions based on disabled Python package index."""
        try:
            is_enabled = self.graph.is_python_package_index_enabled(
                package_version.index.url
            )
        except NotFoundError:
            raise NotAcceptable(
                f"Removing Python package version {package_version.to_tuple()!r} as used index is not registered"
            )

        if not is_enabled:
            raise NotAcceptable(
                f"Removing Python package version {package_version.to_tuple()!r} as used index is not enabled"
            )