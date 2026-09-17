#!/usr/bin/env python3
"""Download the six public S-Seg-RLVR pathology datasets.

  python scripts/download_pathology_datasets.py
  python scripts/download_pathology_datasets.py --only pannuke,monuseg
  python scripts/download_pathology_datasets.py --dry-run
  python scripts/download_pathology_datasets.py --out data/pathology

Writes <out>/{pannuke,consep,monuseg,lizard,glas,crag}/. Default --out is
data/pathology (gitignored). Existing files are skipped; never commit zips.
Warwick-gated sets need WARWICK_USER and WARWICK_PASS; otherwise the script
prints the exact browser steps and exits non-zero (it will not fake a zip).
PanNuke and MoNuSeg are CC BY-NC-SA 4.0 — research / non-commercial only.
Optional: --max-bytes N skips any file whose Content-Length exceeds N.
"""

from __future__ import annotations

import argparse
import http.cookiejar
import os
import re
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import dataclass
from enum import Enum
from html.parser import HTMLParser
from pathlib import Path
from typing import Callable

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUT = ROOT / "data" / "pathology"
USER_AGENT = "S-Seg-RLVR-dataset-bot/0.1 (research; educational; contact via GitHub repo)"
CHUNK = 1024 * 1024
TIMEOUT = 120.0
ARCHIVE_SUFFIXES = (".zip", ".tar", ".tar.gz", ".tgz", ".rar", ".7z", ".npy", ".npz")
DIRECT_SUFFIXES = ARCHIVE_SUFFIXES + (".m", ".pdf", ".xlsx", ".xls", ".csv", ".txt")
DRIVE_HOSTS = ("drive.google.com", "drive.usercontent.google.com")
DRIVE_ID_RE = re.compile(r"(?:/file/d/|/d/)([A-Za-z0-9_-]+)|[?&]id=([A-Za-z0-9_-]+)")
NCSA_MARK = "CC BY-NC-SA 4.0"


class Auth(str, Enum):
    NONE = "none"
    WARWICK = "warwick"
    GRAND_CHALLENGE = "grand_challenge"


class SkipTooLarge(RuntimeError):
    """File is larger than --max-bytes; not a download failure."""


@dataclass(frozen=True)
class DatasetSpec:
    id: str
    dest_subdir: str
    source_urls: tuple[str, ...]
    fetch_notes: str
    auth: Auth
    license_note: str


