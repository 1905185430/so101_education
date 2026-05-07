#!/usr/bin/env python3
"""
SO-101 teaching-oriented hardware detection and command template helper.

The script does three jobs:
1. Detect arms and cameras and keep simple history.
2. Restore role identities such as leader/follower/top_camera/wrist_camera.
3. Produce reference command templates that students must edit by hand.

Usage examples:
    python3 tools/detect_system.py
    python3 tools/detect_system.py --show-template calibrate
    python3 tools/detect_system.py --stage robot --format markdown
    python3 tools/detect_system.py --write-roles-template
"""

from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Tuple


BASE_DIR = Path(__file__).parent / "devices"
IMAGES_DIR = BASE_DIR / "images"
HISTORY_PATH = BASE_DIR / "history.json"
ROLES_PATH = BASE_DIR / "device_roles.json"
DEVICE_FULL_PATH = BASE_DIR / "device.json"
DEVICE_SIMPLE_PATH = BASE_DIR / "device_simple.json"
REPORT_JSON_PATH = BASE_DIR / "report.json"
REPORT_MD_PATH = BASE_DIR / "report.md"

ARM_ROLE_ORDER = ["leader", "follower"]
CAMERA_ROLE_ORDER = ["top_camera", "wrist_camera", "side_camera"]
SUPPORTED_STAGES = ["env", "robot", "camera", "train", "all"]
SUPPORTED_FORMATS = ["text", "json", "markdown"]
SUPPORTED_TEMPLATES = ["calibrate", "teleoperate", "record", "replay", "rollout"]


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


def command_exists(cmd: str) -> bool:
    return shutil.which(cmd) is not None


def load_json(path: Path, default: Any) -> Any:
    if not path.exists():
        return default
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return default


def save_json(path: Path, data: Any):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="SO-101 teaching hardware detection helper")
    parser.add_argument("--stage", choices=SUPPORTED_STAGES, default="all")
    parser.add_argument("--format", choices=SUPPORTED_FORMATS, default="text")
    parser.add_argument("--show-template", choices=SUPPORTED_TEMPLATES)
    parser.add_argument("--expected-arms", type=int)
    parser.add_argument("--expected-cameras", type=int)
    parser.add_argument("--skip-capture", action="store_true")
    parser.add_argument("--write-roles-template", action="store_true")
    return parser.parse_args()


def get_python_version() -> str:
    return sys.version.split()[0]


def get_current_user_groups() -> List[str]:
    result = run_cmd(["id", "-nG"])
    groups = result.stdout.strip().split()
    return groups if groups else []


def detect_env() -> List[Dict[str, str]]:
    checks = []
    python_version = get_python_version()
    checks.append(
        make_check(
            "python",
            "pass" if python_version.startswith("3.10") or python_version.startswith("3.11") or python_version.startswith("3.12") else "warn",
            f"当前 Python 版本: {python_version}",
            "LeRobot 常见教学环境建议使用 Python 3.10-3.12。",
        )
    )

    for cmd in ["ffmpeg", "v4l2-ctl", "nvidia-smi", "lerobot-find-port", "lerobot-calibrate", "lerobot-record", "lerobot-train", "lerobot-rollout"]:
        checks.append(
            make_check(
                cmd,
                "pass" if command_exists(cmd) else "warn",
                f"{cmd}: {'已找到' if command_exists(cmd) else '未找到'}",
                f"如果后续实验会用到 {cmd}，请先在 LeRobot 环境中完成安装。",
            )
        )

    try:
        import cv2  # type: ignore

        checks.append(make_check("opencv-python", "pass", f"cv2 已安装: {cv2.__version__}", ""))
    except Exception:
        checks.append(
            make_check(
                "opencv-python",
                "warn",
                "cv2 未安装",
                "如需保存相机截图，请在教学环境中安装 opencv-python。",
            )
        )

    groups = get_current_user_groups()
    checks.append(
        make_check(
            "dialout",
            "pass" if "dialout" in groups else "warn",
            f"当前用户组: {' '.join(groups) if groups else '未知'}",
            "若串口权限不足，请执行 sudo usermod -a -G dialout $USER 后重新登录。",
        )
    )
    return checks


def make_check(name: str, status: str, detail: str, hint: str) -> Dict[str, str]:
    return {"name": name, "status": status, "detail": detail, "hint": hint}


