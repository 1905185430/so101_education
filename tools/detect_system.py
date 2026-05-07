#!/usr/bin/env python3
"""
Minimal SO-101 device detector.

This tool only does two things:
1. Detect currently connected arms and cameras.
2. Save camera screenshots and export tools/devices/device_simple.json.

Usage examples:
    python3 tools/detect_system.py
    python3 tools/detect_system.py --skip-capture
    python3 tools/detect_system.py --format json
"""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Tuple


BASE_DIR = Path(__file__).parent / "devices"
IMAGES_DIR = BASE_DIR / "images"
DEVICE_SIMPLE_PATH = BASE_DIR / "device_simple.json"
SUPPORTED_FORMATS = ["text", "json"]
COLOR_FORMATS = {"YUYV", "MJPG", "NV12", "RGB3", "BGR3"}


def run_cmd(cmd: List[str], timeout: int = 3) -> subprocess.CompletedProcess:
    try:
        return subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=timeout,
            check=False,
        )
    except Exception:
        return subprocess.CompletedProcess(cmd, 1, "", "")


def save_json(path: Path, data: Any):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")


def safe_name(value: str) -> str:
    return "".join(ch if ch.isalnum() or ch in ("-", "_") else "_" for ch in value)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Minimal SO-101 device detector")
    parser.add_argument("--format", choices=SUPPORTED_FORMATS, default="text")
    parser.add_argument("--skip-capture", action="store_true")
    return parser.parse_args()


def find_video_links(dev_name: str) -> Tuple[str, str]:
    by_id = ""
    by_path = ""

    by_id_dir = Path("/dev/v4l/by-id")
    if by_id_dir.exists():
        for link in by_id_dir.glob("*"):
            try:
                if link.resolve().name == dev_name:
                    by_id = str(link)
                    break
            except Exception:
                pass

    by_path_dir = Path("/dev/v4l/by-path")
    if by_path_dir.exists():
        for link in by_path_dir.glob("*"):
            try:
                if link.resolve().name == dev_name:
                    by_path = str(link)
                    break
            except Exception:
                pass

    return by_id, by_path


def infer_camera_serial(dev_name: str, by_id: str, by_path: str) -> str:
    if by_id and "usb-" in Path(by_id).name:
        return Path(by_id).name.replace("usb-", "").split("-video-index")[0]
    if by_path:
        return Path(by_path).name.replace("-video-index0", "")
    return dev_name


def infer_camera_product(dev_name: str, by_id: str, by_path: str) -> str:
    if by_id:
        return Path(by_id).name.replace("usb-", "").split("-video-index")[0].replace("_", " ")
    if by_path:
        return Path(by_path).name.replace("-video-index0", " ").replace("_", " ")
    return dev_name


def get_formats(dev_path: str) -> List[Dict[str, Any]]:
    formats: List[Dict[str, Any]] = []
    output = run_cmd(["v4l2-ctl", "--device", dev_path, "--list-formats-ext"], timeout=5).stdout
    if not output:
        return formats

    current_format: Dict[str, Any] | None = None
    current_resolution: Dict[str, Any] | None = None
    for raw_line in output.splitlines():
        line = raw_line.strip()
        if "'" in line and ("]:" in line or "Pixel Format:" in line):
            current_format = {"fourcc": line.split("'")[1], "resolutions": []}
            formats.append(current_format)
        elif current_format and "Size: Discrete" in line:
            try:
                width, height = line.split("Discrete")[-1].strip().split("x")
                current_resolution = {"width": int(width), "height": int(height), "fps": []}
                current_format["resolutions"].append(current_resolution)
            except Exception:
                pass
        elif current_resolution and "fps)" in line:
            try:
                current_resolution["fps"].append(float(line.split("(")[-1].split("fps)")[0]))
            except Exception:
                pass
    return formats


def has_color_stream(formats: List[Dict[str, Any]]) -> bool:
    return any(fmt.get("fourcc") in COLOR_FORMATS for fmt in formats)


def get_camera_info(dev_path: str) -> Dict[str, Any]:
    dev_name = Path(dev_path).name
    by_id, by_path = find_video_links(dev_name)

    if by_id and "-video-index" in by_id and not by_id.endswith("-index0"):
        return {}
    if by_path and "-video-index" in by_path and not by_path.endswith("-index0"):
        return {}

    info: Dict[str, Any] = {
        "dev": dev_path,
        "by_id": by_id,
        "by_path": by_path,
        "serial": infer_camera_serial(dev_name, by_id, by_path),
        "product": infer_camera_product(dev_name, by_id, by_path),
        "formats": [],
        "color_stream": None,
        "status": "connected",
    }

    if shutil.which("v4l2-ctl"):
        output = run_cmd(["v4l2-ctl", "--device", dev_path, "--info"]).stdout
        for line in output.splitlines():
            if "Card type" in line:
                info["product"] = line.split(":")[-1].strip()
                break
        info["formats"] = get_formats(dev_path)
        info["color_stream"] = has_color_stream(info["formats"]) if info["formats"] else None

    return info


def get_arm_info(dev_path: str) -> Dict[str, Any]:
    info: Dict[str, Any] = {"tty": dev_path, "status": "connected"}
    dev_name = Path(dev_path).name

    by_id_dir = Path("/dev/serial/by-id")
    if by_id_dir.exists():
        for link in by_id_dir.glob("*"):
            try:
                if link.resolve().name == dev_name:
                    info["port"] = str(link)
                    if "Serial_" in link.name:
                        info["serial"] = link.name.split("Serial_")[1].split("-")[0]
                    else:
                        info["serial"] = link.name
                    break
            except Exception:
                pass

    if not info.get("serial"):
        info["serial"] = dev_name
    return info


