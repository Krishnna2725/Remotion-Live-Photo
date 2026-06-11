#!/usr/bin/env python3
"""
MP4 → Live Photo 批量转换工具
将 Remotion 渲染的 MP4 场景视频转换为 Live Photo 文件对（JPEG + MOV）

用法:
    python mp4_to_livephoto.py <input_dir> [output_dir]
    python mp4_to_livephoto.py scene.mp4              # 单文件
    python mp4_to_livephoto.py ./scenes/ ./output/    # 批量处理目录

输出:
    每个 MP4 生成一对文件: cover.jpg + clip.mov
    两个文件通过 ContentIdentifier UUID 配对，可直接导入 iOS/安卓相册
"""

import argparse
import os
import subprocess
import sys
import struct
import uuid
import io
import shutil
from pathlib import Path

# ── 工具路径 ──────────────────────────────────────────────────────────────
def resolve_tool(name: str, env_name: str) -> str:
    """优先使用环境变量，否则从 PATH 查找工具。"""
    configured = os.environ.get(env_name)
    if configured:
        return configured
    path = shutil.which(name)
    if path:
        return path
    raise FileNotFoundError(
        f"找不到 {name}。请将其加入 PATH，或设置环境变量 {env_name}。"
    )


def ensure_tools():
    """检查必要工具"""
    global FFMPEG, FFPROBE
    FFMPEG = resolve_tool("ffmpeg", "FFMPEG_PATH")
    FFPROBE = resolve_tool("ffprobe", "FFPROBE_PATH")
    for tool_path in (FFMPEG, FFPROBE):
        if not os.path.isfile(tool_path):
            raise FileNotFoundError(f"找不到: {tool_path}")
    print(f"✓ ffmpeg: {FFMPEG}")
    print(f"✓ ffprobe: {FFPROBE}")


FFMPEG = ""
FFPROBE = ""


# ── FFmpeg 操作 ────────────────────────────────────────────────────────────

def get_video_duration(input_path: str) -> float:
    """获取视频时长（秒）"""
    result = subprocess.run(
        [FFPROBE, "-v", "error", "-show_entries", "format=duration",
         "-of", "csv=p=0", input_path],
        capture_output=True, text=True
    )
    return float(result.stdout.strip())


def extract_still_frame(input_path: str, output_jpg: str, seek_time: float = 0.5):
    """从视频提取静帧作为封面图"""
    subprocess.run(
        [FFMPEG, "-y", "-ss", str(seek_time), "-i", input_path,
         "-frames:v", "1", "-q:v", "2", output_jpg],
        capture_output=True, check=True
    )


def convert_to_mov(input_mp4: str, output_mov: str, duration: float = 5.0):
    """将 MP4 转换为符合 Apple Live Photo 规范的 MOV

    要求:
    - H.264 视频编码
    - AAC 音频编码 (如有)
    - MOV 容器 (QuickTime)
    - 时长 ≤ 5 秒
    """
    cmd = [
        FFMPEG, "-y", "-i", input_mp4,
        "-t", str(duration),
        "-c:v", "libx264",
        "-pix_fmt", "yuv420p",
        "-profile:v", "high",
        "-level", "4.0",
        "-movflags", "+faststart",
    ]

    # 检查是否有音频流
    probe = subprocess.run(
        [FFPROBE, "-v", "error", "-select_streams", "a",
         "-show_entries", "stream=codec_type", "-of", "csv=p=0", input_mp4],
        capture_output=True, text=True
    )
    if probe.stdout.strip():
        cmd.extend(["-c:a", "aac", "-b:a", "128k"])
    else:
        cmd.extend(["-an"])

    cmd.append(output_mov)
    subprocess.run(cmd, capture_output=True, check=True)


# ── 元数据写入 ────────────────────────────────────────────────────────────

