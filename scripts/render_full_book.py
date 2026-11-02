"""Render and compare every retained and assembled full-book page.

Examples (run at the repository root):
  python scripts/render_full_book.py sources --jobs 2
  python scripts/render_full_book.py source-pixels
  python scripts/render_full_book.py combined
  python scripts/render_full_book.py compare
  python scripts/render_full_book.py proofs

All evidence is ignored under build/full-book/raster. Source PDFs are immutable.
The combined stage requires a hash-bound pagination.json from the stable build.
An exact comparison excludes only the footer below 225 mm; it does not assert
that new pages, changed pages, or folios have received human visual review.
"""
from __future__ import annotations

import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
import hashlib
import json
import math
import os
from pathlib import Path
import shutil
import struct
import subprocess
import sys
import zlib


ROOT = Path(__file__).resolve().parents[1]
DPI = 150
CUTOFF_MM = 225
CUTOFF_ROW = math.floor(CUTOFF_MM * DPI / 25.4)
GUARD_FIRST_MM, GUARD_LAST_MM = 224, 226
GS_FLAGS = ["-sDEVICE=png16m", "-r150", "-dTextAlphaBits=4",
            "-dGraphicsAlphaBits=4", "-dSAFER", "-dBATCH", "-dNOPAUSE"]
PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"


def stamp():
    return datetime.now(timezone.utc).isoformat()


def digest(path):
    h = hashlib.sha256()
    with Path(path).open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def relative(path):
    return Path(path).resolve().relative_to(ROOT).as_posix()


def write_json(path, value):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n",
                         encoding="utf-8", newline="\n")
    temporary.replace(path)