def get_camera_info(dev_path: str) -> Dict[str, Any]:
    info: Dict[str, Any] = {"dev": dev_path}

    output = run_cmd(["v4l2-ctl", "--device", dev_path, "--info"]).stdout
    for line in output.splitlines():
        if "Card type" in line:
            info["product"] = line.split(":")[-1].strip()
            break
    if not info.get("product"):
        return {}

    dev_name = Path(dev_path).name
    for link in Path("/dev/v4l/by-id").glob("*"):
        try:
            if link.resolve().name == dev_name:
                info["by_id"] = str(link)
                if "usb-" in link.name:
                    info["serial"] = link.name.replace("usb-", "").split("-video-index")[0]
                break
        except Exception:
            pass

    for link in Path("/dev/v4l/by-path").glob("*"):
        try:
            if link.resolve().name == dev_name:
                info["by_path"] = str(link)
                break
        except Exception:
            pass

    by_id = info.get("by_id", "")
    if "-video-index" in by_id and not by_id.endswith("-index0"):
        return {}

    if not info.get("serial"):
        info["serial"] = dev_name

    info["formats"] = get_formats(dev_path)
    info["color_stream"] = has_color_stream(info["formats"])
    return info


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
    color_formats = {"YUYV", "MJPG", "NV12", "RGB3", "BGR3"}
    return any(fmt.get("fourcc") in color_formats for fmt in formats)


def get_arm_info(dev_path: str) -> Dict[str, Any]:
    info: Dict[str, Any] = {"tty": dev_path}
    dev_name = Path(dev_path).name

    for link in Path("/dev/serial/by-id").glob("*"):
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


def capture_image(dev_path: str, output_path: str) -> bool:
    try:
        import cv2  # type: ignore
    except Exception:
        return False

    try:
        output = run_cmd(["v4l2-ctl", "--device", dev_path, "--list-formats-ext"]).stdout
        color_formats = ["YUYV", "MJPG", "NV12", "RGB3", "BGR3"]
        if not any(fmt in output for fmt in color_formats):
            return False

        cap = cv2.VideoCapture(dev_path, cv2.CAP_V4L2)
        if not cap.isOpened():
            cap = cv2.VideoCapture(dev_path)
        if not cap.isOpened():
            return False
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        for _ in range(5):
            cap.read()
        ret, frame = cap.read()
        cap.release()
        if ret and frame is not None:
            cv2.imwrite(output_path, frame)
            return True
    except Exception:
        return False
    return False


def load_history() -> Dict[str, Any]:
    return load_json(HISTORY_PATH, {"cameras": {}, "arms": {}})


def update_status(raw: Dict[str, Dict[str, Any]], history: Dict[str, Dict[str, Any]]) -> Dict[str, Dict[str, Any]]:
    now = datetime.now().isoformat()
    result: Dict[str, Dict[str, Any]] = {}

    for serial, old_info in history.items():
        result[serial] = {**old_info, "status": "disconnected"}

    for serial, info in raw.items():
        if serial in result:
            result[serial].update(info)
            result[serial]["status"] = "connected"
            result[serial]["last_seen"] = now
        else:
            result[serial] = {
                **info,
                "status": "connected",
                "first_seen": now,
                "last_seen": now,
            }
    return result


def detect_hardware(skip_capture: bool) -> Tuple[Dict[str, Any], Dict[str, Any], List[Dict[str, str]]]:
    raw_cameras: Dict[str, Any] = {}
    for dev in sorted(Path("/dev").glob("video*")):
        if dev.name.replace("video", "").isdigit():
            info = get_camera_info(str(dev))
            if info and info.get("serial"):
                raw_cameras[info["serial"]] = info

    raw_arms: Dict[str, Any] = {}
    for pattern in ("ttyACM*", "ttyUSB*"):
        for dev in sorted(Path("/dev").glob(pattern)):
            info = get_arm_info(str(dev))
            raw_arms[info["serial"]] = info

    history = load_history()
    cameras = update_status(raw_cameras, history.get("cameras", {}))
    arms = update_status(raw_arms, history.get("arms", {}))
    save_json(HISTORY_PATH, {"cameras": cameras, "arms": arms})

    BASE_DIR.mkdir(parents=True, exist_ok=True)
    if IMAGES_DIR.exists():
        shutil.rmtree(IMAGES_DIR, ignore_errors=True)
    IMAGES_DIR.mkdir(parents=True, exist_ok=True)

    camera_checks: List[Dict[str, str]] = []
    if not skip_capture:
        for serial, cam in cameras.items():
            if cam.get("status") != "connected" or not cam.get("dev"):
                continue
            img_name = f"{Path(cam['dev']).name}.jpg"
            img_path = IMAGES_DIR / img_name
            if capture_image(cam["dev"], str(img_path)):
                cam["image"] = f"images/{img_name}"
            else:
                camera_checks.append(
                    make_check(
                        f"capture:{serial}",
                        "warn",
                        f"{serial} 未保存截图",
                        "如果需要截图，请确认相机支持彩色流并且 OpenCV 已安装。",
                    )
                )
    return cameras, arms, camera_checks