def write_xmp_to_jpeg(jpeg_path: str, content_id: str):
    """向 JPEG 写入 Apple ContentIdentifier XMP 元数据"""
    xmp_packet = (
        '<?xpacket begin="\xef\xbb\xbf" id="W5M0MpCehiHzreSzNTczkc9d"?>\n'
        '<x:xmpmeta xmlns:x="adobe:ns:meta/">\n'
        '  <rdf:RDF xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">\n'
        '    <rdf:Description rdf:about=""\n'
        '      xmlns:apple-fi="http://ns.apple.com/faceinfo/1.0/"\n'
        f'      apple-fi:ContentIdentifier="{content_id}" />\n'
        '  </rdf:RDF>\n'
        '</x:xmpmeta>\n'
        '<?xpacket end="w"?>'
    )
    xmp_bytes = xmp_packet.encode("utf-8")

    with open(jpeg_path, "rb") as f:
        data = bytearray(f.read())

    # 删除已有 XMP 段 (FF E1 开头的 APP1 段包含 "http://ns.adobe.com/xap/1.0/")
    i = 2  # 跳过 SOI (FF D8)
    segments_to_remove = []
    while i < len(data) - 1:
        if data[i] == 0xFF and data[i + 1] in (0xE0, 0xE1, 0xE2, 0xFE):
            seg_len = struct.unpack(">H", data[i + 2:i + 4])[0]
            if data[i + 1] == 0xE1:
                # 检查是否是 XMP 段
                seg_end = i + 2 + seg_len
                seg_data = data[i + 4:min(seg_end, i + 4 + 30)]
                if b"http://ns.adobe.com/xap/1.0/\x00" in seg_data:
                    segments_to_remove.append((i, seg_end))
            i += 2 + seg_len
        elif data[i] == 0xFF and data[i + 1] == 0xDA:  # SOS - 后面是图像数据
            break
        else:
            i += 1

    # 逆序删除避免偏移问题
    for start, end in reversed(segments_to_remove):
        del data[start:end]

    # 构造新的 APP1 XMP 段
    # APP1 = FF E1 + 长度(2字节) + 命名空间标识 + 0x00 + XMP 数据
    ns_id = b"http://ns.adobe.com/xap/1.0/\x00"
    app1_payload = ns_id + xmp_bytes
    app1_length = len(app1_payload) + 2  # 长度字段包含自身
    app1_segment = b"\xff\xe1" + struct.pack(">H", app1_length) + app1_payload

    # 在 SOI 之后插入
    new_data = bytes(data[:2]) + app1_segment + bytes(data[2:])

    with open(jpeg_path, "wb") as f:
        f.write(new_data)


def write_mov_metadata(mov_path: str, content_id: str):
    """向 MOV 文件写入 com.apple.quicktime.content.identifier 元数据"""
    from mutagen.mp4 import MP4, MP4Tags, MP4FreeForm

    tags = MP4Tags()
    # Apple Live Photo 使用 freeform 标签，key 为反转 DNS 格式
    tags["----:com.apple.quicktime:content.identifier"] = [
        MP4FreeForm(content_id.encode("utf-8"))
    ]

    video = MP4(mov_path)
    video.update(tags)
    video.save()


