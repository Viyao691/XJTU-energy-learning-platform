import { cp, mkdir, readFile, readdir, stat, writeFile } from "node:fs/promises";
import { createRequire } from "node:module";
import { extname, isAbsolute, join, relative, resolve, sep } from "node:path";
import { pathToFileURL } from "node:url";
const sharp = createRequire(new URL("../../frontend/package.json", import.meta.url))("sharp");
sharp.concurrency(1);

async function filesIn(directory) {
  const files = [];
  for (const entry of await readdir(directory, { withFileTypes: true })) {
    const path = join(directory, entry.name);
    if (entry.isDirectory()) files.push(...await filesIn(path));
    else if (entry.isFile()) files.push(path);
  }
  return files;
}

export async function optimizePublic(source, output) {
  const sourceDir = resolve(source);
  const outputDir = resolve(output);
  const relation = relative(sourceDir, outputDir);
  if (!relation || (!relation.startsWith(`..${sep}`) && relation !== ".." && !isAbsolute(relation))) throw new Error("Output must be outside the source public directory");
  await mkdir(outputDir);
  await cp(sourceDir, outputDir, { recursive: true });
  const summary = { source_files: 0, output_files: 0, source_bytes: 0, output_bytes: 0, optimized_files: 0, files: [] };
  for (const path of await filesIn(outputDir)) {
    const name = relative(outputDir, path);
    const inputBytes = (await stat(path)).size;
    let outputBytes = inputBytes;
    const section = name.split(sep)[0];
    const extension = extname(name).toLowerCase();
    if (["chronicle", "workspace"].includes(section) && inputBytes > 512 * 1024 && [".jpg", ".jpeg", ".png"].includes(extension)) {
      const image = sharp(await readFile(path));
      const buffer = extension === ".png"
        ? await image.png({ compressionLevel: 9, palette: false }).toBuffer()
        : await image.rotate().resize({ width: 1920, height: 1920, fit: "inside", withoutEnlargement: true }).jpeg({ quality: 82 }).toBuffer();
      if (buffer.length < inputBytes) {
        await writeFile(path, buffer);
        outputBytes = buffer.length;
        summary.optimized_files++;
        summary.files.push({ path: name.split(sep).join("/"), source_bytes: inputBytes, output_bytes: outputBytes });
      }
    }
    summary.source_files++;
    summary.output_files++;
    summary.source_bytes += inputBytes;
    summary.output_bytes += outputBytes;
  }
  return summary;
}

if (process.argv[1] && import.meta.url === pathToFileURL(resolve(process.argv[1])).href) {
  const [, , source, output, summaryFile] = process.argv;
  if (!source || !output) throw new Error("Usage: node scripts/web/optimize-public.mjs SOURCE_PUBLIC OUTPUT_PUBLIC [SUMMARY_JSON]");
  const summary = await optimizePublic(source, output);
  const json = JSON.stringify(summary, null, 2);
  if (summaryFile) await writeFile(summaryFile, `${json}\n`);
  console.log(json);
}