# Registry: one row per dataset. CLI and auth/download dispatch from these
# fields only — do not add per-id branches below.
DATASETS: tuple[DatasetSpec, ...] = (
    DatasetSpec(
        id="pannuke",
        dest_subdir="pannuke",
        source_urls=(
            "https://warwick.ac.uk/fac/cross_fac/tia/data/pannuke/fold_1.zip",
            "https://warwick.ac.uk/fac/cross_fac/tia/data/pannuke/fold_2.zip",
            "https://warwick.ac.uk/fac/cross_fac/tia/data/pannuke/fold_3.zip",
        ),
        fetch_notes="Open TIA PanNuke page (no sign-in): https://warwick.ac.uk/fac/cross_fac/tia/data/pannuke",
        auth=Auth.NONE,
        license_note="CC BY-NC-SA 4.0; research only; commercial use not allowed; cite Gamper et al. 2019 and 2020.",
    ),
    DatasetSpec(
        id="consep",
        dest_subdir="consep",
        source_urls=("https://warwick.ac.uk/TIA/data/hovernet/",),
        fetch_notes=(
            "Warwick sign-in wall. Manual steps:\n"
            "  1. Open https://warwick.ac.uk/TIA/data/hovernet/ "
            "(paper also cites https://warwick.ac.uk/fac/sci/dcs/research/tia/data/).\n"
            "  2. Sign in with a Warwick ITS / Entra ID account.\n"
            "  3. Download the CoNSeP archive listed on that page.\n"
            "  4. Save it under {dest}/ (do not commit the zip).\n"
            "  5. If the zip is not on the page, email tia@warwick.ac.uk.\n"
            "Re-run this script afterwards; present files are skipped."
        ),
        auth=Auth.WARWICK,
        license_note="Not stated in the HoVer-Net PDF; look up on the official page after sign-in.",
    ),
    DatasetSpec(
        id="monuseg",
        dest_subdir="monuseg",
        source_urls=(
            "https://drive.google.com/uc?export=download&id=1ZgqFJomqQGNnsx7w7QBzQQMVA16lbVCA#MoNuSeg_2018_Training_data.zip",
            "https://drive.google.com/uc?export=download&id=1NKkSQ5T0ZNQ8aUhh0a8Dt2YKYCQXIViw#MoNuSeg_2018_Testing_data.zip",
            "https://drive.google.com/uc?export=download&id=1xYyQ31CHFRnvTCTuuHdconlJCMk2SK7Z#Training_Patient_Organ_information.pdf",
            "https://drive.google.com/uc?export=download&id=1YDtIiLZX0lQzZp_JbqneHXHvRo45ZWGX#HE_to_binary_nary_masks.m",
        ),
        fetch_notes=(
            "Official Data page (open): https://monuseg.grand-challenge.org/Data/\n"
            "Files are the Google Drive links on that page. A Grand Challenge account "
            "is only needed if a link starts requiring sign-in; then register at "
            "grand-challenge.org, download the zips, and place them in {dest}/.\n"
            "Optional: GRAND_CHALLENGE_TOKEN for API-style Authorization headers."
        ),
        auth=Auth.GRAND_CHALLENGE,
        license_note="CC BY-NC-SA 4.0 (official MoNuSeg Data page).",
    ),
    DatasetSpec(
        id="lizard",
        dest_subdir="lizard",
        source_urls=("https://warwick.ac.uk/fac/cross_fac/tia/data/lizard",),
        fetch_notes=(
            "Warwick sign-in wall. Manual steps:\n"
            "  1. Open https://warwick.ac.uk/fac/cross_fac/tia/data/lizard "
            "(paper: warwick.ac.uk/lizard-dataset).\n"
            "  2. Sign in with a Warwick ITS / Entra ID account.\n"
            "  3. Download the Lizard archive listed on that page.\n"
            "  4. Save it under {dest}/ (do not commit the zip).\n"
            "  5. If the zip is not on the page, email tia@warwick.ac.uk.\n"
            "Re-run this script afterwards; present files are skipped."
        ),
        auth=Auth.WARWICK,
        license_note="Not stated in the Lizard PDF; look up on the official page after sign-in.",
    ),
    DatasetSpec(
        id="glas",
        dest_subdir="glas",
        source_urls=("https://warwick.ac.uk/fac/cross_fac/tia/data/glascontest",),
        fetch_notes=(
            "Warwick sign-in wall. Manual steps:\n"
            "  1. Open https://warwick.ac.uk/fac/cross_fac/tia/data/glascontest "
            "(paper: http://www.warwick.ac.uk/bialab/GlasContest/).\n"
            "  2. Sign in with a Warwick ITS / Entra ID account.\n"
            "  3. Download the GlaS contest archive listed on that page.\n"
            "  4. Save it under {dest}/ (do not commit the zip).\n"
            "  5. If the zip is not on the page, email tia@warwick.ac.uk.\n"
            "Re-run this script afterwards; present files are skipped."
        ),
        auth=Auth.WARWICK,
        license_note="Paper: research use. Named dataset licence: look up on the official page (manuscript CC BY-NC-ND 4.0 is the paper, not the dataset).",
    ),
    DatasetSpec(
        id="crag",
        dest_subdir="crag",
        source_urls=("https://warwick.ac.uk/fac/sci/dcs/research/tia/data/mildnet",),
        fetch_notes=(
            "Warwick sign-in wall. Manual steps:\n"
            "  1. Open https://warwick.ac.uk/fac/sci/dcs/research/tia/data/mildnet "
            "(cross_fac twin may 403 the same way).\n"
            "  2. Sign in with a Warwick ITS / Entra ID account.\n"
            "  3. Download the CRAG archive listed on that page.\n"
            "  4. Save it under {dest}/ (do not commit the zip).\n"
            "  5. If the zip is not on the page, email tia@warwick.ac.uk.\n"
            "Re-run this script afterwards; present files are skipped."
        ),
        auth=Auth.WARWICK,
        license_note="Not stated in the MILD-Net PDF; look up on the official page after sign-in.",
    ),
)