def _write_mov_metadata_manual(mov_path: str, content_id: str):
    """手动向 MOV 文件插入 QuickTime metadata atom"""
    with open(mov_path, "rb") as f:
        data = bytearray(f.read())

    # 查找 moov atom
    moov_offset = _find_atom(data, b"moov")
    if moov_offset is None:
        print("  ⚠ MOV 文件中未找到 moov atom，跳过元数据写入")
        return

    moov_size = struct.unpack(">I", data[moov_offset + 4:moov_offset + 8])[0]

    # 查找 moov 内部的 udta atom
    udta_offset_in_moov = _find_atom_in_range(
        data, b"udta", moov_offset + 8, moov_offset + moov_size
    )

    # 构造 metadata atom 树: moov > udta > meta > ilst > ---- > mean + name + data
    metadata_block = _build_metadata_atoms(content_id)

    if udta_offset_in_moov is not None:
        # 在现有 udta 末尾追加
        udta_start = udta_offset_in_moov
        udta_size = struct.unpack(">I", data[udta_start + 4:udta_start + 8])[0]
        insert_pos = udta_start + 8 + (udta_size - 8)  # udta 内容末尾
        # 实际上 moov 中的 udta 之后还有内容（trak等），所以要在 udta 的结尾插入

        # 更简单的方法: 在 moov 的最前面插入 meta atom
        insert_pos = moov_offset + 8
        new_data = bytes(data[:insert_pos]) + metadata_block + bytes(data[insert_pos:])

        # 更新 moov size
        new_moov_size = moov_size + len(metadata_block)
        new_data = (
            bytearray(new_data[:moov_offset + 4])
            + struct.pack(">I", new_moov_size)
            + bytearray(new_data[moov_offset + 8:])
        )
    else:
        # 在 moov 末尾插入 udta 包含 metadata
        udta_atom = b"udta" + struct.pack(">I", len(metadata_block) + 8) + metadata_block
        insert_pos = moov_offset + 8
        new_data = (
            bytearray(data[:insert_pos])
            + udta_atom
            + bytearray(data[insert_pos:])
        )
        new_moov_size = moov_size + len(udta_atom)
        new_data = (
            bytearray(new_data[:moov_offset + 4])
            + struct.pack(">I", new_moov_size)
            + bytearray(new_data[moov_offset + 8:])
        )

    # 更新文件头的 mdat offset (如果有 ftyp)
    # 简化处理: 因为我们在 moov 前面插入，需要调整 moov 中的 chunk offset
    # 对于 -movflags +faststart 的文件，mdat 已经在 moov 后面
    # 重新计算所有 stco/co64 中的偏移量
    _fix_chunk_offsets(new_data, moov_offset, len(metadata_block) if udta_offset_in_moov is None else len(metadata_block))

    with open(mov_path, "wb") as f:
        f.write(new_data)


def _build_metadata_atoms(content_id: str) -> bytes:
    """构造 Apple Live Photo 需要的 metadata atom 树"""
    id_bytes = content_id.encode("utf-8")

    # data atom: type=1 (UTF-8), locale=0, data=id_bytes
    data_atom = (
        struct.pack(">I", len(id_bytes) + 16)
        + b"data"
        + struct.pack(">I", 1)      # type: UTF-8 string
        + struct.pack(">I", 0)      # locale
        + id_bytes
    )

    # name atom
    name_str = b"com.apple.quicktime.content.identifier"
    name_atom = (
        struct.pack(">I", len(name_str) + 12)
        + b"name"
        + struct.pack(">I", 0)
        + name_str
    )

    # mean atom (Apple domain)
    mean_str = b"com.apple.quicktime"
    mean_atom = (
        struct.pack(">I", len(mean_str) + 12)
        + b"mean"
        + struct.pack(">I", 0)
        + mean_str
    )

    # ---- (freeform) item
    item_payload = mean_atom + name_atom + data_atom
    item_atom = (
        struct.pack(">I", len(item_payload) + 8)
        + b"----"
        + item_payload
    )

    # ilst
    ilst_payload = item_atom
    ilst_atom = (
        struct.pack(">I", len(ilst_payload) + 8)
        + b"ilst"
        + ilst_payload
    )

    # hdlr for metadata
    hdlr_type = b"mdir"
    hdlr_subtype = b"mdta"
    hdlr_name = b""
    hdlr_payload = (
        struct.pack(">I", 0)           # version + flags
        + hdlr_type                    # handler type
        + hdlr_subtype                 # handler subtype
        + b"\x00" * 12                 # reserved
        + hdlr_name
    )
    hdlr_atom = (
        struct.pack(">I", len(hdlr_payload) + 12)
        + b"hdlr"
        + hdlr_payload
    )

    # meta container
    meta_payload = hdlr_atom + ilst_atom
    meta_atom = (
        struct.pack(">I", len(meta_payload) + 12)
        + b"meta"
        + struct.pack(">I", 0)  # version + flags
        + meta_payload
    )

    return meta_atom


def _find_atom(data: bytearray, atom_type: bytes) -> int | None:
    """在顶层查找 QuickTime atom"""
    offset = 0
    while offset < len(data) - 8:
        size = struct.unpack(">I", data[offset:offset + 4])[0]
        atype = data[offset + 4:offset + 8]
        if atype == atom_type:
            return offset
        if size < 8:
            break
        offset += size
    return None