def load_roles_config() -> Dict[str, Any]:
    return load_json(ROLES_PATH, {"arms": {}, "cameras": {}})


def write_roles_template():
    template = {
        "arms": {
            "leader": {"serial": "", "port": ""},
            "follower": {"serial": "", "port": ""},
        },
        "cameras": {
            "top_camera": {"serial": "", "by_path": ""},
            "wrist_camera": {"serial": "", "by_path": ""},
            "side_camera": {"serial": "", "by_path": ""},
        },
    }
    save_json(ROLES_PATH, template)


def role_matches(spec: Any, device: Dict[str, Any]) -> bool:
    if not spec:
        return False

    if isinstance(spec, str):
        return spec in {
            device.get("serial"),
            device.get("tty"),
            device.get("dev"),
            device.get("port"),
            device.get("by_id"),
            device.get("by_path"),
        }

    if isinstance(spec, dict):
        for key in ["serial", "tty", "dev", "port", "by_id", "by_path"]:
            expected = spec.get(key)
            if expected and device.get(key) != expected:
                return False
        return any(spec.get(key) for key in ["serial", "tty", "dev", "port", "by_id", "by_path"])

    return False


def has_role_identity(spec: Any) -> bool:
    if isinstance(spec, str):
        return bool(spec.strip())
    if isinstance(spec, dict):
        return any(bool(spec.get(key)) for key in ["serial", "tty", "dev", "port", "by_id", "by_path"])
    return False


def resolve_roles(devices: Dict[str, Any], role_specs: Dict[str, Any]) -> Dict[str, Dict[str, Any]]:
    resolved: Dict[str, Dict[str, Any]] = {}
    for role_name, spec in role_specs.items():
        matched_serial = None
        matched_device = None
        for serial, device in devices.items():
            if role_matches(spec, device):
                matched_serial = serial
                matched_device = device
                break
        resolved[role_name] = {
            "configured": has_role_identity(spec),
            "status": matched_device.get("status", "missing") if matched_device else "missing",
            "match": matched_device or {},
            "serial": matched_serial,
            "spec": spec,
        }
    return resolved


def build_role_summary(cameras: Dict[str, Any], arms: Dict[str, Any], roles_config: Dict[str, Any]) -> Dict[str, Any]:
    arm_specs = {role: roles_config.get("arms", {}).get(role) for role in ARM_ROLE_ORDER}
    camera_specs = {role: roles_config.get("cameras", {}).get(role) for role in CAMERA_ROLE_ORDER}
    arm_roles = resolve_roles(arms, arm_specs)
    camera_roles = resolve_roles(cameras, camera_specs)
    return {"arms": arm_roles, "cameras": camera_roles}


def detect_train_checks() -> List[Dict[str, str]]:
    checks = []
    gpu_present = command_exists("nvidia-smi")
    checks.append(
        make_check(
            "gpu",
            "pass" if gpu_present else "warn",
            "检测到 NVIDIA GPU 工具。" if gpu_present else "未检测到 nvidia-smi。",
            "如果课程要求本地 ACT 训练，请确认机器已安装 NVIDIA 驱动和 CUDA 环境。",
        )
    )

    disk = shutil.disk_usage(Path.cwd())
    free_gb = disk.free / (1024**3)
    checks.append(
        make_check(
            "disk",
            "pass" if free_gb >= 20 else "warn",
            f"当前工作目录剩余空间约 {free_gb:.1f} GB。",
            "建议为数据采集和训练预留至少 20 GB 可用空间。",
        )
    )
    return checks


def build_device_checks(
    cameras: Dict[str, Any],
    arms: Dict[str, Any],
    args: argparse.Namespace,
    capture_checks: List[Dict[str, str]],
) -> Dict[str, List[Dict[str, str]]]:
    robot_checks: List[Dict[str, str]] = []
    camera_checks: List[Dict[str, str]] = []

    connected_arms = sum(1 for arm in arms.values() if arm.get("status") == "connected")
    connected_cameras = sum(1 for cam in cameras.values() if cam.get("status") == "connected")

    robot_checks.append(
        make_check(
            "arms_detected",
            "pass" if connected_arms > 0 else "fail",
            f"已连接机械臂数量: {connected_arms}",
            "请检查主从臂供电、USB 连接和串口权限。",
        )
    )
    if args.expected_arms is not None:
        robot_checks.append(
            make_check(
                "arms_expected",
                "pass" if connected_arms == args.expected_arms else "warn",
                f"期望 {args.expected_arms} 条机械臂，当前检测到 {connected_arms} 条。",
                "若数量不一致，请重新插拔机械臂并再次运行检测。",
            )
        )

    camera_checks.append(
        make_check(
            "cameras_detected",
            "pass" if connected_cameras > 0 else "warn",
            f"已连接相机数量: {connected_cameras}",
            "如果后续实验需要相机，请检查 USB 连接和供电。",
        )
    )
    if args.expected_cameras is not None:
        camera_checks.append(
            make_check(
                "cameras_expected",
                "pass" if connected_cameras == args.expected_cameras else "warn",
                f"期望 {args.expected_cameras} 路相机，当前检测到 {connected_cameras} 路。",
                "请确认相机连接数量是否符合本次实验要求。",
            )
        )

    color_count = sum(1 for cam in cameras.values() if cam.get("status") == "connected" and cam.get("color_stream"))
    camera_checks.append(
        make_check(
            "camera_color_stream",
            "pass" if color_count > 0 else "warn",
            f"支持彩色流的已连接相机数量: {color_count}",
            "如果采集或遥操作需要画面显示，请优先选择支持彩色流的相机。",
        )
    )
    camera_checks.extend(capture_checks)
    return {"robot": robot_checks, "camera": camera_checks}