DATASETS_BY_ID = {spec.id: spec for spec in DATASETS}


def credentials_ready(auth: Auth) -> bool:
    checks: dict[Auth, Callable[[], bool]] = {
        Auth.NONE: lambda: True,
        Auth.WARWICK: lambda: bool(os.environ.get("WARWICK_USER") and os.environ.get("WARWICK_PASS")),
        # Public Data-page Drive links; token only if a host later requires it.
        Auth.GRAND_CHALLENGE: lambda: True,
    }
    return checks[auth]()


def missing_auth_hint(auth: Auth) -> str:
    hints = {
        Auth.NONE: "",
        Auth.WARWICK: "Set WARWICK_USER and WARWICK_PASS, or follow the manual steps.",
        Auth.GRAND_CHALLENGE: "Sign in at grand-challenge.org if a link requires it.",
    }
    return hints[auth]


@dataclass(frozen=True)
class PlannedFetch:
    spec: DatasetSpec
    dest: Path
    url: str
    is_dir: bool


def dest_filename(url: str) -> str | None:
    parsed = urllib.parse.urlparse(url)
    if parsed.fragment:
        return parsed.fragment
    name = Path(parsed.path).name
    if name and name.lower().endswith(DIRECT_SUFFIXES):
        return name
    return None


def planned_fetches(spec: DatasetSpec, out_root: Path) -> list[PlannedFetch]:
    dest_dir = out_root / spec.dest_subdir
    rows: list[PlannedFetch] = []
    for url in spec.source_urls:
        name = dest_filename(url)
        dest = dest_dir / name if name else dest_dir
        rows.append(PlannedFetch(spec, dest, url, name is None))
    if not rows:
        rows.append(PlannedFetch(spec, dest_dir, spec.fetch_notes, True))
    return rows


def already_present(fetch: PlannedFetch) -> bool:
    dest = fetch.dest
    if fetch.is_dir:
        if not dest.is_dir():
            return False
        return any(
            p.is_file() and p.stat().st_size > 0 and not p.name.endswith(".part")
            for p in dest.iterdir()
        )
    return dest.is_file() and dest.stat().st_size > 0


def format_notes(spec: DatasetSpec, dest: Path) -> str:
    return spec.fetch_notes.format(dest=dest)


def print_license_reminders(specs: list[DatasetSpec]) -> None:
    flagged = [s for s in specs if NCSA_MARK in s.license_note]
    if not flagged:
        return
    print(
        f"LICENSE REMINDER: {NCSA_MARK} — research / non-commercial only; "
        "share-alike. Do not use these sets commercially."
    )
    for spec in flagged:
        print(f"  - {spec.id}: {spec.license_note}")
    print()


def select_datasets(only: str | None) -> list[DatasetSpec]:
    if not only:
        return list(DATASETS)
    ids = [part.strip().lower() for part in only.split(",") if part.strip()]
    if not ids:
        raise SystemExit("--only was empty; pass comma-separated ids, e.g. pannuke,monuseg")
    unknown = [i for i in ids if i not in DATASETS_BY_ID]
    if unknown:
        known = ", ".join(DATASETS_BY_ID)
        raise SystemExit(f"Unknown dataset id(s): {', '.join(unknown)}. Known: {known}")
    return [DATASETS_BY_ID[i] for i in ids]


def looks_like_html(data: bytes) -> bool:
    head = data.lstrip()[:256].lower()
    return head.startswith(b"<!doctype html") or head.startswith(b"<html") or b"<html" in head


def looks_like_login(url: str, data: bytes) -> bool:
    text = data[:4000].decode("utf-8", errors="ignore").lower()
    host = urllib.parse.urlparse(url).netloc.lower()
    return (
        "websignon.warwick.ac.uk" in host
        or "login-form" in text
        or "id=\"loginform\"" in text
        or "/accounts/login" in text
        or "grand-challenge.org/accounts/" in text
    )


class _HrefParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.hrefs: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag != "a":
            return
        href = dict(attrs).get("href")
        if href:
            self.hrefs.append(href)


