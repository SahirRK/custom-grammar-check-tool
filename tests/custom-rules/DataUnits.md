
# Test for data units usage

## Correct usage
- The server has 16 GiB of RAM.
- The file size is 2 TiB.

## Incorrect usage
- The hard drive has a capacity of 1 TB. <!-- Should suggest TiB -->
- The image is 5 mb in size. <!-- Should flag as ambiguous -->
- Available memory: 8 Gb <!-- Should flag as ambiguous and suggest GiB -->

## Edge cases
- The prefix "mega" means million.
- In the context of bits, Mb is correct for megabits.

