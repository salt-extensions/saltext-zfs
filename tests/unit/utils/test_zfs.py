"""
Tests for the zfs utils library

:codeauthor:    Jorge Schrauwen <sjorge@blackdot.be>
:maintainer:    Jorge Schrauwen <sjorge@blackdot.be>
:maturity:      new
:platform:      illumos,freebsd,linux

.. versionadded:: 2018.3.1
"""

from unittest.mock import MagicMock
from unittest.mock import patch

import pytest
from salt.utils.odict import OrderedDict

from saltext.zfs.utils import zfs
from tests.support.zfs import ZFSMockData


@pytest.fixture(scope="module")
def zfsdata():
    return ZFSMockData()


# NOTE: test parameter parsing
def test_is_supported():
    """
    Test zfs.is_supported method
    """
    for value in [False, True]:
        with patch("salt.utils.path.which", MagicMock(return_value=value)):
            with patch("salt.utils.platform.is_linux", MagicMock(return_value=value)):
                assert value == zfs.is_supported()


def test_property_data_zpool(zfsdata):
    """
    Test parsing of zpool get output
    """
    with patch.object(zfs, "_zfs_cmd", MagicMock(return_value="/sbin/zfs")):
        with patch.object(zfs, "_zpool_cmd", MagicMock(return_value="/sbin/zpool")):
            with patch.object(zfs, "_exec", MagicMock(return_value=zfsdata.pmap_exec_zpool)):
                assert zfs.property_data_zpool() == zfsdata.pmap_zpool


def test_property_data_zfs(zfsdata):
    """
    Test parsing of zfs get output
    """
    with patch.object(zfs, "_zfs_cmd", MagicMock(return_value="/sbin/zfs")):
        with patch.object(zfs, "_zpool_cmd", MagicMock(return_value="/sbin/zpool")):
            with patch.object(zfs, "_exec", MagicMock(return_value=zfsdata.pmap_exec_zfs)):
                assert zfs.property_data_zfs() == zfsdata.pmap_zfs


# NOTE: testing from_bool results
def test_from_bool_on():
    """
    Test from_bool with 'on'
    """
    assert zfs.from_bool("on") is True
    assert zfs.from_bool(zfs.from_bool("on")) is True


def test_from_bool_off():
    """
    Test from_bool with 'off'
    """
    assert zfs.from_bool("off") is False
    assert zfs.from_bool(zfs.from_bool("off")) is False


def test_from_bool_none():
    """
    Test from_bool with 'none'
    """
    assert zfs.from_bool("none") is None
    assert zfs.from_bool(zfs.from_bool("none")) is None


def test_from_bool_passthrough():
    """
    Test from_bool with 'passthrough'
    """
    assert zfs.from_bool("passthrough") == "passthrough"
    assert zfs.from_bool(zfs.from_bool("passthrough")) == "passthrough"


def test_from_bool_alt_yes():
    """
    Test from_bool_alt with 'yes'
    """
    assert zfs.from_bool_alt("yes") is True
    assert zfs.from_bool_alt(zfs.from_bool_alt("yes")) is True


def test_from_bool_alt_no():
    """
    Test from_bool_alt with 'no'
    """
    assert zfs.from_bool_alt("no") is False
    assert zfs.from_bool_alt(zfs.from_bool_alt("no")) is False


def test_from_bool_alt_none():
    """
    Test from_bool_alt with 'none'
    """
    assert zfs.from_bool_alt("none") is None
    assert zfs.from_bool_alt(zfs.from_bool_alt("none")) is None


def test_from_bool_alt_passthrough():
    """
    Test from_bool_alt with 'passthrough'
    """
    assert zfs.from_bool_alt("passthrough") == "passthrough"
    assert zfs.from_bool_alt(zfs.from_bool_alt("passthrough")) == "passthrough"


# NOTE: testing to_bool results
def test_to_bool_true():
    """
    Test to_bool with True
    """
    assert zfs.to_bool(True) == "on"
    assert zfs.to_bool(zfs.to_bool(True)) == "on"