def archive_links_from_html(page_url: str, html: str) -> list[str]:
    parser = _HrefParser()
    parser.feed(html)
    found: list[str] = []
    for href in parser.hrefs:
        absolute = urllib.parse.urljoin(page_url, href)
        path = urllib.parse.urlparse(absolute).path.lower()
        if path.endswith(ARCHIVE_SUFFIXES):
            found.append(absolute)
    # Preserve order, drop duplicates.
    return list(dict.fromkeys(found))


def drive_id(url: str) -> str | None:
    match = DRIVE_ID_RE.search(url)
    if not match:
        return None
    return match.group(1) or match.group(2)


def is_drive_url(url: str) -> bool:
    host = urllib.parse.urlparse(url).netloc.lower()
    return any(host == h or host.endswith("." + h) for h in DRIVE_HOSTS) or bool(drive_id(url) and "drive.google" in host)


def default_headers(spec: DatasetSpec) -> dict[str, str]:
    headers = {"User-Agent": USER_AGENT}
    if spec.auth is Auth.GRAND_CHALLENGE:
        token = os.environ.get("GRAND_CHALLENGE_TOKEN", "").strip()
        if token:
            headers["Authorization"] = f"Bearer {token}"
    return headers


def make_opener(spec: DatasetSpec) -> urllib.request.OpenerDirector:
    handlers: list[urllib.request.BaseHandler] = [
        urllib.request.HTTPCookieProcessor(http.cookiejar.CookieJar()),
    ]
    if spec.auth is Auth.WARWICK:
        user = os.environ.get("WARWICK_USER", "")
        password = os.environ.get("WARWICK_PASS", "")
        mgr = urllib.request.HTTPPasswordMgrWithDefaultRealm()
        for host in ("https://warwick.ac.uk", "https://websignon.warwick.ac.uk"):
            mgr.add_password(None, host, user, password)
        handlers.append(urllib.request.HTTPBasicAuthHandler(mgr))
    return urllib.request.build_opener(*handlers)


def request(url: str, spec: DatasetSpec, extra: dict[str, str] | None = None) -> urllib.request.Request:
    headers = default_headers(spec)
    if extra:
        headers.update(extra)
    return urllib.request.Request(url, headers=headers)


def content_length(url: str, spec: DatasetSpec, opener: urllib.request.OpenerDirector) -> int | None:
    fetch_url = url.split("#", 1)[0]
    if is_drive_url(fetch_url) and drive_id(fetch_url):
        fetch_url = (
            "https://drive.google.com/uc?export=download&id="
            f"{drive_id(fetch_url)}&confirm=t"
        )
    req = request(fetch_url, spec)
    req.get_method = lambda: "HEAD"  # type: ignore[method-assign]
    try:
        with opener.open(req, timeout=TIMEOUT) as resp:
            value = resp.headers.get("Content-Length")
            if value and value.isdigit():
                return int(value)
    except (urllib.error.HTTPError, urllib.error.URLError, TimeoutError, OSError):
        return None
    return None


def parse_drive_confirm(html: str, cookies: http.cookiejar.CookieJar | None = None) -> str | None:
    if cookies is not None:
        for cookie in cookies:
            if "download_warning" in cookie.name.lower():
                return cookie.value
    for pattern in (
        r"confirm=([0-9A-Za-z_-]+)",
        r'name=["\']confirm["\']\s+value=["\']([^"\']+)["\']',
        r'data-confirm=["\']([^"\']+)["\']',
    ):
        match = re.search(pattern, html)
        if match:
            return match.group(1)
    return None


def opener_cookiejar(opener: urllib.request.OpenerDirector) -> http.cookiejar.CookieJar | None:
    for handler in opener.handlers:
        jar = getattr(handler, "cookiejar", None)
        if isinstance(jar, http.cookiejar.CookieJar):
            return jar
    return None