def _find_atom_in_range(data: bytearray, atom_type: bytes, start: int, end: int) -> int | None:
    """在指定范围内查找 QuickTime atom"""
    offset = start
    while offset < end - 8:
        size = struct.unpack(">I", data[offset:offset + 4])[0]
        atype = data[offset + 4:offset + 8]
        if atype == atom_type:
            return offset
        if size < 8:
            break
        offset += size
    return None


def _fix_chunk_offsets(data: bytearray, moov_offset: int, extra_bytes: int):
    """修复因插入 metadata 导致的 chunk offset 偏移"""
    # 查找所有 stco 或 co64 atom 并更新偏移量
    moov_size = struct.unpack(">I", data[moov_offset + 4:moov_offset + 8])[0]
    _fix_stco_in_range(data, moov_offset + 8, moov_offset + moov_size, extra_bytes)


def _fix_stco_in_range(data: bytearray, start: int, end: int, extra_bytes: int):
    """递归修复 stco/co64 中的 chunk offset"""
    offset = start
    while offset < end - 8:
        size = struct.unpack(">I", data[offset:offset + 4])[0]
        atype = data[offset + 4:offset + 8]
        if size < 8:
            break

        if atype == b"stco":
            # version(1) + flags(3) + entry_count(4) + entries...
            entry_count = struct.unpack(">I", data[offset + 12:offset + 16])[0]
            for i in range(entry_count):
                pos = offset + 16 + i * 4
                old_val = struct.unpack(">I", data[pos:pos + 4])[0]
                struct.pack_into(">I", data, pos, old_val + extra_bytes)
        elif atype == b"co64":
            entry_count = struct.unpack(">I", data[offset + 12:offset + 16])[0]
            for i in range(entry_count):
                pos = offset + 16 + i * 8
                old_val = struct.unpack(">Q", data[pos:pos + 8])[0]
                struct.pack_into(">Q", data, pos, old_val + extra_bytes)
        elif atype in (b"moov", b"trak", b"mdia", b"minf", b"stbl"):
            # 递归进入容器 atom
            _fix_stco_in_range(data, offset + 8, offset + size, extra_bytes)

        offset += size


# ── 单文件 Motion Photo (Google 格式) ─────────────────────────────────────