def test_to_bool_false():
    """
    Test to_bool with False
    """
    assert zfs.to_bool(False) == "off"
    assert zfs.to_bool(zfs.to_bool(False)) == "off"


def test_to_bool_none():
    """
    Test to_bool with None
    """
    assert zfs.to_bool(None) == "none"
    assert zfs.to_bool(zfs.to_bool(None)) == "none"


def test_to_bool_passthrough():
    """
    Test to_bool with 'passthrough'
    """
    assert zfs.to_bool("passthrough") == "passthrough"
    assert zfs.to_bool(zfs.to_bool("passthrough")) == "passthrough"


def test_to_bool_alt_true():
    """
    Test to_bool_alt with True
    """
    assert zfs.to_bool_alt(True) == "yes"
    assert zfs.to_bool_alt(zfs.to_bool_alt(True)) == "yes"


def test_to_bool_alt_false():
    """
    Test to_bool_alt with False
    """
    assert zfs.to_bool_alt(False) == "no"
    assert zfs.to_bool_alt(zfs.to_bool_alt(False)) == "no"


def test_to_bool_alt_none():
    """
    Test to_bool_alt with None
    """
    assert zfs.to_bool_alt(None) == "none"
    assert zfs.to_bool_alt(zfs.to_bool_alt(None)) == "none"


def test_to_bool_alt_passthrough():
    """
    Test to_bool_alt with 'passthrough'
    """
    assert zfs.to_bool_alt("passthrough") == "passthrough"
    assert zfs.to_bool_alt(zfs.to_bool_alt("passthrough")) == "passthrough"


# NOTE: testing from_numeric results
def test_from_numeric_str():
    """
    Test from_numeric with '42'
    """
    assert zfs.from_numeric("42") == 42
    assert zfs.from_numeric(zfs.from_numeric("42")) == 42


def test_from_numeric_int():
    """
    Test from_numeric with 42
    """
    assert zfs.from_numeric(42) == 42
    assert zfs.from_numeric(zfs.from_numeric(42)) == 42


def test_from_numeric_none():
    """
    Test from_numeric with 'none'
    """
    assert zfs.from_numeric("none") is None
    assert zfs.from_numeric(zfs.from_numeric("none")) is None


def test_from_numeric_passthrough():
    """
    Test from_numeric with 'passthrough'
    """
    assert zfs.from_numeric("passthrough") == "passthrough"
    assert zfs.from_numeric(zfs.from_numeric("passthrough")) == "passthrough"


# NOTE: testing to_numeric results
def test_to_numeric_str():
    """
    Test to_numeric with '42'
    """
    assert zfs.to_numeric("42") == 42
    assert zfs.to_numeric(zfs.to_numeric("42")) == 42


def test_to_numeric_int():
    """
    Test to_numeric with 42
    """
    assert zfs.to_numeric(42) == 42
    assert zfs.to_numeric(zfs.to_numeric(42)) == 42


def test_to_numeric_none():
    """
    Test to_numeric with 'none'
    """
    assert zfs.to_numeric(None) == "none"
    assert zfs.to_numeric(zfs.to_numeric(None)) == "none"


def test_to_numeric_passthrough():
    """
    Test to_numeric with 'passthrough'
    """
    assert zfs.to_numeric("passthrough") == "passthrough"
    assert zfs.to_numeric(zfs.to_numeric("passthrough")) == "passthrough"


# NOTE: testing from_size results
def test_from_size_absolute():
    """
    Test from_size with '5G'
    """
    assert zfs.from_size("5G") == 5368709120
    assert zfs.from_size(zfs.from_size("5G")) == 5368709120


def test_from_size_decimal():
    """
    Test from_size with '4.20M'
    """
    assert zfs.from_size("4.20M") == 4404019
    assert zfs.from_size(zfs.from_size("4.20M")) == 4404019


def test_from_size_none():
    """
    Test from_size with 'none'
    """
    assert zfs.from_size("none") is None
    assert zfs.from_size(zfs.from_size("none")) is None