def open_data_response(
    url: str,
    spec: DatasetSpec,
    opener: urllib.request.OpenerDirector,
    extra: dict[str, str] | None = None,
):
    fetch_url = url.split("#", 1)[0]
    if is_drive_url(fetch_url) and drive_id(fetch_url):
        file_id = drive_id(fetch_url)
        fetch_url = f"https://drive.google.com/uc?export=download&id={file_id}&confirm=t"
    resp = opener.open(request(fetch_url, spec, extra), timeout=TIMEOUT)
    content_type = (resp.headers.get("Content-Type") or "").lower()
    if "text/html" not in content_type and "application/xhtml" not in content_type:
        return resp

    preview = resp.read(65536)
    remainder = resp.read()
    html = (preview + remainder).decode("utf-8", errors="ignore")
    resp.close()
    if is_drive_url(url) and drive_id(url):
        token = parse_drive_confirm(html, opener_cookiejar(opener))
        if token:
            retry = (
                f"https://drive.google.com/uc?export=download&id={drive_id(url)}"
                f"&confirm={token}"
            )
            return opener.open(request(retry, spec, extra), timeout=TIMEOUT)
    final_url = getattr(resp, "geturl", lambda: fetch_url)()
    if looks_like_html(preview) or looks_like_login(final_url, preview):
        raise RuntimeError(
            "received an HTML login / interstitial page instead of a data file"
        )
    raise RuntimeError(f"unexpected HTML response from {fetch_url}")


def _reject_if_too_large(declared: int | None, written: int, max_bytes: int) -> None:
    if max_bytes <= 0:
        return
    if declared is not None and declared > max_bytes:
        raise SkipTooLarge(f"{declared} bytes > --max-bytes {max_bytes}")
    if written > max_bytes:
        raise SkipTooLarge(f"streamed {written} bytes > --max-bytes {max_bytes}")


def stream_to_dest(resp, dest: Path, max_bytes: int = 0) -> int:
    dest.parent.mkdir(parents=True, exist_ok=True)
    part = dest.with_name(dest.name + ".part")
    declared = None
    cl = resp.headers.get("Content-Length")
    if cl and cl.isdigit():
        declared = int(cl)
    _reject_if_too_large(declared, 0, max_bytes)
    written = 0
    try:
        with part.open("wb") as handle:
            while True:
                chunk = resp.read(CHUNK)
                if not chunk:
                    break
                if written == 0 and looks_like_html(chunk):
                    raise RuntimeError("got HTML instead of a data file (login wall or virus-scan page)")
                handle.write(chunk)
                written += len(chunk)
                _reject_if_too_large(None, written, max_bytes)
        if written < 1:
            raise RuntimeError("empty download")
        part.replace(dest)
        return written
    except Exception:
        part.unlink(missing_ok=True)
        raise


def download_url(
    url: str,
    dest: Path,
    spec: DatasetSpec,
    opener: urllib.request.OpenerDirector,
    max_bytes: int = 0,
) -> int:
    dest.parent.mkdir(parents=True, exist_ok=True)
    extra: dict[str, str] = {}
    part = dest.with_name(dest.name + ".part")
    if part.exists() and part.stat().st_size > 0 and not is_drive_url(url):
        extra["Range"] = f"bytes={part.stat().st_size}-"
        # Range resume is best-effort; if the server ignores it we restart.
        try:
            resp = open_data_response(url, spec, opener, extra)
            if resp.status == 206:
                with part.open("ab") as handle, resp:
                    while True:
                        chunk = resp.read(CHUNK)
                        if not chunk:
                            break
                        handle.write(chunk)
                        _reject_if_too_large(None, part.stat().st_size, max_bytes)
                part.replace(dest)
                return dest.stat().st_size
            resp.close()
        except SkipTooLarge:
            part.unlink(missing_ok=True)
            raise
        except (urllib.error.HTTPError, urllib.error.URLError, RuntimeError):
            extra.pop("Range", None)
        part.unlink(missing_ok=True)
    with open_data_response(url, spec, opener, extra or None) as resp:
        return stream_to_dest(resp, dest, max_bytes=max_bytes)