def create_motion_photo(jpeg_path: str, mp4_path: str, output_path: str):
    """将 JPEG + MP4 合并为单文件 Motion Photo

    格式: [JPEG SOI...EOI] [MP4 ftyp...]
    兼容: OPPO、Google Pixel、小米、Windows 11 照片、小红书
    """
    import shutil

    # 读取 JPEG（确保以 EOI 结尾）
    with open(jpeg_path, "rb") as f:
        jpeg_data = f.read()
    if jpeg_data[-2:] != b"\xff\xd9":
        jpeg_data += b"\xff\xd9"

    # 读取 MP4
    with open(mp4_path, "rb") as f:
        mp4_data = f.read()

    video_size = len(mp4_data)

    # 构造 XMP（OPPO/Google Motion Photo V2 格式，兼容性最广）
    xmp = (
        '<?xpacket begin="\xef\xbb\xbf" id="W5M0MpCehiHzreSzNTczkc9d"?>\n'
        '<x:xmpmeta xmlns:x="adobe:ns:meta/">\n'
        '  <rdf:RDF xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">\n'
        '    <rdf:Description rdf:about=""\n'
        '      xmlns:GCamera="http://ns.google.com/photos/1.0/camera/"\n'
        '      xmlns:OpCamera="http://ns.oplus.com/photos/1.0/camera/"\n'
        '      xmlns:Container="http://ns.google.com/photos/1.0/container/"\n'
        '      xmlns:Item="http://ns.google.com/photos/1.0/container/item/"\n'
        '      GCamera:MotionPhoto="1"\n'
        '      GCamera:MotionPhotoVersion="1"\n'
        '      GCamera:MotionPhotoPresentationTimestampUs="0"\n'
        '      OpCamera:MotionPhotoOwner="oplus"\n'
        '      OpCamera:OLivePhotoVersion="2"\n'
        f'      OpCamera:VideoLength="{video_size}"\n'
        '      OpCamera:MotionPhotoEnable="True">\n'
        '      <Container:Directory>\n'
        '        <rdf:Seq>\n'
        '          <rdf:li rdf:parseType="Resource">\n'
        '            <Container:Item Item:Mime="image/jpeg" Item:Semantic="Primary" Item:Length="0" Item:Padding="0"/>\n'
        '          </rdf:li>\n'
        f'          <rdf:li rdf:parseType="Resource">\n'
        f'            <Container:Item Item:Mime="video/mp4" Item:Semantic="MotionPhoto" Item:Length="{video_size}" Item:Padding="0"/>\n'
        '          </rdf:li>\n'
        '        </rdf:Seq>\n'
        '      </Container:Directory>\n'
        '    </rdf:Description>\n'
        '  </rdf:RDF>\n'
        '</x:xmpmeta>\n'
        '<?xpacket end="w"?>'
    )

    # 插入 XMP 到 JPEG 部分（替换已有 XMP 或插入到 SOI 之后）
    xmp_bytes = xmp.encode("utf-8")
    ns_id = b"http://ns.adobe.com/xap/1.0/\0"
    payload = ns_id + xmp_bytes
    app1 = bytearray(b"\xff\xe1")
    app1 += struct.pack(">H", len(payload) + 2)
    app1 += payload

    # 在 SOI (FFD8) 之后直接插入 XMP，保留原始 JPEG 完整内容
    final_jpeg = jpeg_data[:2] + bytes(app1) + jpeg_data[2:]

    # 写出: JPEG + MP4
    with open(output_path, "wb") as f:
        f.write(final_jpeg)
        f.write(mp4_data)

    total_size = len(final_jpeg) + len(mp4_data)
    print(f"  ✓ Motion Photo: {Path(output_path).name} ({total_size // 1024}KB)")


# ── 双文件 Live Photo (Apple 格式) ───────────────────────────────────────