def build_placeholder_values(role_summary: Dict[str, Any]) -> Dict[str, str]:
    placeholders = {
        "<LEADER_PORT>": "<请根据检测结果填写>",
        "<FOLLOWER_PORT>": "<请根据检测结果填写>",
        "<TOP_CAMERA_DEV>": "<请根据检测结果填写>",
        "<WRIST_CAMERA_DEV>": "<请根据检测结果填写>",
        "<SIDE_CAMERA_DEV>": "<请根据检测结果填写>",
        "<DATASET_REPO_ID>": "<请自行命名，例如 ${USER}/so101_pick_place>",
        "<OUTPUT_DIR>": "<请自行填写训练输出目录>",
        "<TASK_DESCRIPTION>": "<请填写任务描述，例如 pick cube and place into tray>",
        "<EPISODE_INDEX>": "0",
        "<CHECKPOINT_PATH>": "<请填写训练输出中的 checkpoint 路径>",
    }

    arm_roles = role_summary.get("arms", {})
    cam_roles = role_summary.get("cameras", {})

    if arm_roles.get("leader", {}).get("match", {}).get("tty"):
        placeholders["<LEADER_PORT>"] = arm_roles["leader"]["match"]["tty"]
    if arm_roles.get("follower", {}).get("match", {}).get("tty"):
        placeholders["<FOLLOWER_PORT>"] = arm_roles["follower"]["match"]["tty"]
    if cam_roles.get("top_camera", {}).get("match", {}).get("dev"):
        placeholders["<TOP_CAMERA_DEV>"] = cam_roles["top_camera"]["match"]["dev"]
    if cam_roles.get("wrist_camera", {}).get("match", {}).get("dev"):
        placeholders["<WRIST_CAMERA_DEV>"] = cam_roles["wrist_camera"]["match"]["dev"]
    if cam_roles.get("side_camera", {}).get("match", {}).get("dev"):
        placeholders["<SIDE_CAMERA_DEV>"] = cam_roles["side_camera"]["match"]["dev"]
    return placeholders