def test_from_size_passthrough():
    """
    Test from_size with 'passthrough'
    """
    assert zfs.from_size("passthrough") == "passthrough"
    assert zfs.from_size(zfs.from_size("passthrough")) == "passthrough"


# NOTE: testing to_size results
def test_to_size_str_absolute():
    """
    Test to_size with '5368709120'
    """
    assert zfs.to_size("5368709120") == "5G"
    assert zfs.to_size(zfs.to_size("5368709120")) == "5G"


def test_to_size_str_decimal():
    """
    Test to_size with '4404019'
    """
    assert zfs.to_size("4404019") == "4.20M"
    assert zfs.to_size(zfs.to_size("4404019")) == "4.20M"


def test_to_size_int_absolute():
    """
    Test to_size with 5368709120
    """
    assert zfs.to_size(5368709120) == "5G"
    assert zfs.to_size(zfs.to_size(5368709120)) == "5G"


def test_to_size_int_decimal():
    """
    Test to_size with 4404019
    """
    assert zfs.to_size(4404019) == "4.20M"
    assert zfs.to_size(zfs.to_size(4404019)) == "4.20M"


def test_to_size_none():
    """
    Test to_size with 'none'
    """
    assert zfs.to_size(None) == "none"
    assert zfs.to_size(zfs.to_size(None)) == "none"


def test_to_size_passthrough():
    """
    Test to_size with 'passthrough'
    """
    assert zfs.to_size("passthrough") == "passthrough"
    assert zfs.to_size(zfs.to_size("passthrough")) == "passthrough"


# NOTE: testing from_str results
def test_from_str_space():
    """
    Test from_str with "\"my pool/my dataset\"
    """
    assert zfs.from_str('"my pool/my dataset"') == "my pool/my dataset"
    assert zfs.from_str(zfs.from_str('"my pool/my dataset"')) == "my pool/my dataset"


def test_from_str_squote_space():
    """
    Test from_str with "my pool/jorge's dataset"
    """
    assert zfs.from_str("my pool/jorge's dataset") == "my pool/jorge's dataset"
    assert zfs.from_str(zfs.from_str("my pool/jorge's dataset")) == "my pool/jorge's dataset"


def test_from_str_dquote_space():
    """
    Test from_str with "my pool/the \"good\" stuff"
    """
    assert zfs.from_str('my pool/the "good" stuff') == 'my pool/the "good" stuff'
    assert zfs.from_str(zfs.from_str('my pool/the "good" stuff')) == 'my pool/the "good" stuff'


def test_from_str_none():
    """
    Test from_str with 'none'
    """
    assert zfs.from_str("none") is None
    assert zfs.from_str(zfs.from_str("none")) is None


def test_from_str_passthrough():
    """
    Test from_str with 'passthrough'
    """
    assert zfs.from_str("passthrough") == "passthrough"
    assert zfs.from_str(zfs.from_str("passthrough")) == "passthrough"


# NOTE: testing to_str results
def test_to_str_space():
    """
    Test to_str with 'my pool/my dataset'
    """
    # NOTE: for fun we use both the '"str"' and "\"str\"" way of getting the literal string: "str"
    assert zfs.to_str("my pool/my dataset") == '"my pool/my dataset"'
    assert zfs.to_str(zfs.to_str("my pool/my dataset")) == '"my pool/my dataset"'


def test_to_str_squote_space():
    """
    Test to_str with "my pool/jorge's dataset"
    """
    assert zfs.to_str("my pool/jorge's dataset") == '"my pool/jorge\'s dataset"'
    assert zfs.to_str(zfs.to_str("my pool/jorge's dataset")) == '"my pool/jorge\'s dataset"'


def test_to_str_none():
    """
    Test to_str with 'none'
    """
    assert zfs.to_str(None) == "none"
    assert zfs.to_str(zfs.to_str(None)) == "none"


def test_to_str_passthrough():
    """
    Test to_str with 'passthrough'
    """
    assert zfs.to_str("passthrough") == "passthrough"
    assert zfs.to_str(zfs.to_str("passthrough")) == "passthrough"