def convert_single(input_mp4: str, output_dir: str, clip_duration: float = 5.0,
                   cover_image: str | None = None, motion_photo: bool = False):
    """转换单个 MP4 文件为 Live Photo

    Args:
        cover_image: 外部指定的封面图路径。不指定则从视频中提取。
        motion_photo: True 输出单文件 .jpg（Google Motion Photo 格式）
    """
    input_path = Path(input_mp4)
    out_dir = Path(output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    stem = input_path.stem
    cover_path = out_dir / f"{stem}.jpg"
    clip_path = out_dir / f"{stem}.mov"
    content_id = str(uuid.uuid4()).upper()

    print(f"\n{'─' * 60}")
    print(f"处理: {input_path.name}")
    print(f"  ContentID: {content_id}")

    # 1. 检查视频时长
    duration = get_video_duration(input_mp4)
    actual_duration = min(duration, clip_duration)
    print(f"  视频时长: {duration:.1f}s → 截取 {actual_duration:.1f}s")

    # 2. 封面图
    if cover_image and Path(cover_image).is_file():
        import shutil
        shutil.copy2(cover_image, str(cover_path))
        print(f"  ✓ 封面图: {cover_path.name} (外部指定)")
    else:
        seek_time = min(0.5, duration / 2)
        extract_still_frame(input_mp4, str(cover_path), seek_time)
        print(f"  ✓ 封面图: {cover_path.name} (从视频提取)")

    # 3. 渲染 MP4
    temp_mp4 = str(out_dir / f"{stem}_temp.mp4")
    convert_to_mov(input_mp4, temp_mp4, actual_duration)

    if motion_photo:
        # 单文件模式: JPEG + MP4 合并为 Motion Photo
        mp4_path = out_dir / f"{stem}.jpg"  # 输出就是 .jpg
        create_motion_photo(str(cover_path), temp_mp4, str(mp4_path))
        try: os.unlink(temp_mp4)
        except: pass
        cover_size = mp4_path.stat().st_size // 1024
        print(f"  ✅ Motion Photo 创建成功! ({cover_size}KB)")
        return str(mp4_path), None
    else:
        # 双文件模式: cover.jpg + clip.mov (Apple Live Photo)
        import shutil
        shutil.move(temp_mp4, str(clip_path))
        print(f"  ✓ MOV视频: {clip_path.name}")

        write_xmp_to_jpeg(str(cover_path), content_id)
        print(f"  ✓ JPEG 元数据写入完成")
        write_mov_metadata(str(clip_path), content_id)
        print(f"  ✓ MOV 元数据写入完成")

        cover_size = cover_path.stat().st_size // 1024
        clip_size = clip_path.stat().st_size // 1024
        print(f"  封面: {cover_size}KB | 视频: {clip_size}KB")
        print(f"  ✅ Live Photo 创建成功!")
        return str(cover_path), str(clip_path)


def batch_convert(input_dir: str, output_dir: str, clip_duration: float = 5.0,
                  cover_dir: str | None = None):
    """批量转换目录中的所有 MP4 文件

    Args:
        cover_dir: 封面图目录，按文件名（不含扩展名）与 MP4 配对。
    """
    input_path = Path(input_dir)
    mp4_files = sorted(input_path.glob("**/*.mp4"))

    if not mp4_files:
        print(f"在 {input_dir} 中未找到 MP4 文件")
        return

    print(f"找到 {len(mp4_files)} 个 MP4 文件")
    print(f"输出目录: {output_dir}")
    print(f"动效时长上限: {clip_duration}s")

    success = 0
    failed = 0
    for mp4 in mp4_files:
        try:
            # 保持子目录结构
            rel = mp4.parent.relative_to(input_path)
            out = Path(output_dir) / rel
            # 查找配对封面图
            cover = None
            if cover_dir:
                cover_candidate = Path(cover_dir) / rel / f"{mp4.stem}.jpg"
                if not cover_candidate.is_file():
                    cover_candidate = Path(cover_dir) / f"{mp4.stem}.jpg"
                if cover_candidate.is_file():
                    cover = str(cover_candidate)
            convert_single(str(mp4), str(out), clip_duration, cover_image=cover)
            success += 1
        except Exception as e:
            print(f"\n  ❌ 处理失败 {mp4.name}: {e}")
            failed += 1

    print(f"\n{'═' * 60}")
    print(f"完成: {success} 成功, {failed} 失败")
    print(f"输出: {output_dir}")


def main():
    parser = argparse.ArgumentParser(
        description="MP4 → Live Photo 转换工具 (纯 Python + ffmpeg，无需 exiftool)"
    )
    parser.add_argument("input", help="输入 MP4 文件或目录")
    parser.add_argument("output", nargs="?", default=None, help="输出目录 (默认: 输入目录旁的 *_livephoto/)")
    parser.add_argument(
        "-c", "--cover", default=None,
        help="指定封面图 (JPEG 路径)"
    )
    parser.add_argument(
        "-d", "--duration", type=float, default=5.0,
        help="动效时长上限 (秒, 默认 5.0，单张不得超过 5 秒)"
    )
    parser.add_argument(
        "-m", "--motion-photo", action="store_true", default=False,
        help="输出单文件 Motion Photo (.jpg)，视频嵌在 JPEG 末尾，兼容安卓/小米/谷歌相册"
    )
    args = parser.parse_args()

    # 确保工具可用
    ensure_tools()

    input_path = Path(args.input)
    if args.output:
        output_dir = args.output
    else:
        if input_path.is_dir():
            output_dir = str(input_path.parent / f"{input_path.name}_livephoto")
        else:
            output_dir = str(input_path.parent / f"{input_path.stem}_livephoto")

    if input_path.is_dir():
        batch_convert(str(input_path), output_dir, args.duration, args.cover)
    elif input_path.is_file():
        convert_single(str(input_path), output_dir, args.duration, args.cover, args.motion_photo)
    else:
        print(f"输入路径不存在: {input_path}")
        sys.exit(1)


if __name__ == "__main__":
    main()