def download_landing_or_file(
    fetch: PlannedFetch,
    opener: urllib.request.OpenerDirector,
    max_bytes: int = 0,
) -> list[tuple[Path, int]]:
    """Download a direct file, or discover archive links on a landing page."""
    spec = fetch.spec
    if not fetch.is_dir:
        return [(fetch.dest, download_url(fetch.url, fetch.dest, spec, opener, max_bytes))]

    page_url = fetch.url.split("#", 1)[0]
    with opener.open(request(page_url, spec), timeout=TIMEOUT) as resp:
        body = resp.read()
        final_url = resp.geturl()
    if looks_like_html(body) and looks_like_login(final_url, body):
        raise RuntimeError(
            "Warwick/host SSO login wall still present (HTTP Basic is not enough for Entra ID)"
        )
    if not looks_like_html(body):
        # Unexpected binary at a landing URL — refuse to invent a filename.
        raise RuntimeError("landing URL returned a binary body; place the file in the dest folder manually")

    links = archive_links_from_html(final_url, body.decode("utf-8", errors="ignore"))
    if not links:
        raise RuntimeError("signed-in page had no .zip/.tar archive links")
    written: list[tuple[Path, int]] = []
    for link in links:
        name = dest_filename(link) or Path(urllib.parse.urlparse(link).path).name
        dest = fetch.dest / name
        if dest.is_file() and dest.stat().st_size > 0:
            print(f"  EXISTS  dest={dest} url={link} auth={spec.auth.value}")
            continue
        written.append((dest, download_url(link, dest, spec, opener, max_bytes)))
    return written


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Download the six public S-Seg-RLVR pathology datasets into <out>/<id>/.",
        epilog="Registry-driven: add or edit DatasetSpec rows in DATASETS; do not add per-dataset if/else.",
    )
    parser.add_argument(
        "--out",
        type=Path,
        default=DEFAULT_OUT,
        help=f"Root directory (default: {DEFAULT_OUT})",
    )
    parser.add_argument(
        "--only",
        help="Comma-separated dataset ids (pannuke,consep,monuseg,lizard,glas,crag)",
    )
    parser.add_argument("--dry-run", action="store_true", help="Print dest + URL + auth; write nothing")
    parser.add_argument("--force", action="store_true", help="Re-download even if the dest file exists")
    parser.add_argument(
        "--max-bytes",
        type=int,
        default=0,
        help="Skip a file when HEAD Content-Length exceeds N (0 = no limit). Safety valve for huge folds.",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    specs = select_datasets(args.only)
    print_license_reminders(specs)

    downloaded = existed = skipped_auth = skipped_size = failed = 0

    for spec in specs:
        opener = make_opener(spec)
        for fetch in planned_fetches(spec, args.out):
            label = f"{spec.id:8} dest={fetch.dest} url={fetch.url} auth={spec.auth.value}"
            if already_present(fetch) and not args.force:
                print(f"EXISTS   {label}")
                existed += 1
                continue
            if args.dry_run:
                print(f"DRY-RUN  {label}")
                continue
            if not credentials_ready(spec.auth):
                print(f"SKIP     {label}")
                print(format_notes(spec, fetch.dest if fetch.is_dir else fetch.dest.parent))
                print(f"         {missing_auth_hint(spec.auth)}")
                skipped_auth += 1
                continue
            if args.max_bytes > 0 and not fetch.is_dir:
                size = content_length(fetch.url, spec, opener)
                if size is not None and size > args.max_bytes:
                    print(f"SKIP     {label} ({size} bytes > --max-bytes {args.max_bytes})")
                    skipped_size += 1
                    continue
            try:
                print(f"GET      {label} ...", flush=True)
                results = download_landing_or_file(fetch, opener, max_bytes=args.max_bytes)
                for dest, nbytes in results:
                    print(f"OK       dest={dest} bytes={nbytes} auth={spec.auth.value}")
                    downloaded += 1
                if not results:
                    # Landing page, all discovered files already present.
                    existed += 1
            except SkipTooLarge as exc:
                print(f"SKIP     {label} ({exc})")
                skipped_size += 1
            except (urllib.error.URLError, urllib.error.HTTPError, TimeoutError, RuntimeError, OSError) as exc:
                print(f"FAIL     {label}: {exc}")
                print(format_notes(spec, fetch.dest if fetch.is_dir else fetch.dest.parent))
                failed += 1

    print(
        f"\nSummary: downloaded={downloaded} existed={existed} "
        f"skipped_auth={skipped_auth} skipped_size={skipped_size} failed={failed}"
    )
    if skipped_auth:
        print("One or more auth-gated sets were skipped (non-zero). No fake archives were written.")
    if failed:
        print("One or more downloads failed. See FAIL lines and the printed manual steps.")
    return 0 if skipped_auth == 0 and failed == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