# NOTE: testing is_snapshot
def test_is_snapshot_snapshot():
    """
    Test is_snapshot with a valid snapshot name
    """
    assert zfs.is_snapshot("zpool_name/dataset@backup") is True


def test_is_snapshot_bookmark():
    """
    Test is_snapshot with a valid bookmark name
    """
    assert zfs.is_snapshot("zpool_name/dataset#backup") is False


def test_is_snapshot_filesystem():
    """
    Test is_snapshot with a valid filesystem name
    """
    assert zfs.is_snapshot("zpool_name/dataset") is False


# NOTE: testing is_bookmark
def test_is_bookmark_snapshot():
    """
    Test is_bookmark with a valid snapshot name
    """
    assert zfs.is_bookmark("zpool_name/dataset@backup") is False


def test_is_bookmark_bookmark():
    """
    Test is_bookmark with a valid bookmark name
    """
    assert zfs.is_bookmark("zpool_name/dataset#backup") is True


def test_is_bookmark_filesystem():
    """
    Test is_bookmark with a valid filesystem name
    """
    assert zfs.is_bookmark("zpool_name/dataset") is False


# NOTE: testing is_dataset
def test_is_dataset_snapshot():
    """
    Test is_dataset with a valid snapshot name
    """
    assert zfs.is_dataset("zpool_name/dataset@backup") is False


def test_is_dataset_bookmark():
    """
    Test is_dataset with a valid bookmark name
    """
    assert zfs.is_dataset("zpool_name/dataset#backup") is False


def test_is_dataset_filesystem():
    """
    Test is_dataset with a valid filesystem/volume name
    """
    assert zfs.is_dataset("zpool_name/dataset") is True


@pytest.fixture
def zfs_cmd_mock(zfsdata):
    with patch.object(zfs, "_zfs_cmd", MagicMock(return_value="/sbin/zfs")):
        with patch.object(zfs, "_zpool_cmd", MagicMock(return_value="/sbin/zpool")):
            with patch.object(zfs, "property_data_zfs", MagicMock(return_value=zfsdata.pmap_zfs)):
                with patch.object(
                    zfs,
                    "property_data_zpool",
                    MagicMock(return_value=zfsdata.pmap_zpool),
                ):
                    yield


# NOTE: testing zfs_command
@pytest.mark.usefixtures("zfs_cmd_mock")
def test_zfs_command_simple():
    """
    Test if zfs_command builds the correct string
    """
    assert zfs.zfs_command("list") == "/sbin/zfs list"


@pytest.mark.usefixtures("zfs_cmd_mock")
def test_zfs_command_none_target():
    """
    Test if zfs_command builds the correct string with a target of None
    """
    assert zfs.zfs_command("list", target=[None, "mypool", None]) == "/sbin/zfs list mypool"


@pytest.mark.usefixtures("zfs_cmd_mock")
def test_zfs_command_flag():
    """
    Test if zfs_command builds the correct string
    """
    my_flags = [
        "-r",  # recursive
    ]
    assert zfs.zfs_command("list", flags=my_flags) == "/sbin/zfs list -r"


@pytest.mark.usefixtures("zfs_cmd_mock")
def test_zfs_command_opt():
    """
    Test if zfs_command builds the correct string
    """
    my_opts = {
        "-t": "snap",  # only list snapshots
    }
    assert zfs.zfs_command("list", opts=my_opts) == "/sbin/zfs list -t snap"


@pytest.mark.usefixtures("zfs_cmd_mock")
def test_zfs_command_flag_opt():
    """
    Test if zfs_command builds the correct string
    """
    my_flags = [
        "-r",  # recursive
    ]
    my_opts = {
        "-t": "snap",  # only list snapshots
    }
    assert zfs.zfs_command("list", flags=my_flags, opts=my_opts) == "/sbin/zfs list -r -t snap"


@pytest.mark.usefixtures("zfs_cmd_mock")
def test_zfs_command_target():
    """
    Test if zfs_command builds the correct string
    """
    my_flags = [
        "-r",  # recursive
    ]
    my_opts = {
        "-t": "snap",  # only list snapshots
    }
    assert (
        zfs.zfs_command("list", flags=my_flags, opts=my_opts, target="mypool")
        == "/sbin/zfs list -r -t snap mypool"
    )


