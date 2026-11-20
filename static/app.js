import {
  FaceLandmarker,
  HandLandmarker,
  PoseLandmarker,
  FilesetResolver,
} from "https://cdn.jsdelivr.net/npm/@mediapipe/tasks-vision@0.10.14";

const POSE_IDX = [11, 12, 13, 14];
const MOUTH_IDX = [61, 291, 13, 14];
const MP_WASM =
  "https://cdn.jsdelivr.net/npm/@mediapipe/tasks-vision@0.10.14/wasm";

const video = document.getElementById("video");
const canvas = document.getElementById("overlay");
const ctx = canvas.getContext("2d");
const line1 = document.getElementById("output-line1");
const line2 = document.getElementById("output-line2");

let handLm, poseLm, faceLm;
let frameMs = 0;
let activeTab = "dich";
let mediaStream = null;

const handPoints = (r) => r.landmarks ?? r.handLandmarks ?? [];

function syncCanvasSize() {
  const box = video.parentElement;
  canvas.width = box.clientWidth;
  canvas.height = box.clientHeight;
}

function drawCameraFrame() {
  const w = canvas.width;
  const h = canvas.height;
  const vw = video.videoWidth || w;
  const vh = video.videoHeight || h;
  const scale = Math.min(w / vw, h / vh);
  const dw = vw * scale;
  const dh = vh * scale;
  const ox = (w - dw) / 2;
  const oy = (h - dh) / 2;

  ctx.fillStyle = "#ffffff";
  ctx.fillRect(0, 0, w, h);
  ctx.save();
  ctx.translate(ox + dw, oy);
  ctx.scale(-1, 1);
  ctx.drawImage(video, 0, 0, dw, dh);
  ctx.restore();
  return { ox, oy, dw, dh };
}

const mirrorLandmarks = (lm) =>
  lm.map((p) => ({ ...p, x: 1 - p.x }));

const mapPoint = (p, box) => ({
  x: box.ox + p.x * box.dw,
  y: box.oy + p.y * box.dh,
});

document.querySelectorAll(".pill").forEach((btn) => {
  btn.addEventListener("click", () => {
    document.querySelectorAll(".pill").forEach((b) => b.classList.remove("active"));
    btn.classList.add("active");
    activeTab = btn.dataset.tab;
    const text =
      activeTab === "tra"
        ? ["(Tra cứu từ / câu)", "— module sau"]
        : activeTab === "luyen"
          ? ["(Luyện chuỗi ký tự)", "— module sau"]
          : ["ABC", "cdscv"];
    line1.textContent = text[0];
    line2.textContent = text[1];
  });
});

function cameraHelpText(err) {
  const name = err?.name || "";
  if (name === "NotFoundError" || /not found/i.test(err?.message || "")) {
    return "Không thấy webcam — bật camera, cấp quyền trình duyệt, hoặc dùng python app.py.";
  }
  if (name === "NotAllowedError" || name === "PermissionDeniedError") {
    return "Cho phép camera trên thanh địa chỉ rồi F5.";
  }
  if (name === "NotReadableError") {
    return "Camera đang bận — đóng app khác dùng webcam.";
  }
  if (!window.isSecureContext) {
    return "Mở http://127.0.0.1:8080 sau khi chạy python web_app.py.";
  }
  return String(err?.message || err);
}

async function startCamera() {
  mediaStream?.getTracks().forEach((t) => t.stop());
  mediaStream = await navigator.mediaDevices.getUserMedia({
    video: { width: { ideal: 640 }, height: { ideal: 480 } },
    audio: false,
  });
  video.srcObject = mediaStream;
  await video.play();
  if (!video.videoWidth) {
    await new Promise((r) => {
      video.onloadeddata = () => r();
    });
  }
  syncCanvasSize();
  window.addEventListener("resize", syncCanvasSize);
  requestAnimationFrame(tick);
}

