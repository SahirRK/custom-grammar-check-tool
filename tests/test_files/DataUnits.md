# Test for data units usage

## Correct usage
- The server has 16 GiB of RAM.
- The file size is 2 TiB.
- The data is 5 Kib.

## Incorrect usage
- The hard drive has a capacity of 1 TB. <!-- Should suggest TiB -->
- The image is 5 mb in size. <!-- Should flag as ambiguous -->
- Avoid tb as it could mean TB, TiB, Tb, or TiB
- Available memory: 8 Gb <!-- Should suggest Gib -->
- The download speed is 500 Kb/s. <!-- Should suggest Kib/s -->
- This device supports up to 2 PB of storage. <!-- Should flag as ambiguous and suggest PiB -->
- The video quality is 1080p at 60 fps, with a bit rate of 5 Mb/s. <!-- Should suggest Mib -->
- 20 EB is large. <!-- Should suggest EiB -->

## Edge cases
- The connection speed is 100 Mb/s. <!-- Should suggest Mib even though Mb may be intended here -->
- The prefix "mega" means million.
- In the context of bits, Mb is correct for megabits.
- In the context of bytes, MB is correct for megabytes.
<!-- You should ignore the suggestions when you mean to use the SI units-->
- The average file size is about 4.5 GB. <!-- Should suggest GiB -->