@pytest.mark.usefixtures("zfs_cmd_mock")
def test_zfs_command_target_with_space():
    """
    Test if zfs_command builds the correct string
    """
    my_flags = [
        "-r",  # recursive
    ]
    my_opts = {
        "-t": "snap",  # only list snapshots
    }
    assert (
        zfs.zfs_command("list", flags=my_flags, opts=my_opts, target="my pool")
        == '/sbin/zfs list -r -t snap "my pool"'
    )


@pytest.mark.usefixtures("zfs_cmd_mock")
def test_zfs_command_property():
    """
    Test if zfs_command builds the correct string
    """
    assert (
        zfs.zfs_command("get", property_name="quota", target="mypool")
        == "/sbin/zfs get quota mypool"
    )


@pytest.mark.usefixtures("zfs_cmd_mock")
def test_zfs_command_property_value():
    """
    Test if zfs_command builds the correct string
    """
    my_flags = [
        "-r",  # recursive
    ]
    assert (
        zfs.zfs_command(
            "set", flags=my_flags, property_name="quota", property_value="5G", target="mypool"
        )
        == "/sbin/zfs set -r quota=5368709120 mypool"
    )


@pytest.mark.usefixtures("zfs_cmd_mock")
def test_zfs_command_multi_property_value():
    """
    Test if zfs_command builds the correct string
    """
    property_name = ["quota", "readonly"]
    property_value = ["5G", "no"]
    assert (
        zfs.zfs_command(
            "set", property_name=property_name, property_value=property_value, target="mypool"
        )
        == "/sbin/zfs set quota=5368709120 readonly=off mypool"
    )


@pytest.mark.usefixtures("zfs_cmd_mock")
def test_zfs_command_fs_props():
    """
    Test if zfs_command builds the correct string
    """
    my_flags = [
        "-p",  # create parent
    ]
    my_props = {
        "quota": "1G",
        "compression": "lz4",
    }
    assert (
        zfs.zfs_command(
            "create", flags=my_flags, filesystem_properties=my_props, target="mypool/dataset"
        )
        == "/sbin/zfs create -p -o compression=lz4 -o quota=1073741824 mypool/dataset"
    )


@pytest.mark.usefixtures("zfs_cmd_mock")
def test_zfs_command_fs_props_with_space():
    """
    Test if zfs_command builds the correct string
    """
    my_props = {
        "quota": "4.2M",
        "compression": "lz4",
    }
    assert zfs.zfs_command(
        "create", filesystem_properties=my_props, target="my pool/jorge's dataset"
    ) == ('/sbin/zfs create -o compression=lz4 -o quota=4404019 "my' " pool/jorge's dataset\"")


# NOTE: testing zpool_command
@pytest.mark.usefixtures("zfs_cmd_mock")
def test_zpool_command_simple():
    """
    Test if zfs_command builds the correct string
    """
    assert zfs.zpool_command("list") == "/sbin/zpool list"


@pytest.mark.usefixtures("zfs_cmd_mock")
def test_zpool_command_opt():
    """
    Test if zpool_command builds the correct string
    """
    my_opts = {
        "-o": "name,size",  # show only name and size
    }
    assert zfs.zpool_command("list", opts=my_opts) == "/sbin/zpool list -o name,size"


@pytest.mark.usefixtures("zfs_cmd_mock")
def test_zpool_command_opt_list():
    """
    Test if zpool_command builds the correct string
    """
    my_opts = {
        "-d": ["/tmp", "/zvol"],
    }
    assert (
        zfs.zpool_command("import", opts=my_opts, target="mypool")
        == "/sbin/zpool import -d /tmp -d /zvol mypool"
    )


@pytest.mark.usefixtures("zfs_cmd_mock")
def test_zpool_command_flag_opt():
    """
    Test if zpool_command builds the correct string
    """
    my_opts = {
        "-o": "name,size",  # show only name and size
    }
    assert zfs.zpool_command("list", opts=my_opts) == "/sbin/zpool list -o name,size"