def build_reference_templates(role_summary: Dict[str, Any]) -> Dict[str, Any]:
    placeholders = build_placeholder_values(role_summary)
    templates: Dict[str, Any] = {}

    templates["calibrate"] = {
        "title": "校准参考命令",
        "reference_command": "\n".join(
            [
                "lerobot-calibrate \\",
                "  --teleop.type=so101_leader \\",
                "  --teleop.port=<LEADER_PORT>",
                "",
                "lerobot-calibrate \\",
                "  --robot.type=so101_follower \\",
                "  --robot.port=<FOLLOWER_PORT>",
            ]
        ),
        "replace_values": {
            "<LEADER_PORT>": placeholders["<LEADER_PORT>"],
            "<FOLLOWER_PORT>": placeholders["<FOLLOWER_PORT>"],
        },
        "fixed_parameters": [
            "--teleop.type=so101_leader",
            "--robot.type=so101_follower",
        ],
        "student_must_edit": ["<LEADER_PORT>", "<FOLLOWER_PORT>"],
        "expected_result": "主臂和从臂分别完成零位校准，终端出现校准完成或保存结果提示。",
        "self_check_questions": [
            "如果 leader 当前对应 /dev/ttyACM1，你应该改哪一段？",
            "为什么 leader 和 follower 不能共用同一个端口？",
        ],
    }

    teleoperate_command = "\n".join(
        [
            "lerobot-teleoperate \\",
            "  --robot.type=so101_follower \\",
            "  --robot.port=<FOLLOWER_PORT> \\",
            "  --teleop.type=so101_leader \\",
            "  --teleop.port=<LEADER_PORT> \\",
            "  --robot.cameras='{\"top\": {\"type\": \"opencv\", \"index_or_path\": \"<TOP_CAMERA_DEV>\", \"width\": 640, \"height\": 480, \"fps\": 30}, \"wrist\": {\"type\": \"opencv\", \"index_or_path\": \"<WRIST_CAMERA_DEV>\", \"width\": 640, \"height\": 480, \"fps\": 30}}' \\",
            "  --display_data=true",
        ]
    )
    templates["teleoperate"] = {
        "title": "遥操作参考命令",
        "reference_command": teleoperate_command,
        "replace_values": {
            "<LEADER_PORT>": placeholders["<LEADER_PORT>"],
            "<FOLLOWER_PORT>": placeholders["<FOLLOWER_PORT>"],
            "<TOP_CAMERA_DEV>": placeholders["<TOP_CAMERA_DEV>"],
            "<WRIST_CAMERA_DEV>": placeholders["<WRIST_CAMERA_DEV>"],
        },
        "fixed_parameters": [
            "--robot.type=so101_follower",
            "--teleop.type=so101_leader",
            "--display_data=true",
            "width=640 height=480 fps=30",
        ],
        "student_must_edit": [
            "<LEADER_PORT>",
            "<FOLLOWER_PORT>",
            "<TOP_CAMERA_DEV>",
            "<WRIST_CAMERA_DEV>",
        ],
        "expected_result": "移动主臂时，从臂同步运动，终端或弹窗可以看到 top 和 wrist 画面。",
        "self_check_questions": [
            "如果 wrist camera 实际是 /dev/video4，你应该改 JSON 里的哪一项？",
            "为什么本章要同时填写 leader、follower 和 camera 参数？",
        ],
    }

    record_command = "\n".join(
        [
            "lerobot-record \\",
            "  --robot.type=so101_follower \\",
            "  --robot.port=<FOLLOWER_PORT> \\",
            "  --teleop.type=so101_leader \\",
            "  --teleop.port=<LEADER_PORT> \\",
            "  --robot.cameras='{\"top\": {\"type\": \"opencv\", \"index_or_path\": \"<TOP_CAMERA_DEV>\", \"width\": 640, \"height\": 480, \"fps\": 30}, \"wrist\": {\"type\": \"opencv\", \"index_or_path\": \"<WRIST_CAMERA_DEV>\", \"width\": 640, \"height\": 480, \"fps\": 30}}' \\",
            "  --display_data=true \\",
            "  --dataset.repo_id=<DATASET_REPO_ID> \\",
            "  --dataset.single_task='<TASK_DESCRIPTION>' \\",
            "  --dataset.num_episodes=5 \\",
            "  --dataset.episode_time_s=20 \\",
            "  --dataset.push_to_hub=false",
        ]
    )
    templates["record"] = {
        "title": "数据采集参考命令",
        "reference_command": record_command,
        "replace_values": {
            "<LEADER_PORT>": placeholders["<LEADER_PORT>"],
            "<FOLLOWER_PORT>": placeholders["<FOLLOWER_PORT>"],
            "<TOP_CAMERA_DEV>": placeholders["<TOP_CAMERA_DEV>"],
            "<WRIST_CAMERA_DEV>": placeholders["<WRIST_CAMERA_DEV>"],
            "<DATASET_REPO_ID>": placeholders["<DATASET_REPO_ID>"],
            "<TASK_DESCRIPTION>": placeholders["<TASK_DESCRIPTION>"],
        },
        "fixed_parameters": [
            "--robot.type=so101_follower",
            "--teleop.type=so101_leader",
            "--dataset.num_episodes=5",
            "--dataset.episode_time_s=20",
            "--dataset.push_to_hub=false",
        ],
        "student_must_edit": [
            "<LEADER_PORT>",
            "<FOLLOWER_PORT>",
            "<TOP_CAMERA_DEV>",
            "<WRIST_CAMERA_DEV>",
            "<DATASET_REPO_ID>",
            "<TASK_DESCRIPTION>",
        ],
        "expected_result": "完成多条 episode 采集，本地生成数据集目录，可用于 replay 和 ACT 训练。",
        "self_check_questions": [
            "如果你的数据集名想换成 so101_stack_blocks，应修改哪个占位符？",
            "为什么录制命令里也必须保留 camera 参数？",
        ],
    }

    templates["replay"] = {
        "title": "回放参考命令",
        "reference_command": "\n".join(
            [
                "lerobot-replay \\",
                "  --robot.type=so101_follower \\",
                "  --robot.port=<FOLLOWER_PORT> \\",
                "  --dataset.repo_id=<DATASET_REPO_ID> \\",
                "  --episode=<EPISODE_INDEX>",
            ]
        ),
        "replace_values": {
            "<FOLLOWER_PORT>": placeholders["<FOLLOWER_PORT>"],
            "<DATASET_REPO_ID>": placeholders["<DATASET_REPO_ID>"],
            "<EPISODE_INDEX>": placeholders["<EPISODE_INDEX>"],
        },
        "fixed_parameters": ["--robot.type=so101_follower"],
        "student_must_edit": ["<FOLLOWER_PORT>", "<DATASET_REPO_ID>", "<EPISODE_INDEX>"],
        "expected_result": "从臂按已采集轨迹复现动作，学生能验证录制数据是否可用。",
        "self_check_questions": [
            "如果要回放第 2 条 episode，应修改哪个占位符？",
            "为什么 replay 时不需要填写 leader 端口？",
        ],
    }

    templates["rollout"] = {
        "title": "策略部署参考命令",
        "reference_command": "\n".join(
            [
                "lerobot-rollout \\",
                "  --robot.type=so101_follower \\",
                "  --robot.port=<FOLLOWER_PORT> \\",
                "  --robot.cameras='{\"top\": {\"type\": \"opencv\", \"index_or_path\": \"<TOP_CAMERA_DEV>\", \"width\": 640, \"height\": 480, \"fps\": 30}, \"wrist\": {\"type\": \"opencv\", \"index_or_path\": \"<WRIST_CAMERA_DEV>\", \"width\": 640, \"height\": 480, \"fps\": 30}}' \\",
                "  --policy.path=<CHECKPOINT_PATH>",
            ]
        ),
        "replace_values": {
            "<FOLLOWER_PORT>": placeholders["<FOLLOWER_PORT>"],
            "<TOP_CAMERA_DEV>": placeholders["<TOP_CAMERA_DEV>"],
            "<WRIST_CAMERA_DEV>": placeholders["<WRIST_CAMERA_DEV>"],
            "<CHECKPOINT_PATH>": placeholders["<CHECKPOINT_PATH>"],
        },
        "fixed_parameters": ["--robot.type=so101_follower", "width=640 height=480 fps=30"],
        "student_must_edit": [
            "<FOLLOWER_PORT>",
            "<TOP_CAMERA_DEV>",
            "<WRIST_CAMERA_DEV>",
            "<CHECKPOINT_PATH>",
        ],
        "expected_result": "已训练策略加载成功，follower 在相机反馈下执行任务。",
        "self_check_questions": [
            "为什么 rollout 阶段还要再次检查 top 和 wrist 的 camera 端口？",
            "如果 checkpoint 目录换了，你应替换哪个占位符？",
        ],
    }
    return templates