def capture_image(dev_path: str, output_path: str, formats: List[Dict[str, Any]]) -> Tuple[bool, str]:
    try:
        import cv2  # type: ignore
    except Exception:
        return False, "OpenCV 未安装，无法保存截图。"

    try:
        if formats and not has_color_stream(formats):
            return False, "当前相机未检测到彩色流，已跳过截图。"

        cap = cv2.VideoCapture(dev_path, cv2.CAP_V4L2)
        if not cap.isOpened():
            cap = cv2.VideoCapture(dev_path)
        if not cap.isOpened():
            return False, "OpenCV 无法打开相机，可能设备忙、权限不足或驱动异常。"

        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        for _ in range(5):
            cap.read()
        ret, frame = cap.read()
        cap.release()

        if ret and frame is not None:
            if cv2.imwrite(output_path, frame):
                return True, "截图已保存。"
            return False, "已读取到图像，但写入图片文件失败。"
        return False, "已打开相机，但未读取到有效图像帧。"
    except Exception as exc:
        return False, f"截图异常: {exc.__class__.__name__}"


def detect_hardware(skip_capture: bool) -> Tuple[Dict[str, Any], Dict[str, Any]]:
    cameras: Dict[str, Any] = {}
    for dev in sorted(Path("/dev").glob("video*")):
        if dev.name.replace("video", "").isdigit():
            info = get_camera_info(str(dev))
            if info and info.get("serial"):
                cameras[info["serial"]] = info

    arms: Dict[str, Any] = {}
    for pattern in ("ttyACM*", "ttyUSB*"):
        for dev in sorted(Path("/dev").glob(pattern)):
            info = get_arm_info(str(dev))
            arms[info["serial"]] = info

    BASE_DIR.mkdir(parents=True, exist_ok=True)
    if IMAGES_DIR.exists():
        shutil.rmtree(IMAGES_DIR, ignore_errors=True)
    IMAGES_DIR.mkdir(parents=True, exist_ok=True)

    for serial, cam in cameras.items():
        if skip_capture:
            cam["image"] = ""
            cam["capture_status"] = "skipped"
            cam["capture_detail"] = "本次使用了 --skip-capture。"
            continue

        img_name = f"{safe_name(serial)}__{Path(cam['dev']).name}.jpg"
        img_path = IMAGES_DIR / img_name
        capture_ok, capture_detail = capture_image(cam["dev"], str(img_path), cam.get("formats", []))
        if capture_ok:
            cam["image"] = f"images/{img_name}"
            cam["capture_status"] = "saved"
            cam["capture_detail"] = capture_detail
        else:
            cam["image"] = ""
            cam["capture_status"] = "failed"
            cam["capture_detail"] = capture_detail

    return cameras, arms


def build_device_simple(cameras: Dict[str, Any], arms: Dict[str, Any]) -> Dict[str, Any]:
    simple_cameras: Dict[str, Any] = {}
    for serial, camera in cameras.items():
        simple_cameras[serial] = {k: v for k, v in camera.items() if k != "formats"}

    return {
        "timestamp": datetime.now().isoformat(),
        "device_simple_path": str(DEVICE_SIMPLE_PATH),
        "images_dir": str(IMAGES_DIR),
        "arms": arms,
        "cameras": simple_cameras,
        "summary": {
            "arms": len(arms),
            "cameras": len(cameras),
            "captured_images": sum(1 for cam in simple_cameras.values() if cam.get("capture_status") == "saved"),
        },
    }


def render_text(data: Dict[str, Any]) -> str:
    lines: List[str] = []
    lines.append("SO-101 设备扫描结果")
    lines.append(f"时间: {data['timestamp']}")
    lines.append("")
    lines.append(f"device_simple: {data['device_simple_path']}")
    lines.append(f"images: {data['images_dir']}")
    lines.append("")
    lines.append(
        f"摘要: arms={data['summary']['arms']} cameras={data['summary']['cameras']} captured_images={data['summary']['captured_images']}"
    )
    lines.append("")
    lines.append("机械臂:")
    if data["arms"]:
        for serial, arm in data["arms"].items():
            lines.append(
                f"  - {serial}: tty={arm.get('tty', '')} by-id={arm.get('port', '')}"
            )
    else:
        lines.append("  - 未检测到机械臂")
    lines.append("")
    lines.append("相机:")
    if data["cameras"]:
        for serial, cam in data["cameras"].items():
            lines.append(
                f"  - {serial}: dev={cam.get('dev', '')} by-path={cam.get('by_path', '')} image={cam.get('image') or '未生成'}"
            )
            if cam.get("capture_detail"):
                lines.append(f"    capture: {cam.get('capture_detail')}")
    else:
        lines.append("  - 未检测到相机")
    return "\n".join(lines).strip() + "\n"


def main():
    args = parse_args()
    cameras, arms = detect_hardware(args.skip_capture)
    device_simple = build_device_simple(cameras, arms)
    save_json(DEVICE_SIMPLE_PATH, device_simple)

    if args.format == "json":
        print(json.dumps(device_simple, indent=2, ensure_ascii=False))
    else:
        print(render_text(device_simple), end="")


if __name__ == "__main__":
    main()
