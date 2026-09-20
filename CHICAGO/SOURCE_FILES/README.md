# Chicago canonical original source archive

This is the canonical original source package for **CHICAGO — Episode 1 of Hidden Industrial America**. It is a source package, not the final YouTube publication master.

## Identity

- Original filename: `Hidden_Industrial_America_Chicago_CODEX_READY_v7.rar`
- Exact size: `4,741,988,746` bytes (`4.416319304 GiB`)
- SHA-256: `2fcfcd4767ce0d6234b72a33bde08ea0b5fe0cdb4eb3d9150515cba56ef705eb`
- GitHub Release tag: `chicago-source-archive-v1`
- Release: <https://github.com/reverendstanislav-bot/Youtube-2/releases/tag/chicago-source-archive-v1>

The archive is stored in the Release as a raw binary split. The split does not recompress, unpack, or transform the archive.

## Ordered parts

| Part | Size (bytes) | SHA-256 |
|---|---:|---|
| `Hidden_Industrial_America_Chicago_CODEX_READY_v7.rar.part00` | 1,900,000,000 | `ab58661d982a8789df49f6d431e1e0e9678af7de02d60e8db468988603cc5a79` |
| `Hidden_Industrial_America_Chicago_CODEX_READY_v7.rar.part01` | 1,900,000,000 | `a4525cd68439b0ff143326eb44e168fa516361ae132ebe268f9d423c29ea3297` |
| `Hidden_Industrial_America_Chicago_CODEX_READY_v7.rar.part02` | 941,988,746 | `620c8e160026a8917ea9a8779b620301a514a283a1aad91926c8012ac1ba9899` |

## Reassembly

Download all three parts and one of the scripts from the Release into the same directory.

Windows PowerShell:

```powershell
powershell -ExecutionPolicy Bypass -File .\CHICAGO_REASSEMBLE_WINDOWS.ps1
```

Linux or macOS:

```bash
chmod +x CHICAGO_REASSEMBLE_LINUX_MAC.sh
./CHICAGO_REASSEMBLE_LINUX_MAC.sh
```

Both scripts concatenate the parts in the recorded order, restore the original filename, calculate SHA-256, and exit with an error unless the exact original size and hash match.

Machine-readable details are in [`ORIGINAL_ARCHIVE_MANIFEST.json`](./ORIGINAL_ARCHIVE_MANIFEST.json). The Release also contains `CHICAGO_SOURCE_ARCHIVE_MANIFEST.json` and `SHA256SUMS.txt`.
