# Recovery notes

The Dropbox split payload is recoverable in principle, but the current ChatGPT connector does not provide a safe direct binary bridge from Dropbox into GitHub Releases. Therefore the Git repository now contains the complete integrity manifest and reconstruction tool rather than pretending the bytes were transferred.

The correct future transfer path is:
1. obtain the 14 Dropbox parts locally or through a binary-capable runner;
2. validate them with `tools/reassemble_dropbox_parts.py`;
3. inspect the reconstructed payload with `ffprobe`;
4. publish the recovered legacy source as a **review/source asset**, not as final;
5. repair subtitle timing;
6. build new corrected review;
7. after explicit approval, publish the actual Chicago upload master.

Do not use the 31 KB standalone Dropbox MP4 as a source.
