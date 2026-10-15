import { test } from "node:test";
import assert from "node:assert/strict";
import { mkdtemp, mkdir, readFile, rm, stat, writeFile } from "node:fs/promises";
import { tmpdir } from "node:os";
import { join } from "node:path";
import { createRequire } from "node:module";
import { optimizePublic } from "./optimize-public.mjs";
const sharp = createRequire(new URL("../../frontend/package.json", import.meta.url))("sharp");

test("compresses copied large JPEG while preserving source and excluded homepage", async () => {
  const temporary = await mkdtemp(join(tmpdir(), "energy-web-assets-"));
  try {
    const source = join(temporary, "public");
    const output = join(temporary, "optimized");
    await mkdir(join(source, "chronicle"), { recursive: true });
    await mkdir(join(source, "home-hero"), { recursive: true });
    let seed = 17;
    const pixels = Buffer.alloc(2400 * 1200 * 3);
    for (let index = 0; index < pixels.length; index++) { seed = (seed * 1664525 + 1013904223) >>> 0; pixels[index] = seed >>> 24; }
    const jpeg = await sharp(pixels, { raw: { width: 2400, height: 1200, channels: 3 } }).jpeg({ quality: 100 }).toBuffer();
    assert.ok(jpeg.length > 512 * 1024);
    await writeFile(join(source, "chronicle", "synthetic.jpg"), jpeg);
    await writeFile(join(source, "home-hero", "frozen.jpg"), jpeg);
    const summary = await optimizePublic(source, output);
    assert.equal(summary.optimized_files, 1);
    assert.equal(summary.source_bytes, jpeg.length * 2);
    assert.ok(summary.output_bytes < summary.source_bytes);
    assert.ok((await stat(join(output, "chronicle", "synthetic.jpg"))).size < jpeg.length);
    const metadata = await sharp(await readFile(join(output, "chronicle", "synthetic.jpg"))).metadata();
    assert.equal(metadata.width, 1920);
    assert.equal(metadata.format, "jpeg");
    assert.deepEqual(await readFile(join(source, "chronicle", "synthetic.jpg")), jpeg);
    assert.deepEqual(await readFile(join(output, "home-hero", "frozen.jpg")), jpeg);
  } finally { await rm(temporary, { recursive: true, force: true }); }
});