def summarize_status(check_groups: Dict[str, List[Dict[str, str]]]) -> Dict[str, int]:
    counts = {"pass": 0, "warn": 0, "fail": 0}
    for checks in check_groups.values():
        for item in checks:
            counts[item["status"]] += 1
    return counts


def build_report(
    args: argparse.Namespace,
    env_checks: List[Dict[str, str]],
    device_checks: Dict[str, List[Dict[str, str]]],
    train_checks: List[Dict[str, str]],
    cameras: Dict[str, Any],
    arms: Dict[str, Any],
    role_summary: Dict[str, Any],
    roles_config: Dict[str, Any],
    templates: Dict[str, Any],
) -> Dict[str, Any]:
    timestamp = datetime.now().isoformat()
    checks: Dict[str, List[Dict[str, str]]] = {}
    if args.stage in ("env", "all"):
        checks["env"] = env_checks
    if args.stage in ("robot", "all"):
        checks["robot"] = device_checks["robot"]
    if args.stage in ("camera", "all"):
        checks["camera"] = device_checks["camera"]
    if args.stage in ("train", "all"):
        checks["train"] = train_checks

    template_subset = {args.show_template: templates[args.show_template]} if args.show_template else templates
    summary_counts = summarize_status(checks)
    summary = {
        "checks": summary_counts,
        "arms": {
            "total": len(arms),
            "connected": sum(1 for arm in arms.values() if arm.get("status") == "connected"),
        },
        "cameras": {
            "total": len(cameras),
            "connected": sum(1 for cam in cameras.values() if cam.get("status") == "connected"),
        },
    }

    next_steps = [
        "先核对角色身份是否正确，再开始修改参考命令。",
        "参考命令中的占位符必须由学生手动替换后再执行。",
        "如果角色未绑定，请先编辑 tools/devices/device_roles.json。",
    ]

    return {
        "timestamp": timestamp,
        "stage": args.stage,
        "system": {
            "cwd": str(Path.cwd()),
            "python_version": get_python_version(),
            "platform": sys.platform,
        },
        "checks": checks,
        "roles_config": roles_config,
        "roles": role_summary,
        "devices": {
            "arms": arms,
            "cameras": cameras,
        },
        "summary": summary,
        "reference_templates": template_subset,
        "next_steps": next_steps,
    }


