import logging
import sys

from rekall import session
from rekall import plugins
from rekall.plugins.windows import common

from rekall import utils

# pylint: disable=protected-access

logging.getLogger().setLevel(logging.DEBUG)

s = session.InteractiveSession()

result = []
for executable in sys.argv[1:]:
    try:
        pe_info = s.plugins.peinfo(executable=executable)
    except IOError:
        continue
    version_information = pe_info.pe_helper.VersionInformationDict()
    prod_version = version_information.get('ProductVersion')
    guid = pe_info.pe_helper.RSDS.GUID_AGE
    name = version_information.get("InternalName")
    pdb_name = str(pe_info.pe_helper.RSDS.Filename)
    if pdb_name in common.KERNEL_NAMES:
        name = "nt"

    profile_name = "%s/GUID/%s" % (name.split(".")[0], guid)
    profile = s.LoadProfile(profile_name)
    if profile:
        row = dict(version=prod_version, guid=guid,
                   arch=profile.metadata("arch"))

        for struct, field in [
            ("_EPROCESS", "VadRoot"),
            ("_EPROCESS", "ImageFileName"),
            ("_KPROCESS", "DirectoryTableBase"),
            ("_TOKEN", "OriginatingLogonSession")]:
            row["%s.%s" % (struct, field)] = profile.get_obj_offset(
                struct, field) or 0

        # Constants
        for constant in ["PsActiveProcessHead", "NtBuildLab",
                         "str:FILE_VERSION", "NtCreateToken"]:
            row[constant] = profile.get_constant("PsActiveProcessHead")

        logging.debug(str(row))

        result.append(row)
    else:
        logging.error("Unable to load profile %s %s", guid, pdb_name)

print utils.PPrint(result)