@pytest.mark.usefixtures("zfs_cmd_mock")
def test_zpool_command_target():
    """
    Test if zpool_command builds the correct string
    """
    my_opts = {
        "-o": "name,size",  # show only name and size
    }
    assert (
        zfs.zpool_command("list", opts=my_opts, target="mypool")
        == "/sbin/zpool list -o name,size mypool"
    )


@pytest.mark.usefixtures("zfs_cmd_mock")
def test_zpool_command_target_with_space():
    """
    Test if zpool_command builds the correct string
    """
    fs_props = {
        "quota": "100G",
    }
    pool_props = {
        "comment": "jorge's comment has a space",
    }
    assert zfs.zpool_command(
        "create", pool_properties=pool_props, filesystem_properties=fs_props, target="my pool"
    ) == (
        "/sbin/zpool create -O quota=107374182400 -o"
        ' comment="jorge\'s comment has a space" "my pool"'
    )


@pytest.mark.usefixtures("zfs_cmd_mock")
def test_zpool_command_property():
    """
    Test if zpool_command builds the correct string
    """
    assert (
        zfs.zpool_command("get", property_name="comment", target="mypool")
        == "/sbin/zpool get comment mypool"
    )


@pytest.mark.usefixtures("zfs_cmd_mock")
def test_zpool_command_property_value():
    """
    Test if zpool_command builds the correct string
    """
    my_flags = [
        "-v",  # verbose
    ]
    assert (
        zfs.zpool_command("iostat", flags=my_flags, target=["mypool", 60, 1])
        == "/sbin/zpool iostat -v mypool 60 1"
    )


@pytest.mark.usefixtures("zfs_cmd_mock")
def test_parse_command_result_success():
    """
    Test if parse_command_result returns the expected result
    """
    res = {}
    res["retcode"] = 0
    res["stderr"] = ""
    res["stdout"] = ""
    assert zfs.parse_command_result(res, "tested") == OrderedDict([("tested", True)])


@pytest.mark.usefixtures("zfs_cmd_mock")
def test_parse_command_result_success_nolabel():
    """
    Test if parse_command_result returns the expected result
    """
    res = {}
    res["retcode"] = 0
    res["stderr"] = ""
    res["stdout"] = ""
    assert zfs.parse_command_result(res) == OrderedDict()


@pytest.mark.usefixtures("zfs_cmd_mock")
def test_parse_command_result_fail():
    """
    Test if parse_command_result returns the expected result on failure
    """
    res = {}
    res["retcode"] = 1
    res["stderr"] = ""
    res["stdout"] = ""
    assert zfs.parse_command_result(res, "tested") == OrderedDict([("tested", False)])


@pytest.mark.usefixtures("zfs_cmd_mock")
def test_parse_command_result_nolabel():
    """
    Test if parse_command_result returns the expected result on failure
    """
    res = {}
    res["retcode"] = 1
    res["stderr"] = ""
    res["stdout"] = ""
    assert zfs.parse_command_result(res) == OrderedDict()


@pytest.mark.usefixtures("zfs_cmd_mock")
def test_parse_command_result_fail_message():
    """
    Test if parse_command_result returns the expected result on failure with stderr
    """
    res = {}
    res["retcode"] = 1
    res["stderr"] = "\n".join(["ice is not hot", "usage:", "this should not be printed"])
    res["stdout"] = ""
    assert zfs.parse_command_result(res, "tested") == OrderedDict(
        [("tested", False), ("error", "ice is not hot")]
    )


@pytest.mark.usefixtures("zfs_cmd_mock")
def test_parse_command_result_fail_message_nolabel():
    """
    Test if parse_command_result returns the expected result on failure with stderr
    """
    res = {}
    res["retcode"] = 1
    res["stderr"] = "\n".join(["ice is not hot", "usage:", "this should not be printed"])
    res["stdout"] = ""
    assert zfs.parse_command_result(res) == OrderedDict([("error", "ice is not hot")])
