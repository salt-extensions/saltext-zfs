"""
ZFS grain provider
"""

import logging

# Solve the Chicken and egg problem where grains need to run before any
# of the modules are loaded and are generally available for any usage.
import salt.modules.cmdmod
import salt.utils.dictupdate
import salt.utils.platform

import saltext.zfs.utils.zfs

__virtualname__ = "zfs"
__salt__ = {
    "cmd.run": salt.modules.cmdmod.run,
}

log = logging.getLogger(__name__)


def __virtual__():
    # We always load this grain so we can properly export
    # at least the zfs_support grain
    # except for Windows... don't try to load this on Windows (#51703)
    if salt.utils.platform.is_windows():
        return False, "ZFS: Not available on Windows"
    return __virtualname__


def _zfs_pool_data():
    """
    Provide grains about zpools
    """
    grains = {}

    # collect zpool data
    zpool_list_cmd = saltext.zfs.utils.zfs.zpool_command(
        "list",
        flags=["-H"],
        opts={"-o": "name,size"},
    )
    for zpool in __salt__["cmd.run"](zpool_list_cmd, ignore_retcode=True).splitlines():
        if "zpool" not in grains:
            grains["zpool"] = {}
        zpool = zpool.split()
        grains["zpool"][zpool[0]] = saltext.zfs.utils.zfs.to_size(zpool[1], False)

    return grains


def zfs():
    """
    Provide grains for zfs/zpool
    """
    grains = {}
    grains["zfs_support"] = saltext.zfs.utils.zfs.is_supported()
    grains["zfs_feature_flags"] = saltext.zfs.utils.zfs.has_feature_flags()
    if grains["zfs_support"]:
        grains = salt.utils.dictupdate.update(grains, _zfs_pool_data(), merge_lists=True)

    return grains