def read_json(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def run(args, **kwargs):
    options = {"creationflags": subprocess.CREATE_NO_WINDOW} if os.name == "nt" else {}
    return subprocess.run([str(a) for a in args], cwd=ROOT, **options, **kwargs)


def ghostscript(explicit=None):
    resources = []
    if explicit:
        executable = Path(explicit).resolve()
    else:
        located = next((shutil.which(name) for name in ("gswin64c", "gs", "rungs")
                        if shutil.which(name)), None)
        if not located:
            raise RuntimeError("Ghostscript is required (gswin64c, gs, or rungs).")
        executable = Path(located).resolve()
        if executable.stem.lower() == "rungs":
            bundled = executable.parents[2] / "tlpkg/tlgs/bin/gswin64c.exe"
            if bundled.exists():
                executable = bundled
    gsroot = executable.parent.parent
    if (gsroot / "Resource/Init").is_dir():
        resources = [str(gsroot / p) for p in ("Resource/Init", "lib", "kanji")]
    prefix = [str(executable)]
    if resources:
        prefix.append("-I" + os.pathsep.join(resources))
    version = run(prefix + ["--version"], capture_output=True, text=True,
                  encoding="utf-8", errors="replace")
    if version.returncode:
        raise RuntimeError(version.stderr)
    return {"executable": str(executable), "executable_sha256": digest(executable),
            "version": version.stdout.strip(), "resource_paths": resources,
            "prefix": prefix, "flags": GS_FLAGS, "dpi": DPI,
            "device": "png16m", "channels": "RGB", "bits_per_channel": 8,
            "footer_cutoff_mm": CUTOFF_MM, "compared_rows": CUTOFF_ROW}


def load_png(path):
    """Read validated noninterlaced RGB8 PNG scanlines, without third-party code."""
    data = Path(path).read_bytes()
    if not data.startswith(PNG_SIGNATURE):
        raise ValueError(f"Not a PNG: {path}")
    offset, header, idat, ended = 8, None, [], False
    physical = None
    while offset < len(data):
        if offset + 12 > len(data):
            raise ValueError(f"Truncated PNG chunk: {path}")
        size = struct.unpack_from(">I", data, offset)[0]
        kind = data[offset + 4:offset + 8]
        payload = data[offset + 8:offset + 8 + size]
        if offset + 12 + size > len(data):
            raise ValueError(f"Truncated PNG payload: {path}")
        crc = struct.unpack_from(">I", data, offset + 8 + size)[0]
        if zlib.crc32(kind + payload) & 0xffffffff != crc:
            raise ValueError(f"Bad PNG CRC: {path}")
        if kind == b"IHDR":
            if header is not None or size != 13:
                raise ValueError("Invalid IHDR")
            header = payload
        elif kind == b"IDAT":
            idat.append(payload)
        elif kind == b"pHYs":
            physical = struct.unpack(">IIB", payload)
        elif kind == b"IEND":
            ended = True
            break
        offset += size + 12
    if not header or not ended:
        raise ValueError(f"Missing PNG header/end: {path}")
    width, height, depth, colour, compression, filtering, interlace = struct.unpack(">IIBBBBB", header)
    if (depth, colour, compression, filtering, interlace) != (8, 2, 0, 0, 0):
        raise ValueError(f"Expected noninterlaced RGB8 PNG: {path}")
    scanlines = zlib.decompress(b"".join(idat))
    stride = width * 3 + 1
    if len(scanlines) != stride * height:
        raise ValueError(f"Wrong decompressed PNG size: {path}")
    return {"ihdr": header, "width": width, "height": height, "stride": stride,
            "scanlines": scanlines, "physical": physical,
            "png_sha256": hashlib.sha256(data).hexdigest()}


def png_record(path, page):
    png = load_png(path)
    if png["height"] <= CUTOFF_ROW:
        raise ValueError(f"Page ends above footer cutoff: {path}")
    if abs(png["width"] - 165 * DPI / 25.4) > 1 or abs(png["height"] - 241 * DPI / 25.4) > 1:
        raise ValueError(f"Page is not the contracted 165 x 241 mm size: {path}")
    if png["physical"] and (png["physical"][2] != 1 or
                            any(abs(v * .0254 - DPI) > .1 for v in png["physical"][:2])):
        raise ValueError(f"Unexpected PNG resolution: {path}")
    prefix = png["scanlines"][:png["stride"] * CUTOFF_ROW]
    return {"page": page, "path": relative(path), "sha256": png["png_sha256"],
            "width": png["width"], "height": png["height"], "rgb_bit_depth": 8,
            "compared_rows": CUTOFF_ROW,
            "filtered_scanline_prefix_sha256": hashlib.sha256(prefix).hexdigest()}


def render_job(job, settings, output):
    pdf = ROOT / job["pdf"]
    if digest(pdf) != job["sha256"]:
        raise ValueError(f"PDF differs from declared input: {job['id']}")
    identity = {"pdf_sha256": job["sha256"], "settings": settings}
    identity_hash = hashlib.sha256(json.dumps(identity, sort_keys=True).encode()).hexdigest()
    folder = output / job["category"] / job["id"].replace("/", "--") / identity_hash[:20]
    witness = folder / "render.json"
    if witness.exists():
        previous = read_json(witness)
        if previous["identity"] != identity or previous["pages"] != job["pages"]:
            raise ValueError(f"Existing render identity disagrees: {folder}")
        for page in previous["images"]:
            if digest(ROOT / page["path"]) != page["sha256"]:
                raise ValueError(f"Existing raster changed: {page['path']}")
        return previous
    folder.mkdir(parents=True, exist_ok=True)
    command = settings["prefix"] + settings["flags"] + [
        "-sOutputFile=" + str(folder / "page-%04d.png"), str(pdf)]
    with (folder / "ghostscript.log").open("w", encoding="utf-8", newline="\n") as log:
        result = run(command, stdout=log, stderr=subprocess.STDOUT)
    if result.returncode:
        raise RuntimeError(f"Ghostscript failed for {job['id']}; see {folder / 'ghostscript.log'}")
    paths = sorted(folder.glob("page-*.png"))
    if len(paths) != job["pages"]:
        raise ValueError(f"Page count mismatch for {job['id']}: {len(paths)} != {job['pages']}")
    if digest(pdf) != job["sha256"]:
        raise ValueError(f"PDF changed during render: {job['id']}")
    result = {"id": job["id"], "category": job["category"], "pdf": job["pdf"],
              "pdf_sha256": job["sha256"], "pages": job["pages"], "identity": identity,
              "rendered_utc": stamp(), "command": command,
              "images": [png_record(path, number) for number, path in enumerate(paths, 1)],
              "human_visual_review": "not_performed_by_renderer"}
    write_json(witness, result)
    return result


def render_jobs(jobs, settings, output, workers, manifest_name, input_identity):
    manifest = {"schema_version": 1, "started_utc": stamp(), "input": input_identity,
                "render_settings": settings, "documents": {}, "errors": {}}
    with ThreadPoolExecutor(max_workers=workers) as pool:
        futures = {pool.submit(render_job, job, settings, output): job for job in jobs}
        for future in as_completed(futures):
            job = futures[future]
            try:
                record = future.result()
                manifest["documents"][job["id"]] = record
                print(f"Rendered {job['id']}: {record['pages']} pages", flush=True)
            except Exception as error:
                manifest["errors"][job["id"]] = str(error)
                print(f"FAILED {job['id']}: {error}", flush=True)
            write_json(output / manifest_name, manifest)
    manifest["finished_utc"] = stamp()
    manifest["pages"] = sum(v["pages"] for v in manifest["documents"].values())
    manifest["complete"] = not manifest["errors"] and len(manifest["documents"]) == len(jobs)
    write_json(output / manifest_name, manifest)
    if not manifest["complete"]:
        raise RuntimeError(f"Render errors recorded in {output / manifest_name}")
    return manifest


def render_sources(args):
    contents = read_json(args.contents)
    components = contents["components"]
    if args.select:
        selected = set(args.select.split(","))
        components = [c for c in components if c["component_id"] in selected]
        if {c["component_id"] for c in components} != selected:
            raise ValueError("Unknown component in --select")
    jobs = [{"id": c["component_id"], "category": "sources",
             "pdf": c["sources"]["pdf"]["path"], "sha256": c["sources"]["pdf"]["sha256"],
             "pages": c["standalone_pages"]} for c in components]
    return render_jobs(jobs, ghostscript(args.gs), args.output, args.jobs, "sources.json",
                       {"path": relative(args.contents), "sha256": digest(args.contents),
                        "selection": args.select or "all", "components": len(jobs)})


def pagination_data(args):
    contents, pagination = read_json(args.contents), read_json(args.pagination)
    expected = {c["component_id"]: c for c in contents["components"]}
    seen, page_map = set(), {name: {} for name in pagination["volumes"]}
    for component in pagination["components"]:
        cid = component["component_id"]
        if cid in seen or cid not in expected:
            raise ValueError(f"Unknown or duplicate pagination component: {cid}")
        seen.add(cid)
        source = expected[cid]
        if (component["volume"] != source["volume"] or
                component["source_pdf"] != source["sources"]["pdf"]["path"] or
                component["source_sha256"] != source["sources"]["pdf"]["sha256"] or
                component["source_pages"] != source["standalone_pages"]):
            raise ValueError(f"Pagination/source identity mismatch: {cid}")
        if component["last_page"] - component["first_page"] + 1 != component["source_pages"]:
            raise ValueError(f"Noncontiguous source page mapping: {cid}")
        if component["last_label"] - component["first_label"] + 1 != component["source_pages"]:
            raise ValueError(f"Wrong source label range: {cid}")
        if component["first_label"] % 2 != 1:
            raise ValueError(f"Component does not start recto: {cid}")
        for offset in range(component["source_pages"]):
            physical = component["first_page"] + offset
            target = page_map[component["volume"]]
            if physical in target:
                raise ValueError(f"Overlapping component page: {cid}")
            target[physical] = {"component_id": cid, "source_page": offset + 1,
                                "folio": str(component["first_label"] + offset)}
    if seen != set(expected):
        raise ValueError("Pagination does not contain every accepted component")
    for name, volume in pagination["volumes"].items():
        if "page_labels" in volume and len(volume["page_labels"]) != volume["pages"]:
            raise ValueError(f"PDF page-label list is incomplete: {name}")
        actual_order = [c["component_id"] for c in pagination["components"] if c["volume"] == name]
        if actual_order != contents["volumes"][name]:
            raise ValueError(f"Component order differs from the allowlist: {name}")
        all_pages = set(range(1, volume["pages"] + 1))
        if not set(page_map[name]).issubset(all_pages):
            raise ValueError(f"Mapped page exceeds volume: {name}")
        declared_new = set(volume["new_pages"]) | set(volume["blank_pages"])
        if all_pages - set(page_map[name]) != declared_new:
            raise ValueError(f"New/blank pages do not account for all remaining pages: {name}")
        if digest(ROOT / volume["pdf"]) != volume["sha256"]:
            raise ValueError(f"Combined PDF is not the stable pagination input: {name}")
    return contents, pagination, page_map


def render_combined(args):
    _, pagination, _ = pagination_data(args)
    jobs = [{"id": name, "category": "combined", "pdf": v["pdf"],
             "sha256": v["sha256"], "pages": v["pages"]}
            for name, v in pagination["volumes"].items()]
    return render_jobs(jobs, ghostscript(args.gs), args.output, args.jobs, "combined.json",
                       {"path": relative(args.pagination), "sha256": digest(args.pagination)})


# System.Drawing decodes native RGB values without color management. The helper
# uses exact byte equality, not a visual similarity threshold or hash alone.
# Its generated script and plans are ignored build evidence, not dependencies.
DRAWING_HELPER = r'''
param([Parameter(Mandatory=$true)][string]$PlanPath)
$ErrorActionPreference = 'Stop'
Add-Type -AssemblyName System.Drawing
Add-Type -TypeDefinition @'
using System;
using System.Drawing;
using System.Drawing.Imaging;
using System.Runtime.InteropServices;
using System.Security.Cryptography;
public class PixelFacts {
    public int width, height, compared_rows, guard_first_row, guard_last_row_exclusive;
    public string body_rgb_sha256, full_rgb_sha256;
    public long guard_nonwhite_pixels;
    public int[] guard_nonwhite_box;
}
public class PixelComparison {
    public PixelFacts source, combined;
    public bool dimensions_match, exact_rgb_match;
    public long differing_pixels;
    public int[] differing_box;
}
public static class RasterPixels {
    private class Buffer { public PixelFacts facts; public byte[] rgb; }
    private static string Hash(byte[] data, int count) {
        using (var hash = SHA256.Create()) {
            return BitConverter.ToString(hash.ComputeHash(data, 0, count)).Replace("-", "").ToLowerInvariant();
        }
    }
    private static Buffer Read(string path, int cutoff, int guardFirst, int guardLast) {
        using (var bitmap = new Bitmap(path)) {
            int width = bitmap.Width, height = bitmap.Height;
            if (cutoff > height || guardLast > height) throw new Exception("Invalid cutoff/guard height");
            byte[] rgb = new byte[width * height * 3];
            var data = bitmap.LockBits(new Rectangle(0, 0, width, height), ImageLockMode.ReadOnly, PixelFormat.Format24bppRgb);
            try {
                byte[] row = new byte[Math.Abs(data.Stride)];
                for (int y = 0; y < height; y++) {
                    Marshal.Copy(IntPtr.Add(data.Scan0, y * data.Stride), row, 0, row.Length);
                    int offset = y * width * 3;
                    for (int x = 0; x < width * 3; x += 3) {
                        rgb[offset + x] = row[x + 2];
                        rgb[offset + x + 1] = row[x + 1];
                        rgb[offset + x + 2] = row[x];
                    }
                }
            } finally { bitmap.UnlockBits(data); }
            int xmin = width, ymin = height, xmax = -1, ymax = -1;
            long ink = 0;
            for (int y = guardFirst; y < guardLast; y++) {
                for (int x = 0; x < width; x++) {
                    int p = (y * width + x) * 3;
                    if (rgb[p] != 255 || rgb[p+1] != 255 || rgb[p+2] != 255) {
                        ink++; xmin = Math.Min(xmin, x); xmax = Math.Max(xmax, x);
                        ymin = Math.Min(ymin, y); ymax = Math.Max(ymax, y);
                    }
                }
            }
            var facts = new PixelFacts { width=width, height=height, compared_rows=cutoff,
                body_rgb_sha256=Hash(rgb, cutoff*width*3), full_rgb_sha256=Hash(rgb, rgb.Length),
                guard_first_row=guardFirst, guard_last_row_exclusive=guardLast,
                guard_nonwhite_pixels=ink, guard_nonwhite_box=ink == 0 ? null : new int[]{xmin,ymin,xmax,ymax} };
            return new Buffer { facts=facts, rgb=rgb };
        }
    }
    public static PixelFacts Inspect(string path, int cutoff, int first, int last) {
        return Read(path, cutoff, first, last).facts;
    }
    public static PixelComparison Compare(string oldPath, string newPath, int cutoff, int first, int last) {
        var old = Read(oldPath, cutoff, first, last);
        var current = Read(newPath, cutoff, first, last);
        bool dimensions = old.facts.width == current.facts.width && old.facts.height == current.facts.height;
        var result = new PixelComparison { source=old.facts, combined=current.facts, dimensions_match=dimensions };
        if (!dimensions) { result.differing_pixels=-1; return result; }
        int width=old.facts.width, xmin=width, ymin=cutoff, xmax=-1, ymax=-1;
        long count=0;
        for (int y=0; y<cutoff; y++) {
            for (int x=0; x<width; x++) {
                int p=(y*width+x)*3;
                if (old.rgb[p]!=current.rgb[p] || old.rgb[p+1]!=current.rgb[p+1] || old.rgb[p+2]!=current.rgb[p+2]) {
                    count++; xmin=Math.Min(xmin,x); xmax=Math.Max(xmax,x);
                    ymin=Math.Min(ymin,y); ymax=Math.Max(ymax,y);
                }
            }
        }
        result.exact_rgb_match=count==0;
        result.differing_pixels=count;
        result.differing_box=count==0 ? null : new int[]{xmin,ymin,xmax,ymax};
        return result;
    }
    public static bool CopyEquals(string source, string proof, int x, int y) {
        using (var old = new Bitmap(source)) using (var current = new Bitmap(proof)) {
            var a=old.LockBits(new Rectangle(0,0,old.Width,old.Height), ImageLockMode.ReadOnly, PixelFormat.Format24bppRgb);
            var b=current.LockBits(new Rectangle(x,y,old.Width,old.Height), ImageLockMode.ReadOnly, PixelFormat.Format24bppRgb);
            try {
                byte[] ar=new byte[old.Width*3], br=new byte[old.Width*3];
                for (int row=0; row<old.Height; row++) {
                    Marshal.Copy(IntPtr.Add(a.Scan0,row*a.Stride),ar,0,ar.Length);
                    Marshal.Copy(IntPtr.Add(b.Scan0,row*b.Stride),br,0,br.Length);
                    for (int i=0;i<ar.Length;i++) if(ar[i]!=br[i]) return false;
                }
                return true;
            } finally { old.UnlockBits(a);current.UnlockBits(b); }
        }
    }
}
'@ -ReferencedAssemblies @([System.Drawing.Bitmap].Assembly.Location,
                           [System.Drawing.Rectangle].Assembly.Location,
                           [System.Security.Cryptography.SHA256].Assembly.Location)
$plan = Get-Content -Raw -LiteralPath $PlanPath | ConvertFrom-Json
$writer = [System.IO.StreamWriter]::new($plan.result_path, $false, [System.Text.UTF8Encoding]::new($false))
try {
    if ($plan.mode -eq 'pixels') {
        $n = 0
        foreach ($item in $plan.items) {
            if ($item.source_png) {
                $facts = [RasterPixels]::Compare($item.source_png, $item.png, $plan.cutoff_row, $plan.guard_first_row, $plan.guard_last_row)
                $record = @{ id=$item.id; kind='comparison'; pixels=$facts }
            } else {
                $facts = [RasterPixels]::Inspect($item.png, $plan.cutoff_row, $plan.guard_first_row, $plan.guard_last_row)
                $record = @{ id=$item.id; kind='new_page'; pixels=$facts }
            }
            $writer.WriteLine(($record | ConvertTo-Json -Depth 8 -Compress))
            $n++
            if ($n % 100 -eq 0) { Write-Output "Decoded/checked $n pages" }
        }
    } elseif ($plan.mode -eq 'proofs') {
        $font = [System.Drawing.Font]::new('Arial', 10)
        $titleFont = [System.Drawing.Font]::new('Arial', 15)
        $ink = [System.Drawing.Brushes]::Black
        $rule = [System.Drawing.Pens]::LightGray
        foreach ($group in $plan.groups) {
            $items = @($group.items)
            foreach ($kind in @('contact','folio')) {
                if ($kind -eq 'contact') { $cols=4; $rows=4; $cellW=252; $cellH=402; $top=34 }
                else { $cols=2; $rows=12; $cellW=994; $cellH=126; $top=34 }
                $perSheet=$cols*$rows
                for ($start=0; $start -lt $items.Count; $start+=$perSheet) {
                    $end=[Math]::Min($start+$perSheet,$items.Count)
                    $canvas=[System.Drawing.Bitmap]::new($cols*$cellW,$top+$rows*$cellH)
                    $graphics=[System.Drawing.Graphics]::FromImage($canvas)
                    try {
                        $graphics.Clear([System.Drawing.Color]::White)
                        $graphics.InterpolationMode=[System.Drawing.Drawing2D.InterpolationMode]::HighQualityBicubic
                        $graphics.DrawString(($group.id+' '+$kind+' proof — physical pages '+$items[$start].physical_page+'–'+$items[$end-1].physical_page),$titleFont,$ink,8,5)
                        $ids=@()
                        for ($i=$start; $i -lt $end; $i++) {
                            $item=$items[$i]; $ids+=$item.id
                            $x=(($i-$start)%$cols)*$cellW; $y=$top+[Math]::Floor(($i-$start)/$cols)*$cellH
                            $label=[System.Drawing.RectangleF]::new($x+5,$y+2,$cellW-10,40)
                            $graphics.DrawString($item.label,$font,$ink,$label)
                            $image=[System.Drawing.Image]::FromFile($item.png)
                            try {
                                if ($kind -eq 'contact') {
                                    $dest=[System.Drawing.Rectangle]::new($x+6,$y+45,240,351)
                                    $graphics.DrawImage($image,$dest)
                                    $graphics.DrawRectangle($rule,$dest)
                                } else {
                                    $height=$image.Height-$plan.cutoff_row
                                    $src=[System.Drawing.Rectangle]::new(0,$plan.cutoff_row,$image.Width,$height)
                                    $dest=[System.Drawing.Rectangle]::new($x+10,$y+28,$image.Width,$height)
                                    $graphics.DrawImage($image,$dest,$src,[System.Drawing.GraphicsUnit]::Pixel)
                                }
                            } finally { $image.Dispose() }
                        }
                        $path=Join-Path $plan.output_directory ($group.id+'-'+$kind+'-'+('{0:D3}' -f ([int]($start/$perSheet)+1))+'.png')
                        $canvas.Save($path,[System.Drawing.Imaging.ImageFormat]::Png)
                        $writer.WriteLine((@{kind=$kind;path=$path;pages=$ids} | ConvertTo-Json -Depth 4 -Compress))
                    } finally { $graphics.Dispose();$canvas.Dispose() }
                }
            }
            foreach ($item in $items) {
                if (-not $item.full_size_required) { continue }
                $image=[System.Drawing.Image]::FromFile($item.png)
                $old=$null
                if ($item.mismatch -and $item.source_png) { $old=[System.Drawing.Image]::FromFile($item.source_png) }
                $width=$image.Width
                if ($old) { $width+=$old.Width+12 }
                $height=$image.Height
                if ($old) { $height=[Math]::Max($height,$old.Height) }
                $canvas=[System.Drawing.Bitmap]::new($width,$height+48)
                $graphics=[System.Drawing.Graphics]::FromImage($canvas)
                try {
                    $graphics.Clear([System.Drawing.Color]::White)
                    $graphics.DrawString($item.label,$titleFont,$ink,6,3)
                    if ($old) {
                        $graphics.DrawString('SOURCE',$font,$ink,6,27)
                        $graphics.DrawString('COMBINED',$font,$ink,$old.Width+18,27)
                        $src=[System.Drawing.Rectangle]::new(0,0,$old.Width,$old.Height)
                        $dest=[System.Drawing.Rectangle]::new(0,48,$old.Width,$old.Height)
                        $graphics.DrawImage($old,$dest,$src,[System.Drawing.GraphicsUnit]::Pixel)
                        $src=[System.Drawing.Rectangle]::new(0,0,$image.Width,$image.Height)
                        $dest=[System.Drawing.Rectangle]::new($old.Width+12,48,$image.Width,$image.Height)
                        $graphics.DrawImage($image,$dest,$src,[System.Drawing.GraphicsUnit]::Pixel)
                    } else {
                        $src=[System.Drawing.Rectangle]::new(0,0,$image.Width,$image.Height)
                        $dest=[System.Drawing.Rectangle]::new(0,48,$image.Width,$image.Height)
                        $graphics.DrawImage($image,$dest,$src,[System.Drawing.GraphicsUnit]::Pixel)
                    }
                    $path=Join-Path $plan.output_directory ($group.id+'-page-'+('{0:D4}' -f $item.physical_page)+'.png')
                    $canvas.Save($path,[System.Drawing.Imaging.ImageFormat]::Png)
                    $copyX=0
                    if ($old) {
                        if (-not [RasterPixels]::CopyEquals($item.source_png,$path,0,48)) { throw 'Full-size source proof pixels changed' }
                        $copyX=$old.Width+12
                    }
                    if (-not [RasterPixels]::CopyEquals($item.png,$path,$copyX,48)) { throw 'Full-size combined proof pixels changed' }
                    $writer.WriteLine((@{kind='full_size';path=$path;pages=@($item.id);mismatch=[bool]$item.mismatch;native_pixels_verified=$true} | ConvertTo-Json -Depth 4 -Compress))
                } finally {
                    $graphics.Dispose();$canvas.Dispose();$image.Dispose()
                    if ($old) { $old.Dispose() }
                }
            }
            Write-Output ('Created contact, folio and required full-size proofs for '+$group.id)
        }
        $font.Dispose();$titleFont.Dispose()
    } else { throw 'Unknown helper mode' }
} finally { $writer.Dispose() }
'''


def drawing_run(output, plan, stem):
    executable = shutil.which("pwsh") or shutil.which("powershell")
    if not executable:
        raise RuntimeError("PowerShell with Windows System.Drawing is required for decoded RGB proofs.")
    helper = output / "drawing-helper.ps1"
    helper.write_text(DRAWING_HELPER, encoding="utf-8", newline="\n")
    plan_path, results = output / (stem + "-plan.json"), output / (stem + ".jsonl")
    plan = dict(plan, result_path=str(results))
    write_json(plan_path, plan)
    completed = run([executable, "-NoLogo", "-NoProfile", "-File", helper, "-PlanPath", plan_path],
                    capture_output=True, text=True, encoding="utf-8", errors="replace")
    (output / (stem + ".log")).write_text(completed.stdout + completed.stderr,
                                         encoding="utf-8", newline="\n")
    if completed.stdout:
        print(completed.stdout.strip(), flush=True)
    if completed.returncode:
        print(completed.stderr.strip(), file=sys.stderr, flush=True)
        raise RuntimeError(f"Drawing helper failed; input plan: {relative(plan_path)}")
    return [json.loads(line) for line in results.read_text(encoding="utf-8").splitlines() if line]


def roman(number):
    result = []
    for value, text in ((1000,"m"),(900,"cm"),(500,"d"),(400,"cd"),(100,"c"),(90,"xc"),
                        (50,"l"),(40,"xl"),(10,"x"),(9,"ix"),(5,"v"),(4,"iv"),(1,"i")):
        count, number = divmod(number, value)
        result.append(text * count)
    return "".join(result)


def validate_render(manifest, pdfs):
    if not manifest.get("complete") or manifest.get("errors"):
        raise ValueError("Render manifest is incomplete")
    if set(manifest["documents"]) != set(pdfs):
        raise ValueError("Render manifest does not cover the required documents")
    for cid, expected in pdfs.items():
        document = manifest["documents"][cid]
        if document["pdf_sha256"] != expected["sha256"] or document["pdf"] != expected["pdf"]:
            raise ValueError(f"Render input no longer matches: {cid}")
        if digest(ROOT / document["pdf"]) != expected["sha256"]:
            raise ValueError(f"Rendered PDF changed: {cid}")
        for page in document["images"]:
            if digest(ROOT / page["path"]) != page["sha256"]:
                raise ValueError(f"Rendered image changed: {page['path']}")


def inspect_source_pixels(args):
    contents, sources = read_json(args.contents), read_json(args.output / "sources.json")
    validate_render(sources, {c["component_id"]: {"pdf": c["sources"]["pdf"]["path"],
                                               "sha256": c["sources"]["pdf"]["sha256"]}
                              for c in contents["components"]})
    pages = []
    for component in contents["components"]:
        cid = component["component_id"]
        for image in sources["documents"][cid]["images"]:
            pages.append({"id": f"{cid}/{image['page']:04d}", "component_id": cid,
                          "source_page": image["page"], "png": image})
    facts = drawing_run(args.output, {"mode": "pixels", "cutoff_row": CUTOFF_ROW,
                                     "guard_first_row": math.floor(GUARD_FIRST_MM * DPI / 25.4),
                                     "guard_last_row": math.ceil(GUARD_LAST_MM * DPI / 25.4),
                                     "items": [{"id": p["id"], "png": str(ROOT / p["png"]["path"]),
                                                "source_png": None} for p in pages]}, "source-decoded-pixels")
    by_id = {r["id"]: r["pixels"] for r in facts}
    if set(by_id) != {p["id"] for p in pages}:
        raise ValueError("Source pixel inspection coverage is incomplete")
    flags = []
    for page in pages:
        page["decoded_pixels"] = by_id[page["id"]]
        if page["decoded_pixels"]["guard_nonwhite_pixels"]:
            flags.append(page["id"])
    report = {"schema_version": 1, "created_utc": stamp(), "script_sha256": digest(Path(__file__)),
              "sources_manifest": {"path": relative(args.output / "sources.json"), "sha256": digest(args.output / "sources.json")},
              "source_components": len(sources["documents"]), "source_pages": len(pages),
              "footer_cutoff_mm": CUTOFF_MM, "compared_rows": CUTOFF_ROW,
              "guard_band_mm": [GUARD_FIRST_MM,GUARD_LAST_MM], "guard_flags": flags, "pages": pages,
              "status": "source_cutoff_guard_clear" if not flags else "footer_gap_requires_review",
              "human_visual_review": "Not inferred from pixel inspection."}
    write_json(args.output / "source-pixels.json", report)
    print(f"Decoded {len(pages)} source pages; {len(flags)} footer-gap flags", flush=True)
    return report


def compare_pages(args):
    contents, pagination, page_map = pagination_data(args)
    sources, combined = read_json(args.output / "sources.json"), read_json(args.output / "combined.json")
    validate_render(sources, {c["component_id"]: {"pdf": c["sources"]["pdf"]["path"],
                                               "sha256": c["sources"]["pdf"]["sha256"]}
                              for c in contents["components"]})
    validate_render(combined, {name: {"pdf": v["pdf"], "sha256": v["sha256"]}
                               for name, v in pagination["volumes"].items()})
    if sources["render_settings"] != combined["render_settings"]:
        raise ValueError("Source and combined render settings differ")
    if combined["input"]["sha256"] != digest(args.pagination):
        raise ValueError("Pagination changed after combined rendering")
    items, records = [], []
    for volume_name, volume in pagination["volumes"].items():
        for image in combined["documents"][volume_name]["images"]:
            page = image["page"]
            mapped = page_map[volume_name].get(page)
            if mapped:
                source = sources["documents"][mapped["component_id"]]["images"][mapped["source_page"] - 1]
                folio, kind = mapped["folio"], "retained"
            else:
                source = None
                if page in volume["blank_pages"]:
                    folio, kind = "blank (no printed folio)", "inserted_blank"
                elif page < volume["body_start_physical"]:
                    folio, kind = roman(page) + " (if printed)", "front_matter"
                else:
                    folio = str(page - volume["body_start_physical"] + 1)
                    kind = "index" if volume.get("index_first_physical") and page >= volume["index_first_physical"] else "new_page"
            pdf_label = str(volume["page_labels"][page-1]) if "page_labels" in volume else None
            if pdf_label is not None:
                if mapped and pdf_label != mapped["folio"]:
                    raise ValueError(f"Mapped folio differs from actual PDF page label: {volume_name}/{page}")
                folio = pdf_label + (" (blank/no printed folio)" if kind == "inserted_blank" else
                                     " (if printed)" if kind == "front_matter" else "")
            record = {"id": f"{volume_name}/{page:04d}", "volume": volume_name, "physical_page": page,
                      "folio": folio, "pdf_page_label": pdf_label, "kind": kind, "png": image,
                      "component_id": mapped["component_id"] if mapped else None,
                      "source_page": mapped["source_page"] if mapped else None,
                      "source_png": source}
            records.append(record)
            items.append({"id": record["id"], "png": str(ROOT / image["path"]),
                          "source_png": str(ROOT / source["path"]) if source else None})
    plan = {"mode": "pixels", "cutoff_row": CUTOFF_ROW,
            "guard_first_row": math.floor(GUARD_FIRST_MM * DPI / 25.4),
            "guard_last_row": math.ceil(GUARD_LAST_MM * DPI / 25.4), "items": items}
    decoded = drawing_run(args.output, plan, "decoded-pixels")
    by_id = {row["id"]: row for row in decoded}
    if set(by_id) != {row["id"] for row in records}:
        raise ValueError("Decoded pixel results do not cover every combined page exactly once")
    mismatches, guard_flags = [], []
    for record in records:
        facts = by_id[record["id"]]["pixels"]
        record["decoded_pixels"] = facts
        if record["source_png"]:
            record["match"] = facts["exact_rgb_match"]
            record["comparison_method"] = "Exact equality of all decoded RGB8 pixels in rows 0 through 1327 inclusive"
            record["filtered_prefix_hash_equal"] = (record["png"]["filtered_scanline_prefix_sha256"] ==
                                                      record["source_png"]["filtered_scanline_prefix_sha256"])
            if record["filtered_prefix_hash_equal"] and not record["match"]:
                raise ValueError("Independent PNG-filter prefix check contradicts decoded comparison")
            if not record["match"]:
                mismatches.append(record["id"])
            guarded = [("source", facts["source"]), ("combined", facts["combined"])]
        else:
            record["match"] = None
            record["comparison_method"] = "New page: no accepted-source counterpart; full-size human review required"
            guarded = [("combined", facts)]
        for origin, stats in guarded:
            if stats["guard_nonwhite_pixels"]:
                guard_flags.append({"id": record["id"], "origin": origin,
                                    "nonwhite_pixels": stats["guard_nonwhite_pixels"],
                                    "box": stats["guard_nonwhite_box"]})
    report = {"schema_version": 1, "created_utc": stamp(),
              "script_sha256": digest(Path(__file__)),
              "source_render_manifest_sha256": digest(args.output / "sources.json"),
              "combined_render_manifest_sha256": digest(args.output / "combined.json"),
              "contents": {"path": relative(args.contents), "sha256": digest(args.contents)},
              "pagination": {"path": relative(args.pagination), "sha256": digest(args.pagination)},
              "volumes": pagination["volumes"], "render_settings": combined["render_settings"],
              "method": "System.Drawing without color management decodes every raster to top-down RGB8; exact channel-byte equality above the footer, with SHA-256 receipts and mismatch pixel bounds. PNG-filter prefix hashes are an independent sufficient equality check, not the final comparison criterion.",
              "footer_exclusion": {"cutoff_mm": CUTOFF_MM, "rows_compared": CUTOFF_ROW,
                                   "effective_cutoff_mm": CUTOFF_ROW * 25.4 / DPI,
                                   "guard_band_mm": [GUARD_FIRST_MM, GUARD_LAST_MM],
                                   "guard_rows": [plan["guard_first_row"], plan["guard_last_row"]],
                                   "guard_expectation": "Every RGB channel is 255 in the full-width blank gap around the cutoff.",
                                   "guard_flags": guard_flags},
              "totals": {"accepted_sources": len(sources["documents"]), "source_pages": sources["pages"],
                         "combined_pages": len(records), "retained_pages": sum(r["match"] is not None for r in records),
                         "exact_body_header_matches": sum(r["match"] is True for r in records),
                         "mismatches": len(mismatches), "new_pages": sum(r["match"] is None for r in records),
                         "guard_flags": len(guard_flags)},
              "mismatch_pages": mismatches, "pages": records,
              "human_visual_review": "Not performed or inferred by this script. Inspect contact sheets/folios and every new or mismatched page.",
              "status": "pixel_checks_passed_human_proofs_pending" if not mismatches and not guard_flags else "differences_or_footer_gap_require_review"}
    write_json(args.output / "comparison.json", report)
    write_json(args.output / "comparisons" / report["pagination"]["sha256"][:20] / "comparison.json", report)
    print(json.dumps(report["totals"], ensure_ascii=False), flush=True)
    return report


def make_proofs(args):
    comparison = read_json(args.output / "comparison.json")
    if comparison["pagination"]["sha256"] != digest(args.pagination):
        raise ValueError("Comparison is stale for current pagination")
    for volume in comparison["volumes"].values():
        if digest(ROOT / volume["pdf"]) != volume["sha256"]:
            raise ValueError("Combined PDF changed after comparison")
    folder = args.output / "proofs" / comparison["pagination"]["sha256"][:20]
    folder.mkdir(parents=True, exist_ok=True)
    groups = []
    for name in comparison["volumes"]:
        items = []
        for page in comparison["pages"]:
            if page["volume"] != name:
                continue
            source = page["source_png"]
            suffix = f"{page['component_id']} source {page['source_page']}" if source else page["kind"]
            label = f"{name} physical {page['physical_page']} | folio {page['folio']} | {suffix}"
            items.append({"id": page["id"], "physical_page": page["physical_page"], "label": label,
                          "png": str(ROOT / page["png"]["path"]),
                          "source_png": str(ROOT / source["path"]) if source else None,
                          "mismatch": page["match"] is False,
                          "full_size_required": page["match"] is not True})
        groups.append({"id": name, "items": items})
    artifacts = drawing_run(args.output, {"mode": "proofs", "cutoff_row": CUTOFF_ROW,
                                         "output_directory": str(folder), "groups": groups}, "proof-artifacts")
    for artifact in artifacts:
        path = Path(artifact["path"])
        artifact["path"], artifact["sha256"] = relative(path), digest(path)
    for kind in ("contact", "folio"):
        covered = [p for a in artifacts if a["kind"] == kind for p in a["pages"]]
        if len(covered) != len(set(covered)) or set(covered) != {p["id"] for p in comparison["pages"]}:
            raise ValueError(f"Incomplete or duplicate {kind} proof coverage")
    full = {p for a in artifacts if a["kind"] == "full_size" for p in a["pages"]}
    if full != {p["id"] for p in comparison["pages"] if p["match"] is not True}:
        raise ValueError("Required full-size proofs are incomplete")
    report = {"schema_version": 1, "created_utc": stamp(),
              "comparison": {"path": relative(args.output / "comparison.json"), "sha256": digest(args.output / "comparison.json")},
              "pagination_sha256": digest(args.pagination), "artifacts": artifacts,
              "counts": {kind: sum(a["kind"] == kind for a in artifacts) for kind in ("contact", "folio", "full_size")},
              "all_page_contact_and_folio_coverage": True,
              "new_and_mismatched_page_full_size_coverage": True,
              "inspection_mode": "Generated evidence only. Contact sheets are reduced views; folio strips and required full-size proofs retain native pixels. Human inspection must be recorded separately."}
    write_json(args.output / "proofs.json", report)
    print(json.dumps(report["counts"], ensure_ascii=False), flush=True)
    return report


def self_test(args):
    """A changed body pixel must fail; a changed footer pixel must pass."""
    folder = args.output / "self-test"
    folder.mkdir(parents=True, exist_ok=True)
    width, height = 20, 20
    def png(name, changed=None, filter_kind=0):
        pixels = [bytearray([255] * width * 3) for _ in range(height)]
        if changed:
            x, y = changed
            pixels[y][x*3:x*3+3] = b"\x00\x80\xff"
        previous, rows = bytearray(width*3), []
        for row in pixels:
            encoded = row if filter_kind == 0 else bytes((a-b) % 256 for a,b in zip(row, previous))
            rows.append(bytes([filter_kind]) + encoded)
            previous = row
        def chunk(kind, body):
            return struct.pack(">I", len(body)) + kind + body + struct.pack(">I", zlib.crc32(kind+body) & 0xffffffff)
        data = PNG_SIGNATURE + chunk(b"IHDR",struct.pack(">IIBBBBB",width,height,8,2,0,0,0))
        data += chunk(b"IDAT",zlib.compress(b"".join(rows))) + chunk(b"IEND",b"")
        path = folder / name
        path.write_bytes(data)
        load_png(path)
        return str(path)
    original = png("original.png")
    cases = [("same_rgb_different_filter", png("refiltered.png",filter_kind=2), True),
             ("body_change", png("body.png",(3,5)), False),
             ("footer_change", png("footer.png",(3,18)), True)]
    results = drawing_run(folder, {"mode":"pixels","cutoff_row":15,"guard_first_row":14,"guard_last_row":16,
                                  "items":[{"id":name,"source_png":original,"png":path} for name,path,_ in cases]}, "results")
    actual={r["id"]:r["pixels"] for r in results}
    for name,_,wanted in cases:
        if actual[name]["exact_rgb_match"] is not wanted:
            raise AssertionError(f"Pixel comparator self-test failed: {name}")
    if actual["body_change"]["differing_pixels"] != 1 or actual["body_change"]["differing_box"] != [3,5,3,5]:
        raise AssertionError("Pixel difference location is wrong")
    write_json(folder / "receipt.json", {"passed": True, "cases": results,
                                        "purpose": "Actual RGB equality despite different PNG filters; body edits detected; footer-only changes excluded."})
    print("Pixel comparator self-test passed", flush=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("stage", choices=["sources", "source-pixels", "combined", "compare", "proofs", "self-test"])
    parser.add_argument("--contents", type=Path, default=ROOT / "book/contents.json")
    parser.add_argument("--pagination", type=Path, default=ROOT / "typesetting/full-book/pagination.json")
    parser.add_argument("--output", type=Path, default=ROOT / "build/full-book/raster")
    parser.add_argument("--jobs", type=int, choices=range(1, 5), default=2)
    parser.add_argument("--gs", help="Optional explicit Ghostscript executable")
    parser.add_argument("--select", default="", help="Source-only comma-separated component IDs")
    args = parser.parse_args()
    args.output = args.output.resolve()
    args.output.relative_to((ROOT / "build/full-book/raster").resolve())
    args.output.mkdir(parents=True, exist_ok=True)
    if args.stage == "sources":
        render_sources(args)
    elif args.stage == "source-pixels":
        inspect_source_pixels(args)
    elif args.stage == "combined":
        render_combined(args)
    elif args.stage == "compare":
        compare_pages(args)
    elif args.stage == "proofs":
        make_proofs(args)
    elif args.stage == "self-test":
        self_test(args)


if __name__ == "__main__":
    try:
        main()
    except Exception as error:
        print(f"ERROR: {error}", file=sys.stderr)
        raise SystemExit(1)