def format_role_line(role_name: str, data: Dict[str, Any], key: str) -> str:
    match = data.get("match", {})
    current_value = match.get(key, "未识别")
    status = data.get("status", "missing")
    return f"- `{role_name}`: {status} | 当前{key}: `{current_value}`"


def get_lab_focus_notes() -> List[str]:
    return [
        "第一次课重点关注 `leader`、`follower` 和当前 `tty`，用于角色绑定与校准命令改写。相关背景先阅读 [01_so101_intro.md](/home/xuan/so101_education/primer/01_so101_intro.md) 和 [02_lerobot_intro.md](/home/xuan/so101_education/primer/02_lerobot_intro.md)。",
        "第二次课在第一次课基础上新增关注 `top_camera`、`wrist_camera` 和当前 `video` 节点，用于遥操作、录制与回放。`side_camera` 作为可选扩展视角。相关背景先阅读 [03_embodied_data_intro.md](/home/xuan/so101_education/primer/03_embodied_data_intro.md)。",
        "第三次课重点沿用第二次课的数据集命名与相机映射，并结合训练输出目录与 checkpoint 路径完成训练启动和 rollout。默认相机为 `top_camera + wrist_camera`，`side_camera` 为可选扩展。相关背景先阅读 [04_act_intro.md](/home/xuan/so101_education/primer/04_act_intro.md)。",
    ]


def render_markdown(report: Dict[str, Any]) -> str:
    lines: List[str] = []
    lines.append("# SO-101 实验设备检测报告")
    lines.append("")
    lines.append(f"- 生成时间: `{report['timestamp']}`")
    lines.append(f"- 检测阶段: `{report['stage']}`")
    lines.append("")
    lines.append("## 当前角色身份与端口")
    lines.append("")
    for role_name in ARM_ROLE_ORDER:
        role_data = report["roles"]["arms"].get(role_name)
        if role_data:
            lines.append(format_role_line(role_name, role_data, "tty"))
    for role_name in CAMERA_ROLE_ORDER:
        role_data = report["roles"]["cameras"].get(role_name)
        if role_data:
            lines.append(format_role_line(role_name, role_data, "dev"))
    lines.append("")
    lines.append("## 三次课使用提示")
    lines.append("")
    for note in get_lab_focus_notes():
        lines.append(f"- {note}")
    lines.append("")
    lines.append("## 当前识别到的设备")
    lines.append("")
    lines.append("### 机械臂")
    lines.append("")
    for serial, arm in report["devices"]["arms"].items():
        lines.append(
            f"- `{serial}` | status=`{arm.get('status')}` | tty=`{arm.get('tty', '未知')}` | by-id=`{arm.get('port', '未知')}`"
        )
    if not report["devices"]["arms"]:
        lines.append("- 未检测到机械臂")
    lines.append("")
    lines.append("### 相机")
    lines.append("")
    for serial, cam in report["devices"]["cameras"].items():
        lines.append(
            f"- `{serial}` | status=`{cam.get('status')}` | dev=`{cam.get('dev', '未知')}` | by-path=`{cam.get('by_path', '未知')}`"
        )
    if not report["devices"]["cameras"]:
        lines.append("- 未检测到相机")
    lines.append("")
    lines.append("## 检查结果")
    lines.append("")
    for group_name, items in report["checks"].items():
        lines.append(f"### {group_name}")
        lines.append("")
        for item in items:
            lines.append(f"- `{item['status'].upper()}` {item['name']}: {item['detail']}")
            if item["hint"]:
                lines.append(f"  提示: {item['hint']}")
        lines.append("")
    lines.append("## 参考命令模板")
    lines.append("")
    for name, template in report["reference_templates"].items():
        lines.append(f"### {name} - {template['title']}")
        lines.append("")
        lines.append("```bash")
        lines.append(template["reference_command"])
        lines.append("```")
        lines.append("")
        lines.append("本机应参考的占位符取值：")
        for placeholder, value in template["replace_values"].items():
            lines.append(f"- `{placeholder}` -> `{value}`")
        lines.append("")
        lines.append("你需要修改的参数：")
        for placeholder in template["student_must_edit"]:
            lines.append(f"- `{placeholder}`")
        lines.append("")
        lines.append(f"修改后应达到的效果：{template['expected_result']}")
        lines.append("")
        lines.append("自检问题：")
        for question in template["self_check_questions"]:
            lines.append(f"- {question}")
        lines.append("")
    return "\n".join(lines).strip() + "\n"