async function initModels() {
  const vision = await FilesetResolver.forVisionTasks(MP_WASM);
  const videoMode = { runningMode: "VIDEO" };
  const handBase = {
    modelAssetPath:
      "https://storage.googleapis.com/mediapipe-models/hand_landmarker/hand_landmarker/float16/1/hand_landmarker.task",
  };
  const handOpts = {
    ...videoMode,
    numHands: 2,
    minHandDetectionConfidence: 0.25,
    minHandPresenceConfidence: 0.25,
    minTrackingConfidence: 0.25,
  };
  try {
    handLm = await HandLandmarker.createFromOptions(vision, {
      baseOptions: { ...handBase, delegate: "GPU" },
      ...handOpts,
    });
  } catch {
    handLm = await HandLandmarker.createFromOptions(vision, {
      baseOptions: handBase,
      ...handOpts,
    });
  }
  poseLm = await PoseLandmarker.createFromOptions(vision, {
    baseOptions: {
      modelAssetPath:
        "https://storage.googleapis.com/mediapipe-models/pose_landmarker/pose_landmarker_lite/float16/1/pose_landmarker_lite.task",
    },
    ...videoMode,
  });
  faceLm = await FaceLandmarker.createFromOptions(vision, {
    baseOptions: {
      modelAssetPath:
        "https://storage.googleapis.com/mediapipe-models/face_landmarker/face_landmarker/float16/1/face_landmarker.task",
    },
    ...videoMode,
    numFaces: 1,
  });
}

function drawPosePoints(landmarks, box) {
  if (!landmarks?.length) return;
  const lm = mirrorLandmarks(landmarks[0]);
  for (const idx of POSE_IDX) {
    const p = lm[idx];
    if (!p || (p.visibility ?? 1) < 0.5) continue;
    const { x, y } = mapPoint(p, box);
    ctx.fillStyle = "#00ffff";
    ctx.beginPath();
    ctx.arc(x, y, 8, 0, Math.PI * 2);
    ctx.fill();
    ctx.strokeStyle = "#fff";
    ctx.lineWidth = 2;
    ctx.stroke();
  }
}

function drawMouthPoints(landmarks, box) {
  if (!landmarks?.length) return;
  const lm = mirrorLandmarks(landmarks[0]);
  for (const idx of MOUTH_IDX) {
    const p = lm[idx];
    if (!p) continue;
    const { x, y } = mapPoint(p, box);
    ctx.fillStyle = "#ff00ff";
    ctx.beginPath();
    ctx.arc(x, y, 5, 0, Math.PI * 2);
    ctx.fill();
  }
}

function drawHands(handLmList, box) {
  const conns = HandLandmarker.HAND_CONNECTIONS;
  for (const h of handLmList) {
    const mirrored = mirrorLandmarks(h);
    for (const p of mirrored) {
      const { x, y } = mapPoint(p, box);
      ctx.fillStyle = "#ff0000";
      ctx.beginPath();
      ctx.arc(x, y, 4, 0, Math.PI * 2);
      ctx.fill();
    }
    if (!conns?.length) continue;
    for (const c of conns) {
      const a = mapPoint(mirrored[c.start], box);
      const b = mapPoint(mirrored[c.end], box);
      ctx.strokeStyle = "#00ff00";
      ctx.lineWidth = 2;
      ctx.beginPath();
      ctx.moveTo(a.x, a.y);
      ctx.lineTo(b.x, b.y);
      ctx.stroke();
    }
  }
}

function tick() {
  if (video.readyState < 2) {
    requestAnimationFrame(tick);
    return;
  }
  if (activeTab === "dich") {
    frameMs += 33;
    const hand = handLm.detectForVideo(video, frameMs);
    const pose = poseLm.detectForVideo(video, frameMs);
    const face = faceLm.detectForVideo(video, frameMs);
    const box = drawCameraFrame();
    const hands = handPoints(hand);
    if (hands.length) drawHands(hands, box);
    if (pose.landmarks?.length) drawPosePoints(pose.landmarks, box);
    if (face.faceLandmarks?.length) drawMouthPoints(face.faceLandmarks, box);
  }
  requestAnimationFrame(tick);
}

(async () => {
  try {
    await initModels();
    await startCamera();
  } catch (e) {
    console.error(e);
    alert(cameraHelpText(e));
  }
})();