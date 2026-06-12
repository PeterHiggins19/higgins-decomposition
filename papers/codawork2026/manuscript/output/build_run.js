// Wrapper that re-exports the build by re-requiring the canonical build script.
// Used to force the bash mount to re-read the canonical build_docx.js on a fresh inode.
// (Workaround for SMB cache-lag observed during 2026-05-17 manuscript rebuild.)
require("/sessions/epic-gracious-lovelace/mnt/Claude CoWorker/Current-Repo/Hs/papers/codawork2026/manuscript/build/build_docx.js");