def render_text(report: Dict[str, Any]) -> str:
    lines: List[str] = []
    lines.append("SO-101 实验设备检测结果")
    lines.append(f"时间: {report['timestamp']}")
    lines.append("")
    lines.append("角色身份与当前端口:")
    for role_name in ARM_ROLE_ORDER:
        role_data = report["roles"]["arms"].get(role_name)
        if role_data:
            match = role_data.get("match", {})
            lines.append(f"  - {role_name}: {role_data.get('status')} | tty={match.get('tty', '未识别')}")
    for role_name in CAMERA_ROLE_ORDER:
        role_data = report["roles"]["cameras"].get(role_name)
        if role_data:
            match = role_data.get("match", {})
            lines.append(f"  - {role_name}: {role_data.get('status')} | dev={match.get('dev', '未识别')}")
    lines.append("")
    lines.append("三次课使用提示:")
    for note in get_lab_focus_notes():
        lines.append(f"  - {note}")
    lines.append("")
    lines.append("当前识别到的设备:")
    for serial, arm in report["devices"]["arms"].items():
        lines.append(f"  - arm {serial}: status={arm.get('status')} tty={arm.get('tty', '未知')} by-id={arm.get('port', '未知')}")
    for serial, cam in report["devices"]["cameras"].items():
        lines.append(f"  - camera {serial}: status={cam.get('status')} dev={cam.get('dev', '未知')} by-path={cam.get('by_path', '未知')}")
    if not report["devices"]["arms"] and not report["devices"]["cameras"]:
        lines.append("  - 未检测到设备")
    lines.append("")
    lines.append("检查摘要:")
    summary = report["summary"]["checks"]
    lines.append(f"  PASS={summary['pass']} WARN={summary['warn']} FAIL={summary['fail']}")
    lines.append("")
    for group_name, items in report["checks"].items():
        lines.append(f"[{group_name}]")
        for item in items:
            hint = f" | 提示: {item['hint']}" if item["hint"] else ""
            lines.append(f"  - {item['status'].upper()} {item['name']}: {item['detail']}{hint}")
        lines.append("")
    lines.append("参考命令模板:")
    for name, template in report["reference_templates"].items():
        lines.append(f"  [{name}] {template['title']}")
        for cmd_line in template["reference_command"].splitlines():
            lines.append(f"    {cmd_line}")
        lines.append("    你需要替换:")
        for placeholder in template["student_must_edit"]:
            lines.append(f"      - {placeholder} -> {template['replace_values'].get(placeholder, '请自行填写')}")
        lines.append(f"    修改后应达到的效果: {template['expected_result']}")
        lines.append("")
    lines.append(f"完整 Markdown 报告已写入: {REPORT_MD_PATH}")
    return "\n".join(lines).strip() + "\n"


def build_device_exports(report: Dict[str, Any]) -> Tuple[Dict[str, Any], Dict[str, Any]]:
    timestamp = report["timestamp"]
    full = {
        "timestamp": timestamp,
        "roles": report["roles"],
        "arms": report["devices"]["arms"],
        "cameras": report["devices"]["cameras"],
        "summary": report["summary"],
    }
    simple_cameras = {}
    for serial, camera in report["devices"]["cameras"].items():
        simple_cameras[serial] = {k: v for k, v in camera.items() if k != "formats"}
    simple = {
        "timestamp": timestamp,
        "roles": report["roles"],
        "arms": report["devices"]["arms"],
        "cameras": simple_cameras,
        "summary": report["summary"],
    }
    return full, simple


def main():
    args = parse_args()
    BASE_DIR.mkdir(parents=True, exist_ok=True)

    if args.write_roles_template:
        write_roles_template()

    env_checks = detect_env()
    cameras, arms, capture_checks = detect_hardware(args.skip_capture)
    roles_config = load_roles_config()
    role_summary = build_role_summary(cameras, arms, roles_config)
    device_checks = build_device_checks(cameras, arms, args, capture_checks)
    train_checks = detect_train_checks()
    templates = build_reference_templates(role_summary)

    report = build_report(
        args,
        env_checks,
        device_checks,
        train_checks,
        cameras,
        arms,
        role_summary,
        roles_config,
        templates,
    )

    full_export, simple_export = build_device_exports(report)
    save_json(DEVICE_FULL_PATH, full_export)
    save_json(DEVICE_SIMPLE_PATH, simple_export)
    save_json(REPORT_JSON_PATH, report)
    REPORT_MD_PATH.write_text(render_markdown(report), encoding="utf-8")

    if args.format == "json":
        print(json.dumps(report, indent=2, ensure_ascii=False))
    elif args.format == "markdown":
        print(render_markdown(report), end="")
    else:
        print(render_text(report), end="")


if __name__ == "__main__":
    main()
